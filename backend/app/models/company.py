from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class CompanyProfile(Base):
    __tablename__ = "company_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    company_name = Column(String)
    communication_style = Column(String)  # e.g. "async" or "sync"
    meeting_frequency = Column(String)  # e.g. "daily" or "weekly"
    work_pace = Column(String)  # e.g. "fast" or "steady"
    environment_type = Column(String)  # e.g. "open_office" or "quiet"
    remote_policy = Column(String)  # e.g. "remote" or "hybrid"
