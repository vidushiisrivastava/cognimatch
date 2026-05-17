from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.company import CompanyProfile
from app.schemas.company import CompanyProfileCreate, CompanyProfileOut

router = APIRouter(prefix="/company", tags=["Company"])


@router.post("/culture-form", response_model=CompanyProfileOut)
def submit_culture_form(
    data: CompanyProfileCreate, user_id: int, db: Session = Depends(get_db)
):
    existing = (
        db.query(CompanyProfile).filter(CompanyProfile.user_id == user_id).first()
    )
    if existing:
        for key, value in data.dict().items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing

    profile = CompanyProfile(user_id=user_id, **data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/profile/{user_id}", response_model=CompanyProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = (
        db.query(CompanyProfile)
        .filter(CompanyProfile.user_id == user_id == user_id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Company profile not found")
    return profile
