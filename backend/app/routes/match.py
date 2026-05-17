from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.candidate import CandidateProfile
from app.models.company import CompanyProfile
from app.models.match import Match
from app.services.matching_service import calculate_match

router = APIRouter(prefix="/match", tags=["Matching"])


@router.post("/run")
def run_match(
    candidate_user_id: int, company_user_id: int, db: Session = Depends(get_db)
):
    candidate = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.user_id == candidate_user_id)
        .first()
    )
    company = (
        db.query(CompanyProfile)
        .filter(CompanyProfile.user_id == company_user_id)
        .first()
    )

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate profile not found")
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found")

    result = calculate_match(candidate, company)

    match = Match(
        candidate_id=candidate_user_id,
        company_id=company_user_id,
        match_score=result["match_score"],
        risk_level=result["risk_level"],
    )
    db.add(match)
    db.commit()

    return {
        "candidate_id": candidate_user_id,
        "company_id": company_user_id,
        "match_score": result["match_score"],
        "risk_level": result["risk_level"],
        "verdict": "Strong Fit"
        if result["match_score"] >= 75
        else "Moderate Fit"
        if result["match_score"] >= 50
        else "Possible Burnout Risk",
    }
