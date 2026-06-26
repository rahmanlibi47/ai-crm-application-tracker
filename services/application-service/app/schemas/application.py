from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class JobApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    status: str = "applied"
    job_url: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    job_title: str
    status: str
    job_url: Optional[str]
    notes: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class Job(BaseModel):
    id: str
    source: str
    title: str
    company: str
    location: str
    description: str = ""
    salary: str | None = None
    apply_url: str
    company_logo: str | None = None
    tags: list[str] = Field(default_factory=list)
    posted_at: datetime | None = None