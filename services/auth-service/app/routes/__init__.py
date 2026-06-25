from fastapi import APIRouter

from app.routes.auth_routes import router as auth_router
from app.routes.google_routes import router as google_router
from app.routes.otp_routes import router as otp_router
from app.routes.user_routes import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(google_router)
router.include_router(otp_router)
router.include_router(user_router)