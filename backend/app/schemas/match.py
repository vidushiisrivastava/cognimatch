from pydantic import BaseModel


class MatchResult(BaseModel):
    candidate_id: int
    company_id: int
    match_score: float
    risk_level: str

    class Config:
        from_attributes = True
