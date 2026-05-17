from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json
from app.database import get_db
from app.models.candidate import CandidateProfile
from app.schemas.candidate import CandidateProfileCreate, CandidateProfileOut, AIProfileUpdate

router = APIRouter(prefix="/candidate", tags=["Candidate"])

@router.post("/assessment", response_model=CandidateProfileOut)
def submit_assessment(data: CandidateProfileCreate, user_id: int, db: Session = Depends(get_db)):
    existing = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()
    if existing:
        for key, value in data.dict().items():
            setattr(existing, key, value)
        existing.last_updated = datetime.now()
        db.commit()
        db.refresh(existing)
        return existing
    profile = CandidateProfile(user_id=user_id, **data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/profile/{user_id}", response_model=CandidateProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/ai-profile")
def save_ai_profile(user_id: int, data: AIProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found")
    profile.raw_responses = json.dumps(data.persona_data)
    profile.last_updated = datetime.now()
    profile.profile_version += 1
    if data.time_spent_seconds:
        profile.time_spent_seconds = data.time_spent_seconds
    db.commit()
    db.refresh(profile)
    return {"message": "AI profile saved", "profile_version": profile.profile_version}
