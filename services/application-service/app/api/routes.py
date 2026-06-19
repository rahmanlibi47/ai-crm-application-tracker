from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.application import JobApplicationCreate
from app.schemas.application import JobApplicationResponse
from app.crud.application import create_job_application
from app.crud.application import get_user_applications
from app.dependencies.auth import get_current_user_id

from app.dependencies.rate_limit import check_rate_limit


router = APIRouter()


@router.post(
    "/applications",
    response_model=JobApplicationResponse
)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    rate_limit_key = f"user:{user_id}:create_application"

    check_rate_limit(
        key=rate_limit_key,
        limit=5,
        window_seconds=60
    )
    
    

    return create_job_application(
        db=db,
        application=application,
        user_id=user_id
    )


@router.get(
    "/applications",
    response_model=List[JobApplicationResponse]
)
def list_applications(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return get_user_applications(
        db=db,
        user_id=user_id
    )