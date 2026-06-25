from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import VerifyOtpRequest, ResendOtpRequest
from app.auth import create_access_token
from app.crud import get_user_by_email
from app.redis_client import redis_client

from app.services.otp_service import (
    generate_otp,
    verify_login_otp as verify_login_otp_service,
    save_login_otp,
)
from app.services.email_service import send_login_otp_background


router = APIRouter()

OTP_DAILY_LIMIT = 3
OTP_IP_DAILY_LIMIT = 15
OTP_COOLDOWN_SECONDS = 60


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
        secure=True,
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