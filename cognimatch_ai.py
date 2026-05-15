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
    print("Answer honestly — there are no right or wrong answers.\n")
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

    # SECTION 1 — Focus & Attention (ADHD-informed)
    print("\n--- Section 1: Focus & Attention ---")
    
    q1 = choose("When working on a task, I typically:", [
        "Can focus deeply for long periods without distraction",
        "Work best in short intense bursts with breaks",
        "Need external structure to stay on track",
        "Hyperfocus on things I find interesting, struggle with others"
    ])

    q2 = choose("When I receive a complex project, I prefer to:", [
        "Break it into small structured steps with clear deadlines",
        "Dive straight in and figure it out as I go",
        "Understand the big picture first before any details",
        "Work through it with someone else for accountability"
    ])

    q3 = choose("Interruptions during deep work make me feel:", [
        "Frustrated — I need long uninterrupted blocks",
        "Fine — I can switch tasks easily",
        "Anxious — I lose my train of thought completely",
        "Relieved — I welcome natural breaks"
    ])

    # SECTION 2 — Sensory & Environment (Sensory Profile-informed)
    print("\n--- Section 2: Sensory & Environment ---")

    q4 = choose("In a busy open office, I typically:", [
        "Struggle to concentrate due to noise and movement",
        "Feel energised by the activity around me",
        "Can tune it out with headphones",
        "Feel overwhelmed and need to leave regularly"
    ])

    q5 = choose("My ideal physical workspace is:", [
        "A private quiet room with minimal stimulation",
        "A small team room with familiar people",
        "A lively open space with energy",
        "Fully remote — home environment I control"
    ])

    q6 = choose("Regarding lighting and noise at work:", [
        "Sensitive to both — need low light and quiet",
        "Sensitive to noise only — lighting doesn't matter",
        "Sensitive to lighting only — noise is fine",
        "Not particularly sensitive to either"
    ])

    # SECTION 3 — Communication & Social (Autism-informed)
    print("\n--- Section 3: Communication & Social ---")

    q7 = choose("I communicate most effectively through:", [
        "Written messages — email, chat, documents",
        "Face to face conversations",
        "Video calls with camera on",
        "Structured meetings with a clear agenda sent in advance"
    ])

    q8 = choose("When given instructions, I work best when they are:", [
        "Written down with clear steps and expected outcomes",
        "Explained verbally with room to ask questions",
        "Demonstrated visually or shown by example",
        "Left open — I prefer figuring things out myself"
    ])

    q9 = choose("In team meetings, I typically:", [
        "Prefer to listen and contribute in writing afterwards",
        "Speak up easily and enjoy live discussion",
        "Struggle to process information fast enough to respond",
        "Need the agenda and materials in advance to participate well"
    ])

    # SECTION 4 — Structure & Flexibility (Dyslexia/Executive Function-informed)
    print("\n--- Section 4: Structure & Flexibility ---")

    q10 = choose("When my schedule or plans change unexpectedly, I:", [
        "Find it very difficult — I need predictability",
        "Adapt easily — I enjoy variety",
        "Need time to process the change before moving forward",
        "Feel anxious but manage after a short adjustment period"
    ])

    q11 = choose("I produce my best work when:", [
        "Given a clear deadline and specific requirements",
        "Given creative freedom with minimal constraints",
        "Working on one thing at a time with no multitasking",
        "Able to switch between tasks to maintain momentum"
    ])

    q12 = choose("When reading or writing at work:", [
        "I find it straightforward and efficient",
        "I prefer visual formats like diagrams and charts",
        "I take longer than others but am thorough",
        "I prefer someone to explain things verbally"
    ])

    # SECTION 5 — Strengths & Energy (Big Five-informed)
    print("\n--- Section 5: Strengths & Energy ---")

    q13 = choose("My greatest professional strength is:", [
        "Attention to detail — I catch things others miss",
        "Creative thinking — I generate unusual solutions",
        "Pattern recognition — I see connections in data",
        "Hyperfocus — when engaged, my output is exceptional",
        "Systematic thinking — I build reliable processes"
    ])

    q14 = choose("After a full day of social interaction at work, I feel:", [
        "Completely drained — I need alone time to recover",
        "Energised — I enjoy being around people",
        "Neutral — depends on the quality of interaction",
        "Anxious — social situations are mentally exhausting"
    ])

    q15 = choose("The accommodation that would help me most is:", [
        "Written instructions and clear expectations",
        "Flexible hours to work when I'm most productive",
        "Quiet workspace or noise-cancelling headphones",
        "Remote or hybrid work option",
        "Regular structured check-ins with my manager"
    ])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
            You are an occupational psychologist specializing in neurodiversity.
            Based on these validated assessment responses, generate a detailed 
            professional neurodivergent candidate persona.

            FOCUS & ATTENTION:
            - Task focus style: {q1}
            - Project approach: {q2}
            - Interruption response: {q3}

            SENSORY & ENVIRONMENT:
            - Open office response: {q4}
            - Ideal workspace: {q5}
            - Sensory sensitivities: {q6}

            COMMUNICATION & SOCIAL:
            - Communication preference: {q7}
            - Instruction preference: {q8}
            - Meeting style: {q9}

            STRUCTURE & FLEXIBILITY:
            - Change response: {q10}
            - Best work conditions: {q11}
            - Reading/writing style: {q12}

            STRENGTHS & ENERGY:
            - Core strength: {q13}
            - Social energy: {q14}
            - Key accommodation: {q15}

            Return ONLY a JSON object:
            {{
                "persona_name": "professional cognitive style label (e.g. Deep Focus Analyst, Creative Systems Thinker)",
                "likely_cognitive_profile": "brief description of likely neurodivergent profile based on answers",
                "cognitive_strengths": ["strength 1", "strength 2", "strength 3", "strength 4"],
                "ideal_environment": "detailed description of ideal work environment",
                "potential_challenges": ["challenge 1", "challenge 2", "challenge 3"],
                "accommodation_requests": ["specific request 1", "specific request 2", "specific request 3"],
                "best_role_types": ["role type 1", "role type 2", "role type 3"],
                "worst_environments": ["environment to avoid 1", "environment to avoid 2"],
                "employer_message": "a professional 3-sentence message this candidate can share with employers explaining their working style and needs"
            }}
            """
        }]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)

    print(f"\n🧠 COGNITIVE PERSONA: {data['persona_name']}")
    print(f"\n📋 PROFILE: {data['likely_cognitive_profile']}")
    print("\n💪 COGNITIVE STRENGTHS:")
    for s in data['cognitive_strengths']:
        print(f"   • {s}")
    print(f"\n🏢 IDEAL ENVIRONMENT: {data['ideal_environment']}")
    print("\n⚠️  POTENTIAL CHALLENGES:")
    for c in data['potential_challenges']:
        print(f"   • {c}")
    print("\n🤝 ACCOMMODATION REQUESTS:")
    for a in data['accommodation_requests']:
        print(f"   • {a}")
    print("\n💼 BEST ROLE TYPES:")
    for r in data['best_role_types']:
        print(f"   • {r}")
    print("\n🚫 ENVIRONMENTS TO AVOID:")
    for w in data['worst_environments']:
        print(f"   • {w}")
    print(f"\n📝 EMPLOYER MESSAGE:\n   {data['employer_message']}")

    save_output("persona", {
        "name": name,
        "responses": {
            "focus_attention": [q1, q2, q3],
            "sensory_environment": [q4, q5, q6],
            "communication_social": [q7, q8, q9],
            "structure_flexibility": [q10, q11, q12],
            "strengths_energy": [q13, q14, q15]
        },
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