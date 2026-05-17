def calculate_match(candidate, company) -> dict:
    score = 0

    if candidate.communication_style == company.communication_style:
        score += 25

    if candidate.work_preference == company.remote_policy:
        score += 25

    if candidate.focus_style == "deep_focus" and company.work_pace == "steady":
        score += 25
    elif candidate.focus_style == "collaborative" and company.work_pace == "fast":
        score += 25

    if candidate.energy_pattern and company.meeting_frequency:
        score += 25

    if score >= 75:
        risk = "Low"
    elif score >= 50:
        risk = "Moderate"
    else:
        risk = "High"

    return {"match_score": score, "risk_level": risk}
