<div align="center">

# CogniMatch

### AI-Powered Inclusive Hiring for Neurodivergent Talent

*Built at **LinkedIn Hackathon 2026** by Team InnovHer*

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)](https://groq.com)

</div>

---

## 🌟 The Problem

Hiring systems today silently filter out neurodivergent talent — through biased job description language, rigid interview formats, and resume screening that rewards conformity over capability.

**CogniMatch** uses AI to fix that. We match candidates on **working style compatibility**, not just keywords — and we give companies the tools to make their hiring genuinely inclusive.

---

## ✨ Features

### 1. 📊 Culture Intelligence Report
Analyzes a company's work culture and generates a detailed inclusion assessment.

| I/O | Details |
|-----|---------|
| **Input** | Company description |
| **Output** | Inclusion score (0–100), strengths, gaps, actionable recommendations |
| **AI** | LLaMA 3.3 70B via Groq |

---

### 2. 🚩 JD Bias Scanner
Detects exclusionary language in job descriptions and rewrites them to be inclusive.

| I/O | Details |
|-----|---------|
| **Input** | Job description text |
| **Output** | Bias score, flagged phrases, inclusive replacements, fully rewritten JD |
| **AI** | LLaMA 3.3 70B via Groq |

---

### 3. 🎯 Working Style Match Score
Semantically matches a candidate's working style to a job description — going far beyond keyword matching.

| I/O | Details |
|-----|---------|
| **Input** | 5 working style answers + job description |
| **Output** | Match % with Strong / Moderate / Poor label + AI-generated explanation |
| **AI** | Sentence Transformers (`all-MiniLM-L6-v2`) + LLaMA 3.3 70B |

---

### 4. 🧬 Candidate Persona Generator
Builds a shareable neurodivergent professional profile to help candidates advocate for themselves.

| I/O | Details |
|-----|---------|
| **Input** | 6 multiple-choice questions about working preferences |
| **Output** | Persona name, strengths, ideal environment, accommodation requests, employer message |
| **AI** | LLaMA 3.3 70B via Groq |

---

## 🛠️ Tech Stack

### 🤖 AI / ML
| Component | Technology |
|-----------|-----------|
| **LLM** | LLaMA 3.3 70B via Groq API |
| **Embeddings** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Similarity** | Cosine Similarity (vector-based matching) |
| **Output** | Structured JSON via Prompt Engineering |
| **Use Cases** | Candidate matching, bias detection, report generation |

### ⚙️ Backend
| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.13 |
| **Framework** | FastAPI + Uvicorn |
| **ORM** | SQLAlchemy |
| **Database** | PostgreSQL |
| **Auth** | JWT + bcrypt |
| **Validation** | Pydantic |

### 🎨 Frontend
| Component | Technology |
|-----------|-----------|
| **Framework** | Next.js + React |
| **Language** | TypeScript |
| **Styling** | Tailwind CSS |

### 🗄️ Database
| Component | Technology |
|-----------|-----------|
| **Platform** | Supabase (PostgreSQL) |
| **Client** | supabase-py |
| **Vector Search** | pgvector (embedding-based similarity) |
| **Config** | python-dotenv |

---

## 🧠 AI Techniques

- **LLM Prompting** — structured JSON extraction from natural language responses
- **Vector Embeddings** — semantic understanding of working style beyond surface keywords
- **Cosine Similarity** — mathematical compatibility scoring between candidate and job
- **pgvector** — database-level embedding search for scalable similarity queries

---

## 📁 Project Structure

```
cognimatch/
├── backend/                  # Backend API and integrations
├── cognimatch_ai.py          # Core AI engine & persona generator
├── bias_scanner.py           # JD bias detection & rewriting
├── match_score.py            # Working style vector matching
├── report.py                 # Culture intelligence report generator
├── .gitignore
└── README.md
```

### Output Files
Every feature auto-saves a timestamped JSON file for backend consumption:

```
output_culture_report_<TIMESTAMP>.json
output_bias_scan_<TIMESTAMP>.json
output_match_score_<TIMESTAMP>.json
output_persona_<TIMESTAMP>.json
```

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.13+
- A [Groq API key](https://console.groq.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/vidushiisrivastava/cognimatch.git
cd cognimatch

# 2. Install dependencies
pip install groq sentence-transformers python-dotenv

# 3. Set up environment variables
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Run any module
python cognimatch_ai.py    # Persona generator
python bias_scanner.py     # JD bias scanner
python match_score.py      # Working style match
python report.py           # Culture intelligence report
```

---

## 👩‍💻 Team InnovHer

| Name | Role |
|------|------|
| Vidushi Srivastava | AI / ML |
| Divisha Panjwani | Backend |
| Riya Umesh Singh | Frontend |
| Apekshita Chauhan | Database |
| Stuti Agarwal | Product + Testing |

---

## 💡 Why This Matters

> ~15–20% of the global population is neurodivergent, including people with ADHD, autism, dyslexia, and more. Many are filtered out of hiring pipelines not because of capability, but because the system wasn't designed for them.
>
> CogniMatch doesn't just optimize for efficiency. It optimizes for **equity**.

---

<div align="center">

Made by Team InnovHer &nbsp;|&nbsp; LinkedIn Hackathon 2026

</div>
