from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.models import JobApplication
from app.schemas.application import JobApplicationCreate

def create_job_application(
    db: Session,
    application: JobApplicationCreate,
    user_id: int
):
    existing_application = (
        db.query(JobApplication)
        .filter(
            JobApplication.user_id == user_id,
            JobApplication.company_name == application.company_name,
            JobApplication.job_title == application.job_title
        )
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="Application already exists"
        )

    db_application = JobApplication(
        user_id=user_id,
        company_name=application.company_name,
        job_title=application.job_title,
        status=application.status,
        job_url=application.job_url,
        notes=application.notes
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


def get_user_applications(
    db: Session,
    user_id: int
):
    return (
        db.query(JobApplication)
        .filter(JobApplication.user_id == user_id)
        .order_by(JobApplication.created_at.desc())
        .all()
    )