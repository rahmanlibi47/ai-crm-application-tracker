from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    auth_provider = Column(String, default="local")

    otp_code = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)