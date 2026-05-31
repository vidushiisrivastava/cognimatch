from sentence_transformers import SentenceTransformer, util

WEIGHTS = {
    "work_pace":      0.20,   # 20% — how candidate handles pace + deadlines
    "environment":    0.15,   # 15% — physical/remote workspace needs
    "structure":      0.15,   # 15% — how much clarity/structure they need
    "communication":  0.15,   # 15% — written vs verbal preference
    "burnout":        0.20,   # 20% — stress tolerance + burnout sensitivity
    "collaboration":  0.15,   # 15% — solo vs team preference
}


PSYCHOMETRIC_MATRIX = {
    "q1": {
        "Detailed written brief upfront": {
            "db_slug": "deep_focus",
            "weight_category": "structure",
            "ai_payload": "Candidate requires high structural certainty and explicit written documentation before starting work. Thrives on clear unambiguous requirements and independent deep execution."
        },
        "Quick verbal overview then figure it out": {
            "db_slug": "collaborative",
            "weight_category": "structure",
            "ai_payload": "Candidate prefers high autonomy paired with brief verbal alignment. Learns dynamically through rapid execution and adapts quickly without rigid blueprints."
        },
        "Collaborative planning session": {
            "db_slug": "collaborative",
            "weight_category": "collaboration",
            "ai_payload": "Candidate excels in highly interactive synchronous environments. Maximizes output through active collective brainstorming and real-time peer alignment."
        },
        "Just dive in and learn as I go": {
            "db_slug": "deep_focus",
            "weight_category": "structure",
            "ai_payload": "Candidate possesses exceptional tolerance for ambiguity. Highly experimental and action-oriented, flourishes in unstructured environments."
        }
    },
    "q2": {
        "Quiet, private, minimal interruptions": {
            "db_slug": "quiet",
            "weight_category": "environment",
            "ai_payload": "Candidate requires deeply isolated environments optimized for sensory containment. Maximizes productivity when protected from context-switching and office noise."
        },
        "Open, social, collaborative buzz": {
            "db_slug": "open_office",
            "weight_category": "environment",
            "ai_payload": "Candidate draws energy from high-stimulation interactive environments. Thrives amidst organic team chats and verbal accessibility."
        },
        "Flexible — I switch between both": {
            "db_slug": "hybrid",
            "weight_category": "environment",
            "ai_payload": "Candidate relies on adaptive workspace layout. Needs dynamic scheduling that transitions between collaborative huddles and quiet individual phases."
        },
        "Remote, fully async": {
            "db_slug": "remote",
            "weight_category": "environment",
            "ai_payload": "Candidate operates optimally with total spatial and temporal control. Excels in remote environments with written tracking and completely independent schedules."
        }
    },
    "q3": {
        "I need clear requirements first": {
            "db_slug": "ambiguity",
            "weight_category": "structure",
            "ai_payload": "Candidate delivers peak performance within deterministic frameworks. Requires bounded task scope and explicit parameters before starting development."
        },
        "I thrive with creative freedom": {
            "db_slug": "creative",
            "weight_category": "structure",
            "ai_payload": "Candidate functions exceptionally well in highly fluid situations. Views missing specifications as opportunity for innovative design choices."
        },
        "I ask lots of clarifying questions": {
            "db_slug": "sync",
            "weight_category": "communication",
            "ai_payload": "Candidate actively mitigates risks by initiating upstream discovery. Relies on verbal loops and collaborative dialogue to resolve edge cases."
        },
        "I make assumptions and adjust later": {
            "db_slug": "fast",
            "weight_category": "work_pace",
            "ai_payload": "Candidate champions high-velocity prototype iterations. Willing to deploy imperfect baseline rapidly and refine based on real-time feedback."
        }
    },
    "q4": {
        "Written first — I think in text": {
            "db_slug": "written",
            "weight_category": "communication",
            "ai_payload": "Candidate treats written text as core cognitive medium. Relies on comprehensive documentation and well-documented pull requests to transmit logic."
        },
        "Visual — diagrams and whiteboards": {
            "db_slug": "verbal",
            "weight_category": "communication",
            "ai_payload": "Candidate processes complex dependencies spatially. Excels using interactive whiteboards and system diagrams to map layout dependencies."
        },
        "Verbal — I process by talking": {
            "db_slug": "verbal",
            "weight_category": "communication",
            "ai_payload": "Candidate generates clarity by thinking aloud. Benefits significantly from live audio channels and talk-centric check-ins."
        },
        "Direct and concise, no small talk": {
            "db_slug": "written",
            "weight_category": "communication",
            "ai_payload": "Candidate communicates with absolute operational precision. Cuts social overhead, preferring dense technical logs and zero-noise metrics."
        }
    },
    "q5": {
        "Focus deeply on one thing at a time": {
            "db_slug": "steady",
            "weight_category": "burnout",
            "ai_payload": "Candidate requires strict single-threaded execution under pressure. Protects cognitive load by finishing one critical module before opening subsequent tasks."
        },
        "Context-switch rapidly between tasks": {
            "db_slug": "fast",
            "weight_category": "work_pace",
            "ai_payload": "Candidate maintains cognitive fluidity during rapid delivery cycles. Capable of juggling hotfixes and multiple development threads simultaneously."
        },
        "Need to step back and re-prioritize": {
            "db_slug": "steady",
            "weight_category": "burnout",
            "ai_payload": "Candidate manages delivery stress via structured triage. Responds to deadlines by analyzing risks and organizing architectural priorities."
        },
        "Thrive — pressure helps me focus": {
            "db_slug": "fast",
            "weight_category": "work_pace",
            "ai_payload": "Candidate enters intentional hyperfocused flow state under tight timelines. High urgency serves as positive catalyst for accelerated output."
        }
    }
}

def get_match_tier(score: float) -> str:
    """
    Converts a numeric score into a human-readable match label.

    85-100 → Strong Fit    (shown at top, recommend strongly)
    65-84  → Good Fit      (recommend with insight notes)
    40-64  → Partial Fit   (show with risk alerts)
    0-39   → Poor Fit      (do not show to either party)
    """
    if score >= 85:
        return "Strong Fit"
    elif score >= 65:
        return "Good Fit"
    elif score >= 40:
        return "Partial Fit"
    else:
        return "Poor Fit"



def detect_burnout(db_slugs: dict) -> tuple:
    """
    Only flags burnout when candidate is in a HIGH PRESSURE
    environment that conflicts with their needs.
    Remote + structured = safe, NOT burnout risk.
    """
    energy = db_slugs.get("energy_pattern", "")
    environment = db_slugs.get("work_preference", "")
    stress = db_slugs.get("stress_triggers", "")

    # Only flag burnout if:
    # Candidate needs quiet BUT is in open office AND fast paced
    if (energy == "steady" and 
        environment == "open_office" and 
        stress == "ambiguity"):
        return True, "Candidate needs quiet structured environment but role is open and fast-paced"

    # Flag if candidate hates ambiguity AND company is fast paced
    if (stress == "ambiguity" and 
        energy == "fast" and 
        environment == "open_office"):
        return True, "Candidate sensitive to ambiguity in high stimulation environment"

    return False, None



def check_inclusion_badge(inclusion_score: float, bias_score: float) -> tuple:
    """
    Checks if a company qualifies for the Verified Inclusion Badge.

    inclusion_score: from Vidushi's culture_report() — 0 to 100
    bias_score:      from Vidushi's bias_scanner()   — 0 to 100

    Returns (True, message) or (False, message)
    """
    if inclusion_score >= 80 and bias_score <= 20:
        return True, "✅ Qualifies for Verified Inclusion Badge"
    elif inclusion_score >= 80 and bias_score > 20:
        return False, "Inclusion score is strong but JD bias is too high. Rewrite job descriptions to qualify."
    elif inclusion_score < 80 and bias_score <= 20:
        return False, "JD language is inclusive but culture score needs improvement. Review gaps in culture report."
    else:
        return False, "Both inclusion score and JD bias need improvement before qualifying."



def calculate_hybrid_score(frontend_answers: list, job_desc: str) -> dict:
    """
    Called when frontend POSTs to /api/match

    frontend_answers: list of 5 strings (exact options from match/page.tsx)
    job_desc:         job description text pasted by user

    Returns:
    {
        "database_slugs":    {...},  → save to candidate_profiles table
        "match_percentage":  float,  → shown as big number on frontend
        "match_label":       str,    → shown below the number
        "explanation":       str,    → "What this means" section
        "strengths":         list,   → green strengths section
        "risks":             list,   → red mismatch risks section
        "burnout_risk":      bool,   → internal flag
        "burnout_reason":    str     → shown in risks if True
    }
    """

    # Step 1 — Look up each answer in the psychometric matrix
    q1 = PSYCHOMETRIC_MATRIX["q1"].get(
        frontend_answers[0],
        {"db_slug": "unknown", "weight_category": "structure", "ai_payload": ""}
    )
    q2 = PSYCHOMETRIC_MATRIX["q2"].get(
        frontend_answers[1],
        {"db_slug": "unknown", "weight_category": "environment", "ai_payload": ""}
    )
    q3 = PSYCHOMETRIC_MATRIX["q3"].get(
        frontend_answers[2],
        {"db_slug": "unknown", "weight_category": "structure", "ai_payload": ""}
    )
    q4 = PSYCHOMETRIC_MATRIX["q4"].get(
        frontend_answers[3],
        {"db_slug": "unknown", "weight_category": "communication", "ai_payload": ""}
    )
    q5 = PSYCHOMETRIC_MATRIX["q5"].get(
        frontend_answers[4],
        {"db_slug": "unknown", "weight_category": "burnout", "ai_payload": ""}
    )

    # Step 2 — Extract database slugs
    database_slugs = {
        "focus_style":          q1["db_slug"],   # deep_focus / collaborative
        "work_preference":      q2["db_slug"],   # quiet / remote / hybrid / open_office
        "stress_triggers":      q3["db_slug"],   # ambiguity / creative / sync / fast
        "communication_style":  q4["db_slug"],   # written / verbal
        "energy_pattern":       q5["db_slug"],   # steady / fast
    }

    # Step 3 — Compile AI text profile from all answer payloads
    compiled_profile = " ".join([
        q1["ai_payload"],
        q2["ai_payload"],
        q3["ai_payload"],
        q4["ai_payload"],
        q5["ai_payload"],
    ]).strip()

    # Step 4 — Compute vector similarity using sentence transformers
    print("Running vector similarity match...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    candidate_embedding = model.encode(compiled_profile, convert_to_tensor=True)
    job_embedding = model.encode(job_desc, convert_to_tensor=True)
    similarity = util.cos_sim(candidate_embedding, job_embedding)
    raw_score = float(similarity[0][0])

    # Step 5 — Apply weighted category boost
    # Count how many answers fall into each weight category
    category_hits = {cat: 0 for cat in WEIGHTS}
    for q in [q1, q2, q3, q4, q5]:
        cat = q.get("weight_category", "")
        if cat in category_hits:
            category_hits[cat] += 1

    # Apply boost: each answer in a heavy category adds weight
    weighted_boost = sum(
        WEIGHTS.get(cat, 0) * hits * 0.1
        for cat, hits in category_hits.items()
    )
    # Maps 0.0->50%, 0.5->75%, 1.0->100%
    normalized_score = 50 + (raw_score * 50)
    
    final_score = round(
        max(0.0, min(100.0, normalized_score + weighted_boost)), 1
    )

    # Step 6 — Get match tier and label
    tier = get_match_tier(final_score)

    if final_score >= 85:
        match_label = "✅ Strong Fit"
    elif final_score >= 65:
        match_label = "⚠️ Good Fit"
    elif final_score >= 40:
        match_label = "🟠 Partial Fit"
    else:
        match_label = "❌ Poor Fit"

    # Step 7 — Detect burnout risk
    burnout_risk, burnout_reason = detect_burnout(database_slugs)

    # Step 8 — Build strengths and risks lists
    strengths = []
    risks = []

    if database_slugs["communication_style"] == "written":
        strengths.append("Strong written communication — great for async teams")
    if database_slugs["energy_pattern"] == "steady":
        strengths.append("Consistent steady output — reliable in structured roles")
    if database_slugs["focus_style"] == "deep_focus":
        strengths.append("Deep focus capability — excellent for complex tasks")
    if database_slugs["work_preference"] == "remote":
        strengths.append("Remote-ready — thrives without in-person supervision")
    if database_slugs["stress_triggers"] == "creative":
        strengths.append("Embraces creative freedom — self-directed and innovative")

    if burnout_risk:
        risks.append(f"⚠️ Burnout risk: {burnout_reason}")
    if database_slugs["energy_pattern"] == "steady" and "fast" in job_desc.lower():
        risks.append("Role may require faster pace than candidate prefers")
    if database_slugs["communication_style"] == "written" and "verbal" in job_desc.lower():
        risks.append("Role emphasizes verbal communication — candidate prefers written")
    if database_slugs["work_preference"] == "quiet" and "open" in job_desc.lower():
        risks.append("Open office environment may conflict with need for quiet workspace")

    # Fallback strengths/risks if none generated
    if not strengths:
        strengths = ["Working style assessed — see match score for compatibility"]
    if not risks and final_score < 65:
        risks = ["Some working style mismatches detected — review role requirements"]

    # Step 9 — Build explanation
    explanation = (
        f"Based on your working style preferences, you have a {final_score}% "
        f"compatibility with this role. Your profile shows a {tier} based on "
        f"communication style, environment needs, and deadline handling. "
        f"{'Burnout risk has been flagged — review the risks below.' if burnout_risk else 'No significant burnout risk detected.'}"
    )

    return {
        "database_slugs":   database_slugs,
        "compiled_profile": compiled_profile,
        "match_percentage": final_score,
        "match_label":      match_label,
        "match_tier":       tier,
        "explanation":      explanation,
        "strengths":        strengths,
        "risks":            risks,
        "burnout_risk":     burnout_risk,
        "burnout_reason":   burnout_reason,
    }



def score_work_pace(candidate, company) -> float:
    """Compares candidate's energy pattern with company's work pace"""
    if candidate.energy_pattern == "steady" and company.work_pace == "steady":
        return 100.0
    elif candidate.energy_pattern == "fast" and company.work_pace == "fast":
        return 100.0
    elif candidate.energy_pattern == "fast" and company.work_pace == "steady":
        return 60.0
    elif candidate.energy_pattern == "steady" and company.work_pace == "fast":
        return 25.0  # High burnout risk combination
    return 50.0


def score_environment(candidate, company) -> float:
    """Compares candidate's workspace needs with company's environment"""
    if candidate.work_preference == "quiet" and company.environment_type == "quiet":
        return 100.0
    elif candidate.work_preference == "remote" and company.remote_policy == "remote":
        return 100.0
    elif candidate.work_preference == "hybrid" and company.remote_policy == "hybrid":
        return 100.0
    elif candidate.work_preference == "remote" and company.remote_policy == "hybrid":
        return 70.0
    elif candidate.work_preference == "quiet" and company.environment_type == "open_office":
        return 20.0  # Major mismatch
    elif candidate.work_preference == "open_office" and company.environment_type == "open_office":
        return 100.0
    return 50.0


def score_structure(candidate, company) -> float:
    """Compares candidate's structure needs with company's pace"""
    if candidate.stress_triggers == "ambiguity" and company.work_pace == "steady":
        return 90.0
    elif candidate.stress_triggers == "ambiguity" and company.work_pace == "fast":
        return 25.0  # Ambiguity-sensitive in fast company = mismatch
    elif candidate.stress_triggers == "creative" and company.work_pace == "fast":
        return 85.0
    elif candidate.stress_triggers == "creative" and company.work_pace == "steady":
        return 65.0
    elif candidate.stress_triggers == "sync":
        return 70.0
    return 50.0


def score_communication(candidate, company) -> float:
    """Compares candidate's communication style with company's style"""
    if candidate.communication_style == "written" and company.communication_style == "async":
        return 100.0
    elif candidate.communication_style == "verbal" and company.communication_style == "sync":
        return 100.0
    elif candidate.communication_style == "written" and company.communication_style == "sync":
        return 40.0  # Mismatch — written person in sync company
    elif candidate.communication_style == "verbal" and company.communication_style == "async":
        return 45.0  # Mismatch — verbal person in async company
    return 55.0


def score_burnout(candidate, company) -> float:
    """
    Evaluates burnout risk based on energy pattern vs meeting frequency.
    Low score = higher burnout risk.
    """
    if candidate.energy_pattern == "steady" and company.meeting_frequency == "weekly":
        return 90.0  # Steady person with few meetings = safe
    elif candidate.energy_pattern == "fast" and company.meeting_frequency == "daily":
        return 75.0  # High energy person handles daily meetings well
    elif candidate.energy_pattern == "steady" and company.meeting_frequency == "daily":
        return 25.0  # Burnout risk: steady person with daily meetings
    elif candidate.energy_pattern == "fast" and company.meeting_frequency == "weekly":
        return 70.0  # Fast person with few meetings — may get bored
    return 50.0


def score_collaboration(candidate, company) -> float:
    """Compares candidate's focus style with company's work pace"""
    if candidate.focus_style == "deep_focus" and company.work_pace == "steady":
        return 100.0
    elif candidate.focus_style == "collaborative" and company.work_pace == "fast":
        return 90.0
    elif candidate.focus_style == "deep_focus" and company.work_pace == "fast":
        return 45.0  # Deep focus person in fast company = friction
    elif candidate.focus_style == "collaborative" and company.work_pace == "steady":
        return 65.0
    return 50.0


def calculate_match(candidate, company) -> dict:

    # Score each category individually
    category_scores = {
        "work_pace":     score_work_pace(candidate, company),
        "environment":   score_environment(candidate, company),
        "structure":     score_structure(candidate, company),
        "communication": score_communication(candidate, company),
        "burnout":       score_burnout(candidate, company),
        "collaboration": score_collaboration(candidate, company),
    }

    # Apply weights to get final score
    final_score = round(
        sum(category_scores[cat] * WEIGHTS[cat] for cat in WEIGHTS), 1
    )

    # Get match tier
    tier = get_match_tier(final_score)

    # Build db_slugs from candidate object for burnout check
    db_slugs = {
        "focus_style":          candidate.focus_style,
        "work_preference":      candidate.work_preference,
        "stress_triggers":      candidate.stress_triggers,
        "communication_style":  candidate.communication_style,
        "energy_pattern":       candidate.energy_pattern,
    }
    burnout_risk, burnout_reason = detect_burnout(db_slugs)

    # Set risk level
    if burnout_risk or final_score < 40:
        risk_level = "High"
    elif final_score < 65:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {
        "match_score":      final_score,
        "match_tier":       tier,
        "risk_level":       risk_level,
        "burnout_risk":     burnout_risk,
        "burnout_reason":   burnout_reason,
        "category_scores":  category_scores,
    }
