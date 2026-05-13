# 🧠 CogniMatch — AI Engine
> AI-powered inclusive hiring platform for neurodivergent talent
> Built for LinkedIn Hackathon 2026

---

## 🚀 What is CogniMatch?
Hiring systems today accidentally filter out neurodivergent talent through biased language, sensory-unfriendly environments, and style mismatches. CogniMatch uses AI to fix that — matching candidates on **working style** not just resume keywords.

---

## 🤖 4 AI Features

### 1. 📊 Culture Intelligence Report
Analyzes a company's work environment and generates an inclusion report.
- **Input:** Company description
- **Output:** Inclusion score (0-100), strengths, gaps, recommendations
- **AI:** LLaMA 3.3 70B via Groq

### 2. 🚩 JD Bias Scanner
Detects exclusionary language in job descriptions.
- **Input:** Job description
- **Output:** Bias score, flagged phrases, inclusive replacements, rewritten JD
- **AI:** LLaMA 3.3 70B via Groq

### 3. 🎯 Working Style Match Score
Matches candidate working style to a job using vector embeddings.
- **Input:** 5 working style answers + job description
- **Output:** Match % (Strong/Moderate/Poor) + AI explanation
- **AI:** Sentence Transformers (all-MiniLM-L6-v2) + LLaMA 3.3 70B

### 4. 🧠 Candidate Persona Generator
Generates a shareable neurodivergent professional profile.
- **Input:** 6 multiple choice questions about working style
- **Output:** Persona name, strengths, ideal environment, accommodation requests, employer message
- **AI:** LLaMA 3.3 70B via Groq

---

## 🛠️ Tech Stack
| Component | Technology |
|-----------|-----------|
| Language | Python 3.13 |
| LLM | Groq API — LLaMA 3.3 70B |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Output format | Structured JSON |
| Environment | python-dotenv |

---

## ⚙️ Setup & Run

1. Clone the repo:
git clone https://github.com/vidushiisrivastava/cognimatch.git
2. Install dependencies:
pip install groq sentence-transformers python-dotenv
3. Create a `.env` file:
GROQ_API_KEY=your_key_here
4. Run the AI engine:

---

## 📁 Output Files
Every feature auto-saves a timestamped JSON file consumed by the backend:
- `output_culture_report_TIMESTAMP.json`
- `output_bias_scan_TIMESTAMP.json`
- `output_match_score_TIMESTAMP.json`
- `output_persona_TIMESTAMP.json`

---

## 🧠 AI Techniques Used
- **LLM prompting** — structured JSON extraction from natural language
- **Vector embeddings** — semantic similarity matching beyond keywords
- **Cosine similarity** — mathematical working style compatibility score

---

## 👩‍💻 Built by
**Vidushi Srivastava** 
