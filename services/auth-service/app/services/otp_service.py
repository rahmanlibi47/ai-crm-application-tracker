import random
from datetime import datetime, timedelta


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def save_login_otp(db, user, otp):
    user.otp_code = otp
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def verify_login_otp(db, user, otp):
    if not user.otp_code:
        return False

    if user.otp_code != otp:
        return False

    if user.otp_expires_at < datetime.utcnow():
        return False

    user.otp_code = None
    user.otp_expires_at = None

    db.add(user)
    db.commit()

    return True