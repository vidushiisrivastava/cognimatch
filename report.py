from dotenv import load_dotenv
load_dotenv()
from groq import Groq
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
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
        """
    }]
)

print(response.choices[0].message.content)