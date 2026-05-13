from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("=== CogniMatch JD Bias Scanner ===\n")
print("Paste your job description below.")
print("When done, type END on a new line and press Enter:\n")

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
        You are an inclusive hiring expert. Analyze this job description for language 
        that may unintentionally exclude neurodivergent candidates (ADHD, autism, dyslexia etc).
        
        Job Description:
        {job_description}
        
        Provide:
        1. BIAS SCORE (0-100, where 0 = very biased, 100 = very inclusive)
        2. FLAGGED WORDS/PHRASES - list each biased phrase and why it's exclusionary
        3. SUGGESTED REPLACEMENTS - better alternatives for each flagged phrase
        4. REWRITTEN JD - rewrite the entire job description to be more inclusive
        
        Be specific and practical.
        """
    }]
)

print("\n" + response.choices[0].message.content)