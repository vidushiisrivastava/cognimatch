
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# PERSONA GENERATOR

def generate_persona(answers: list) -> dict:
    prompt = f"""
    You are an occupational psychologist specializing in neurodiversity.
    Based on these 6 working style answers, generate a professional
    neurodivergent candidate persona.

    ANSWERS:
    1. Task start preference: {answers[0]}
    2. Best work environment: {answers[1]}
    3. Feedback preference: {answers[2]}
    4. Deadline relationship: {answers[3]}
    5. Meeting style: {answers[4]}
    6. Ideal team: {answers[5]}

    Return ONLY a JSON object with exactly this structure, no extra text:
    {{
        "persona_name": "professional cognitive style label",
        "working_style_summary": "2 sentence summary",
        "strengths": ["strength 1", "strength 2", "strength 3"],
        "ideal_environment": ["factor 1", "factor 2", "factor 3"],
        "accommodation_requests": ["accommodation 1", "accommodation 2"],
        "employer_message": "2 sentence message for employers"
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# BIAS SCANNER
def scan_bias(job_description: str) -> dict:
    prompt = f"""
    You are an inclusive hiring expert. Analyze this job description
    for language that excludes neurodivergent candidates.

    Job Description: {job_description}

    Return ONLY a JSON object with exactly this structure, no extra text:
    {{
        "bias_score": 0,
        "summary": "one sentence summary",
        "flagged_phrases": [
            {{"phrase": "word", "reason": "why exclusionary", "replacement": "better word"}}
        ],
        "rewritten_jd": "full rewritten inclusive version"
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)

# CULTURE REPORT

def generate_culture_report(company_description: str) -> dict:
    prompt = f"""
    You are an inclusion expert analyzing workplace culture for neurodivergent employees.
    
    Score the company description from 0-100 where:
    - 80-100 = Highly inclusive (remote, async, accommodations, flexible)
    - 60-79  = Moderately inclusive (some flexibility, some support)
    - 40-59  = Partially inclusive (basic policies only)
    - 0-39   = Low inclusion (rigid, no accommodations mentioned)

    Company description: {company_description}

    Return ONLY a valid JSON object with exactly this structure.
    All array items must be plain strings only.
    Do not include markdown, backticks, or extra text:
    {{
        "inclusion_score": 85,
        "summary": "one sentence overall assessment",
        "strengths": [
            "first strength as a plain sentence",
            "second strength as a plain sentence",
            "third strength as a plain sentence"
        ],
        "gaps": [
            "first gap as a plain sentence",
            "second gap as a plain sentence"
        ],
        "recommendations": [
            "first recommendation as a plain sentence",
            "second recommendation as a plain sentence",
            "third recommendation as a plain sentence"
        ]
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# MATCH EXPLANATION

def generate_match_explanation(
    match_percentage: float,
    match_label: str,
    compiled_profile: str,
    job_description: str
) -> dict:
    prompt = f"""
    A candidate has a {match_percentage}% working style match with this job.
    Match level: {match_label}

    Candidate profile: {compiled_profile[:500]}
    Job description: {job_description[:500]}

    Return ONLY a JSON object with exactly this structure, no extra text:
    {{
        "explanation": "3 sentence explanation of this match score",
        "strengths": ["alignment point 1", "alignment point 2", "alignment point 3"],
        "risks": ["mismatch risk 1", "mismatch risk 2"]
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)