from groq import Groq
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from db import save_candidate_persona, save_match_score, save_bias_scan, save_culture_report

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def save_output(feature_name, data):
    filename = f"output_{feature_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Output saved to {filename}")
    return filename

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
    print("✓ STRENGTHS:")
    for s in data['strengths']:
        print(f"   • {s['point']}: {s['detail']}")
    print("\n⚠  GAPS:")
    for g in data['gaps']:
        print(f"   • {g['point']}: {g['detail']}")
    print("\n💡 RECOMMENDATIONS:")
    for r in data['recommendations']:
        print(f"   • {r}")

    output = {
        "company_description": company,
        "report": data,
        "timestamp": str(datetime.now())
    }
    filename = save_output("culture_report", output)

    # --- SAVE TO DATABASE ---
    try:
        save_culture_report(filename, org_id=None)
        print("✓ Saved to Supabase database!")
    except Exception as e:
        print(f"DB save skipped: {e}")

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
    print("\n🚨 FLAGGED PHRASES:")
    for f in data['flagged_phrases']:
        print(f"   • '{f['phrase']}' → {f['replacement']}")
        print(f"     Why: {f['reason']}")
    print("\n✓ REWRITTEN JD:")
    print(data['rewritten_jd'])

    output = {
        "original_jd": job_description,
        "analysis": data,
        "flagged_terms": data['flagged_phrases'],
        "bias_score": data['bias_score'],
        "suggestions": [p['replacement'] for p in data['flagged_phrases']],
        "timestamp": str(datetime.now())
    }
    filename = save_output("bias_scan", output)

    # --- SAVE TO DATABASE ---
    try:
        save_bias_scan(filename, org_id=None, job_description=job_description)
        print("✓ Saved to Supabase database!")
    except Exception as e:
        print(f"DB save skipped: {e}")

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
        match_level = "Strong Match"
    elif score >= 50:
        match_level = "Moderate Match"
    else:
        match_level = "Poor Match"

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

    output = {
        "candidate_profile": candidate_profile,
        "job_description": job_description,
        "match_score": score,
        "match_level": match_level,
        "breakdown": {"explanation": explanation},
        "timestamp": str(datetime.now())
    }
    filename = save_output("match_score", output)

    # --- SAVE TO DATABASE ---
    try:
        save_match_score(filename, candidate_id=None, org_id=None)
        print("✓ Saved to Supabase database!")
    except Exception as e:
        print(f"DB save skipped: {e}")

def persona_generator():
    print("\n=== Neurodivergent Candidate Persona Generator ===\n")
    name = input("Your name (or anonymous): ")

    def choose(question, options):
        print(f"\n{question}")
        for i, opt in enumerate(options, 1):
            print(f"   {i}. {opt}")
        while True:
            try:
                choice = int(input("Choose (enter number): "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Please enter a valid number")

    q1 = choose("How do you work best?", [
        "Alone with deep focus",
        "Small team of 2-3 people",
        "Large collaborative team",
        "Mix of solo and team work"
    ])
    q2 = choose("What environment helps you focus?", [
        "Quiet private space",
        "Background noise/music",
        "Busy open office",
        "Work from home"
    ])
    q3 = choose("What is your biggest strength?", [
        "Deep focus and attention to detail",
        "Creative and outside-the-box thinking",
        "Pattern recognition and analysis",
        "Hyperfocus on topics I'm passionate about",
        "Systematic and process-oriented thinking"
    ])
    q4 = choose("What is your biggest challenge at work?", [
        "Sensory overload in loud environments",
        "Back-to-back meetings with no breaks",
        "Unclear or changing instructions",
        "Open-ended tasks with no structure",
        "Social communication and small talk"
    ])
    q5 = choose("What accommodation helps you most?", [
        "Written instructions instead of verbal",
        "Flexible work hours",
        "Quiet workspace or noise-cancelling headphones",
        "Clear deadlines and structured tasks",
        "Remote or hybrid work option"
    ])
    q6 = choose("What type of role suits you best?", [
        "Technical / engineering / coding",
        "Research and analysis",
        "Creative / design / writing",
        "Data and systems",
        "Problem solving and strategy"
    ])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
            Based on these answers, generate a professional neurodivergent
            candidate persona profile to share with employers.
            Works best: {q1}
            Environment: {q2}
            Strength: {q3}
            Challenge: {q4}
            Accommodation: {q5}
            Role type: {q6}
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
    print("\n💬 COGNITIVE STRENGTHS:")
    for s in data['cognitive_strengths']:
        print(f"   • {s}")
    print(f"\n🏠 IDEAL ENVIRONMENT: {data['ideal_environment']}")
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

    output = {
        "name": name,
        "persona": data,
        "working_style": {
            "works_best": q1,
            "environment": q2,
            "strength": q3,
            "challenge": q4,
            "accommodation": q5,
            "role_type": q6
        },
        "timestamp": str(datetime.now())
    }
    filename = save_output("persona", output)

    # --- SAVE TO DATABASE ---
    try:
        save_candidate_persona(filename, user_id=None)
        print("✓ Saved to Supabase database!")
    except Exception as e:
        print(f"DB save skipped: {e}")

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
        print("\nGoodbye!")
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")