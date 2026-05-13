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
            Generate a Culture Intelligence Report with:
            1. Inclusion Score (out of 100)
            2. Top 3 strengths for neurodivergent employees
            3. Top 3 gaps
            4. Recommendations for improvement
            Return as plain text.
            """
        }]
    )
    
    result = response.choices[0].message.content
    print("\n" + result)
    save_output("culture_report", {
        "company_description": company,
        "report": result,
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
            for language that may exclude neurodivergent candidates.
            
            Job Description: {job_description}
            
            Provide:
            1. BIAS SCORE (0-100, where 100 = very inclusive)
            2. FLAGGED WORDS/PHRASES with explanation
            3. SUGGESTED REPLACEMENTS
            4. REWRITTEN inclusive JD
            """
        }]
    )
    
    result = response.choices[0].message.content
    print("\n" + result)
    save_output("bias_scan", {
        "original_jd": job_description,
        "analysis": result,
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

# MAIN MENU
while True:
    print("\n" + "="*40)
    print("   🧠 CogniMatch AI Engine")
    print("="*40)
    print("1. Generate Culture Intelligence Report")
    print("2. Scan Job Description for Bias")
    print("3. Get Working Style Match Score")
    print("4. Exit")
    print("="*40)
    
    choice = input("Choose (1/2/3/4): ")
    
    if choice == "1":
        culture_report()
    elif choice == "2":
        bias_scanner()
    elif choice == "3":
        match_score()
    elif choice == "4":
        print("\nGoodbye! 👋")
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3 or 4.")