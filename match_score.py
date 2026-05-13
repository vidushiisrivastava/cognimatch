from sentence_transformers import SentenceTransformer, util
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("=== CogniMatch Working Style Match Score ===\n")

# Step 1: Get candidate working style
print("Answer these questions about how you work best:\n")
q1 = input("1. Do you prefer working alone or in a team? ")
q2 = input("2. Do you prefer quiet focused work or collaborative discussions? ")
q3 = input("3. How do you handle tight deadlines? ")
q4 = input("4. Do you prefer structured tasks or open-ended problems? ")
q5 = input("5. Remote, hybrid or office? ")

candidate_profile = f"""
Working style: {q1}
Environment preference: {q2}
Deadline handling: {q3}
Task preference: {q4}
Location preference: {q5}
"""

# Step 2: Get job description
print("\nPaste the job description (type END when done):\n")
lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)
job_description = "\n".join(lines)

# Step 3: Calculate match score using embeddings
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

# Step 4: Get AI explanation
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{
        "role": "user",
        "content": f"""
        A candidate has a {score}% working style match with a job.
        
        Candidate profile: {candidate_profile}
        Job description: {job_description}
        
        In 3-4 sentences explain:
        1. Why this is a {match_level} 
        2. What specifically aligns or doesn't align
        3. One practical recommendation for the candidate
        """
    }]
)

print(response.choices[0].message.content)