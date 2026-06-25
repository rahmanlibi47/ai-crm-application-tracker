import time

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.auth import hash_password, verify_password, create_access_token
from app.crud import get_user_by_email
from app.redis_client import redis_client

from app.services.otp_service import generate_otp, save_login_otp
from app.services.email_service import send_login_otp_background

from app.routes.otp_routes import check_otp_limits


router = APIRouter()


@router.post("/signup", response_model=None)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
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


@router.get("/me")
def get_me(
    request: Request,
    db: Session = Depends(get_db)
):
    start = time.perf_counter()

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

    elapsed = (time.perf_counter() - start) * 1000

    print(f"/me completed in {elapsed:.2f} ms")

    return JSONResponse(
        content={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "auth_provider": user.auth_provider,
            "is_verified": user.is_verified,
        },
        headers={
            "X-Response-Time": f"{elapsed:.2f}ms"
        }
    )