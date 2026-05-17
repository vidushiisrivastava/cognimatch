from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    focus_style = Column(String)  # e.g. "deep_focus" or "collaborative"
    communication_style = Column(String)  # e.g. "written" or "verbal"
    work_preference = Column(String)  # e.g. "remote" or "in_person"
    stress_triggers = Column(String)  # e.g. "noise" or "ambiguity"
    energy_pattern = Column(String)  # e.g. "morning" or "evening"
