import json
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


def save_candidate_persona(persona_json_path: str, user_id: str = None):
    with open(persona_json_path) as f:
        data = json.load(f)

    row = {
        "user_id": user_id,
        "name": data.get("name", "Unknown"),
        "persona": data.get("persona", {}),
        "working_style": data.get("working_style", {}),
    }
    result = supabase.table("candidates").insert(row).execute()
    print("Saved candidate:", result.data)
    return result.data


def save_match_score(match_json_path: str, candidate_id: str, org_id: str):
    with open(match_json_path) as f:
        data = json.load(f)

    row = {
        "candidate_id": candidate_id,
        "org_id": org_id,
        "score": data.get("match_score", 0),
        "breakdown": data.get("breakdown", {}),
    }
    result = supabase.table("match_scores").insert(row).execute()
    print("Saved match score:", result.data)
    return result.data


def save_bias_scan(bias_json_path: str, org_id: str, job_description: str):
    with open(bias_json_path) as f:
        data = json.load(f)

    row = {
        "org_id": org_id,
        "job_description": job_description,
        "flagged_words": data.get("flagged_terms", []),
        "risk_score": data.get("bias_score", 0),
        "suggestions": data.get("suggestions", []),
    }
    result = supabase.table("bias_scans").insert(row).execute()
    print("Saved bias scan:", result.data)
    return result.data


def save_culture_report(report_json_path: str, org_id: str):
    with open(report_json_path) as f:
        data = json.load(f)

    row = {
        "org_id": org_id,
        "report": data,
    }
    result = supabase.table("culture_reports").insert(row).execute()
    print("Saved culture report:", result.data)
    return result.data


def get_all_candidates():
    result = supabase.table("candidates").select("*").execute()
    return result.data


def get_matches_for_org(org_id: str):
    result = supabase.table("match_scores").select("*").eq("org_id", org_id).execute()
    return result.data


def get_bias_scans_for_org(org_id: str):
    result = supabase.table("bias_scans").select("*").eq("org_id", org_id).execute()
    return result.data


if __name__ == "__main__":
    print("Testing Supabase connection...")
    candidates = get_all_candidates()
    print(f"Connected! Found {len(candidates)} candidates in database.")
    print("db.py is working correctly.")