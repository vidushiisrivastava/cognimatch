from groq import Groq
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def save_output(feature_name, data):
    filename = f"output_{feature_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Output saved to {filename}")

def culture_report():
    print("\n=== Culture Intelligence Report ===\n")
    company = input("Describe the company: ")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
            You are an inclusion expert. Based on this company: {company}
            Return ONLY a JSON object with exactly this structure, no extra text:
            {{
                "inclusion_score": 0,
                "score_explanation": "explanation here",
                "strengths": [
                    {{"point": "strength 1", "detail": "explanation"}},
                    {{"point": "strength 2", "detail": "explanation"}},
                    {{"point": "strength 3", "detail": "explanation"}}
                ],
                "gaps": [
                    {{"point": "gap 1", "detail": "explanation"}},
                    {{"point": "gap 2", "detail": "explanation"}},
                    {{"point": "gap 3", "detail": "explanation"}}
                ],
                "recommendations": [
                    "recommendation 1",
                    "recommendation 2",
                    "recommendation 3"
                ]
            }}
            """
        }]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)

    print(f"\n📊 INCLUSION SCORE: {data['inclusion_score']}/100")
    print(f"   {data['score_explanation']}\n")
    print("✅ STRENGTHS:")
    for s in data['strengths']:
        print(f"   • {s['point']}: {s['detail']}")
    print("\n⚠️  GAPS:")
    for g in data['gaps']:
        print(f"   • {g['point']}: {g['detail']}")
    print("\n💡 RECOMMENDATIONS:")
    for r in data['recommendations']:
        print(f"   • {r}")

    save_output("culture_report", {
        "company_description": company,
        "report": data,
        "timestamp": str(datetime.now())
    })

def bias_scanner():
    print("\n=== JD Bias Scanner ===\n")
    print("Paste your job description (type END when done):\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    job_description = "\n".join(lines)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
            You are an inclusive hiring expert. Analyze this job description
            for language that excludes neurodivergent candidates.
            Job Description: {job_description}
            Return ONLY a JSON object with exactly this structure, no extra text:
            {{
                "bias_score": 0,
                "flagged_phrases": [
                    {{"phrase": "word", "reason": "why exclusionary", "replacement": "better alternative"}}
                ],
                "rewritten_jd": "full rewritten inclusive version"
            }}
            """
        }]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)

    print(f"\n📊 BIAS SCORE: {data['bias_score']}/100")
    print("\n🚩 FLAGGED PHRASES:")
    for f in data['flagged_phrases']:
        print(f"   • '{f['phrase']}' → {f['replacement']}")
        print(f"     Why: {f['reason']}")
    print("\n✅ REWRITTEN JD:")
    print(data['rewritten_jd'])

    save_output("bias_scan", {
        "original_jd": job_description,
        "analysis": data,
        "timestamp": str(datetime.now())
    })

def match_score():
    print("\n=== Working Style Match Score ===\n")
    print("Answer these questions:\n")
    q1 = input("1. Alone or in a team? ")
    q2 = input("2. Quiet focused work or collaboration? ")
    q3 = input("3. How do you handle deadlines? ")
    q4 = input("4. Structured tasks or open-ended? ")
    q5 = input("5. Remote, hybrid or office? ")

    candidate_profile = f"""
    Working style: {q1}
    Environment: {q2}
    Deadlines: {q3}
    Task preference: {q4}
    Location: {q5}
    """

    print("\nPaste the job description (type END when done):\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    job_description = "\n".join(lines)

    print("\nCalculating match score...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    candidate_embedding = model.encode(candidate_profile, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    similarity = util.cos_sim(candidate_embedding, job_embedding)
    score = round(float(similarity[0][0]) * 100, 1)

    if score >= 70:
        match_level = "✅ Strong Match"
    elif score >= 50:
        match_level = "⚠️ Moderate Match"
    else:
        match_level = "❌ Poor Match"

    print(f"\n{'='*40}")
    print(f"MATCH SCORE: {score}%  —  {match_level}")
    print(f"{'='*40}\n")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
            Candidate has {score}% match with this job.
            Candidate profile: {candidate_profile}
            Job: {job_description}
            In 3-4 sentences explain why this is a {match_level}
            and give one practical recommendation.
            """
        }]
    )

    explanation = response.choices[0].message.content
    print(explanation)

    save_output("match_score", {
        "candidate_profile": candidate_profile,
        "job_description": job_description,
        "match_score": score,
        "match_level": match_level,
        "explanation": explanation,
        "timestamp": str(datetime.now())
    })

def persona_generator():
    print("\n=== Neurodivergent Candidate Persona Generator ===\n")
    print("Answer these questions:\n")
    name = input("Your name (or anonymous): ")
    q1 = input("1. How do you work best? ")
    q2 = input("2. What environment helps you focus? ")
    q3 = input("3. What are your biggest strengths? ")
    q4 = input("4. What challenges do you face at work? ")
    q5 = input("5. What accommodations help you most? ")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
            Based on these answers, generate a professional neurodivergent 
            candidate persona profile that this person can share with employers.
            
            Answers: 
            Works best: {q1}
            Environment: {q2}
            Strengths: {q3}
            Challenges: {q4}
            Accommodations: {q5}
            
            Return ONLY a JSON object:
            {{
                "persona_name": "professional label for their work style",
                "cognitive_strengths": ["strength 1", "strength 2", "strength 3"],
                "ideal_environment": "description of best work environment",
                "growth_areas": ["area 1", "area 2"],
                "accommodation_requests": ["request 1", "request 2", "request 3"],
                "best_role_types": ["role type 1", "role type 2", "role type 3"],
                "employer_message": "a short professional message this candidate can share with employers"
            }}
            """
        }]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)

    print(f"\n🧠 PERSONA: {data['persona_name']}")
    print("\n💪 COGNITIVE STRENGTHS:")
    for s in data['cognitive_strengths']:
        print(f"   • {s}")
    print(f"\n🏢 IDEAL ENVIRONMENT: {data['ideal_environment']}")
    print("\n📈 GROWTH AREAS:")
    for g in data['growth_areas']:
        print(f"   • {g}")
    print("\n🤝 ACCOMMODATION REQUESTS:")
    for a in data['accommodation_requests']:
        print(f"   • {a}")
    print("\n💼 BEST ROLE TYPES:")
    for r in data['best_role_types']:
        print(f"   • {r}")
    print(f"\n📝 EMPLOYER MESSAGE:\n   {data['employer_message']}")

    save_output("persona", {
        "name": name,
        "persona": data,
        "timestamp": str(datetime.now())
    })

# MAIN MENU
while True:
    print("\n" + "="*40)
    print("   🧠 CogniMatch AI Engine")
    print("="*40)
    print("1. Culture Intelligence Report")
    print("2. JD Bias Scanner")
    print("3. Working Style Match Score")
    print("4. Candidate Persona Generator")
    print("5. Exit")
    print("="*40)

    choice = input("Choose (1/2/3/4/5): ")

    if choice == "1":
        culture_report()
    elif choice == "2":
        bias_scanner()
    elif choice == "3":
        match_score()
    elif choice == "4":
        persona_generator()
    elif choice == "5":
        print("\nGoodbye! 👋")
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")