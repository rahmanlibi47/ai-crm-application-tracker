from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.schemas import UserResponse
from app.schemas import UserLogin, AuthResponse
from app.schemas import TokenResponse

from app.auth import hash_password, verify_password, decode_access_token
from app.auth import create_access_token

from app.auth import oauth2_scheme


from app.crud import get_user_by_email
from app.crud import get_user_by_id

from app.auth_service import generate_auth_response

router = APIRouter()

@router.post(
    "/signup",
    response_model=AuthResponse
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
        full_name = user.full_name
    )
    
    db.add(new_user)
    
    db.commit()
    
    db.refresh(new_user)
    
    return generate_auth_response(new_user)


@router.post(
    "/login",
    response_model=AuthResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    
    existing_user = get_user_by_email(db, user.email)
    
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
        
    password_valid = verify_password(
        user.password,
        existing_user.hashed_password
    )
    
    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
        
    access_token = create_access_token(
        data={
            "sub": existing_user.email,
            "user_id": existing_user.id
        }
    )
    
    return generate_auth_response(existing_user)
    
@router.get("/me", response_model=UserResponse)
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