from fastapi import APIRouter
from fastapi import Depends
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from app.config import settings
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.schemas import UserResponse
from app.schemas import UserLogin, AuthResponse
from app.schemas import TokenResponse, VerifyOtpRequest, ResendOtpRequest

from app.auth import hash_password, verify_password, decode_access_token
from app.auth import create_access_token

from app.auth import oauth2_scheme


from app.crud import get_user_by_email
from app.crud import get_user_by_id

from app.auth_service import generate_auth_response

from app.redis_client import redis_client
from app.otp import generate_otp, verify_login_otp as verify_login_otp_service, save_login_otp

from app.email_service import send_login_otp_background

OTP_DAILY_LIMIT = 3
OTP_IP_DAILY_LIMIT = 15
OTP_COOLDOWN_SECONDS = 60

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

router = APIRouter()

@router.post(
    "/signup",
    response_model=None
)
def signup(
    user:UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user.email)
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
        
    new_user = User(
        email  = user.email,
        hashed_password = hash_password(user.password),
        full_name = user.full_name,
        auth_provider="local",
        is_verified=False
    )
    
    db.add(new_user)
    
    db.commit()
    
    db.refresh(new_user)
    
    otp = generate_otp()

    redis_client.setex(
        f"email_otp:{new_user.email}",
        300,
        otp
    )

    print(f"OTP for {new_user.email}: {otp}")
    
    return {
    "message": "Signup successful. Please verify your email."
}
    
    
def check_otp_limits(email: str, request: Request):
    email = email.lower()
    ip = request.client.host if request.client else "unknown"

    cooldown_key = f"otp:cooldown:{email}"
    daily_key = f"otp:daily:{email}"
    ip_key = f"otp:ip:{ip}"

    if redis_client.exists(cooldown_key):
        raise HTTPException(
            status_code=429,
            detail="Please wait before requesting another OTP."
        )

    daily_count = redis_client.incr(daily_key)
    if daily_count == 1:
        redis_client.expire(daily_key, 86400)

    if daily_count > OTP_DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Daily OTP limit reached. Try again tomorrow."
        )

    ip_count = redis_client.incr(ip_key)
    if ip_count == 1:
        redis_client.expire(ip_key, 86400)

    if ip_count > OTP_IP_DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many OTP requests from this network."
        )

    redis_client.setex(cooldown_key, OTP_COOLDOWN_SECONDS, "1")


@router.post("/login")
def login(
    user: UserLogin,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user.email)

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    check_otp_limits(existing_user.email, request)
    
    otp = generate_otp()

    save_login_otp(
        db=db,
        user=existing_user,
        otp=otp
    )

    background_tasks.add_task(
        send_login_otp_background,
        existing_user.email,
        otp
    )

    return {
        "message": "OTP generated successfully",
        "email": existing_user.email,
        "requires_otp": True
    }
    
@router.post("/login/verify-otp")
def verify_login_otp_route(
    payload: VerifyOtpRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, payload.email)

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    otp_valid = verify_login_otp_service(
        db=db,
        user=existing_user,
        otp=payload.otp
    )

    if not otp_valid:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "user_id": existing_user.id
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,      # True in production HTTPS
        samesite="lax",
        max_age=60 * 60,
    )

    return {
        "message": "Login successful",
        "user": {
            "id": existing_user.id,
            "email": existing_user.email,
            "full_name": existing_user.full_name,
        }
    }
    
@router.get("/get_user", response_model=UserResponse)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user



@router.get("/oauth/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        settings.GOOGLE_REDIRECT_URI
    )


@router.get("/oauth/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    token = await oauth.google.authorize_access_token(request)

    user_info = token.get("userinfo")

    email = user_info["email"]
    full_name = user_info.get("name", email)

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        user = User(
            email=email,
            full_name=full_name,
            hashed_password="GOOGLE_OAUTH_USER",
            auth_provider="google",
            is_verified=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id
        }
    )

    response = RedirectResponse(
        url=f"{settings.FRONTEND_URL}/oauth/success"
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60
    )

    return response


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return {
        "message": "Logged out successfully"
    }
    
@router.post("/login/resend-otp")
def resend_login_otp(
    payload: ResendOtpRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, payload.email)

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    check_otp_limits(existing_user.email, request)

    otp = generate_otp()

    save_login_otp(
        db=db,
        user=existing_user,
        otp=otp
    )

    background_tasks.add_task(
        send_login_otp_background,
        existing_user.email,
        otp
    )

    return {
        "message": "OTP resent successfully",
        "email": existing_user.email
    }
    
    
    
@router.get("/me")
def get_me(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "auth_provider": user.auth_provider,
        "is_verified": user.is_verified,
    }