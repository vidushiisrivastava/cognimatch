from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CandidateProfileCreate(BaseModel):
    focus_style:          str
    communication_style:  str
    work_preference:      str
    stress_triggers:      str
    energy_pattern:       str
    time_spent_seconds:   Optional[int] = None

class CandidateProfileOut(CandidateProfileCreate):
    id:              int
    user_id:         int
    profile_version: Optional[int] = 1
    last_updated:    Optional[datetime] = None
    raw_responses:   Optional[str] = None

    class Config:
        from_attributes = True

class AIProfileUpdate(BaseModel):
    persona_data: dict
    time_spent_seconds: Optional[int] = None
