from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from app.db.database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, nullable=False, index=True)
    
    company_name = Column(String, nullable=False)
    
    job_title = Column(String, nullable=False)
    
    status = Column(String, nullable=False, default="applied")
    
    job_url = Column(String, nullable=True)
    
    notes = Column(String, nullable=True)
    
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )