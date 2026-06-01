from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.services.ai_service import (
    generate_persona,
    scan_bias,
    generate_culture_report,
    generate_match_explanation,
)
from app.services.matching_service import (
    calculate_hybrid_score,
    check_inclusion_badge,
)

router = APIRouter(prefix="/api", tags=["API"])


class PersonaRequest(BaseModel):
    answers: List[str]


class MatchRequest(BaseModel):
    answers: List[str]
    job_description: str


class BiasScanRequest(BaseModel):
    job_description: str


class CultureRequest(BaseModel):
    company_description: str


@router.post("/persona")
async def persona_endpoint(data: PersonaRequest):
    if len(data.answers) < 6:
        return {"error": f"Expected 6 answers, got {len(data.answers)}"}

    result = generate_persona(data.answers)

    return {
        "persona_name":           result.get("persona_name", "Working Style Profile"),
        "working_style_summary":  result.get("working_style_summary", ""),
        "strengths":              result.get("strengths", []),
        "ideal_environment":      result.get("ideal_environment", []),
        "accommodation_requests": result.get("accommodation_requests", []),
        "employer_message":       result.get("employer_message", ""),
    }


@router.post("/match")
async def match_endpoint(data: MatchRequest):
    if len(data.answers) < 5:
        return {"error": f"Expected 5 answers, got {len(data.answers)}"}

    score_result = calculate_hybrid_score(data.answers, data.job_description)

    try:
        ai_result = generate_match_explanation(
            match_percentage=score_result["match_percentage"],
            match_label=score_result["match_label"],
            compiled_profile=score_result.get("compiled_profile", ""),
            job_description=data.job_description,
        )
        explanation = ai_result.get("explanation", score_result["explanation"])
        strengths   = ai_result.get("strengths", score_result["strengths"])
        risks       = ai_result.get("risks", score_result["risks"])
    except Exception:
        explanation = score_result["explanation"]
        strengths   = score_result["strengths"]
        risks       = score_result["risks"]

    if score_result.get("burnout_risk") and score_result.get("burnout_reason"):
        if score_result["burnout_reason"] not in risks:
            risks.insert(0, f"Burnout Risk: {score_result['burnout_reason']}")

    return {
        "match_percentage": score_result["match_percentage"],
        "match_label":      score_result["match_label"],
        "explanation":      explanation,
        "strengths":        strengths,
        "risks":            risks,
        "database_slugs":   score_result.get("database_slugs", {}),
    }



@router.post("/bias-scan")
async def bias_scan_endpoint(data: BiasScanRequest):
    if not data.job_description.strip():
        return {"error": "Job description cannot be empty"}

    result = scan_bias(data.job_description)

    return {
        "bias_score":      result.get("bias_score", 0),
        "summary":         result.get("summary", ""),
        "flagged_phrases": result.get("flagged_phrases", []),
        "rewritten_jd":    result.get("rewritten_jd", ""),
    }



@router.post("/culture")
async def culture_endpoint(data: CultureRequest):
    if not data.company_description.strip():
        return {"error": "Company description cannot be empty"}

    result = generate_culture_report(data.company_description)
    inclusion_score = result.get("inclusion_score", 0)

    badge_qualified, badge_message = check_inclusion_badge(
        inclusion_score=inclusion_score,
        bias_score=50
    )

    return {
        "inclusion_score":  inclusion_score,
        "summary":          result.get("summary", ""),
        "strengths":        result.get("strengths", []),
        "gaps":             result.get("gaps", []),
        "recommendations":  result.get("recommendations", []),
        "inclusion_badge":  badge_qualified,
        "badge_message":    badge_message,
    }