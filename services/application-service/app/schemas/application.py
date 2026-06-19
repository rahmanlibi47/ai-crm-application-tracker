from datetime import datetime
from typing import Optional

from pydantic import BaseModel

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