from sqlalchemy import Column, Integer, Float, ForeignKey, String
from app.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("users.id"))
    match_score = Column(Float)
    risk_level = Column(String)  # "Low", "Moderate", "High"
