'use client'
import { useState } from 'react'

const questions = [
  { id: 'q1', text: 'When starting a new task, I prefer to...', options: ['Plan everything out first', 'Dive straight in', 'Research examples first', 'Talk it through with someone'] },
  { id: 'q2', text: 'I do my best work...', options: ['In complete quiet', 'With background music or noise', 'In short intense bursts', 'In long uninterrupted sessions'] },
  { id: 'q3', text: 'When I get feedback, I prefer it to be...', options: ['Written and detailed', 'Verbal and conversational', 'Direct and blunt', 'Gentle and encouraging'] },
  { id: 'q4', text: 'My relationship with deadlines is...', options: ['I always finish early', 'I work best near the deadline', 'I need flexible timelines', 'Deadlines stress me out significantly'] },
  { id: 'q5', text: 'In meetings, I typically...', options: ['Share ideas freely', 'Prefer to listen and process', 'Need an agenda to participate', 'Find them draining'] },
  { id: 'q6', text: 'My ideal team is...', options: ['Highly collaborative, always together', 'Independent but aligned', 'Async-first, minimal meetings', 'Small and deeply focused'] },
]

interface PersonaResult {
  persona_name: string
  strengths: string[]
  ideal_environment: string[]
  accommodation_requests: string[]
  employer_message: string
  working_style_summary: string
}

export default function OnboardingPage() {
  const [step, setStep] = useState(0) // 0=intro, 1-6=questions, 7=result
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PersonaResult | null>(null)
  const [error, setError] = useState('')

  const currentQ = questions[step - 1]
  const progress = step === 0 ? 0 : (step / questions.length) * 100

  const selectAnswer = async (opt: string) => {
    const newAnswers = { ...answers, [currentQ.id]: opt }
    setAnswers(newAnswers)
    if (step < questions.length) {
      setStep(step + 1)
    } else {
      // Last question — generate persona
      setStep(7)
      setLoading(true)
      try {
        const res = await fetch('http://localhost:8000/api/persona', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ answers: Object.values(newAnswers) }),
        })
        if (!res.ok) throw new Error()
        setResult(await res.json())
      } catch {
        setError('Could not reach the AI engine. Make sure FastAPI is running on port 8000.')
      } finally {
        setLoading(false)
      }
    }
  }

  // Intro screen
  if (step === 0) return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: '80px 24px', textAlign: 'center' }}>
      <div style={{ fontSize: 56, marginBottom: 24 }}>🧠</div>
      <h1 style={{ fontFamily: 'Syne, sans-serif', fontSize: 36, marginBottom: 14 }}>Discover your work persona</h1>
      <p style={{ color: '#9590b8', fontSize: 15, lineHeight: 1.7, marginBottom: 12 }}>
        6 quick questions about how you work. No diagnosis. No labels. Just honest answers.
      </p>
      <p style={{ color: '#5a5570', fontSize: 13, marginBottom: 36 }}>Takes about 2 minutes.</p>
      <button className="btn-primary" onClick={() => setStep(1)} style={{ fontSize: 16, padding: '14px 32px' }}>
        Let's go →
      </button>
    </div>
  )

  // Loading / result
  if (step === 7) return (
    <div style={{ maxWidth: 700, margin: '0 auto', padding: '48px 24px' }}>
      {loading && (
        <div style={{ textAlign: 'center', padding: '80px 0' }}>
          <div className="spinner" style={{ width: 40, height: 40, margin: '0 auto 24px', borderWidth: 3 }}/>
          <p style={{ color: '#9590b8', fontFamily: 'Syne, sans-serif', fontSize: 18 }}>Generating your persona...</p>
          <p style={{ color: '#5a5570', fontSize: 13, marginTop: 8 }}>LLaMA 3.3 70B via Groq is thinking</p>
        </div>
      )}

      {error && (
        <div style={{ background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.25)', borderRadius: 10, padding: '20px', color: '#ff6b6b', textAlign: 'center' }}>
          ⚠️ {error}
        </div>
      )}

      {result && !loading && (
        <div className="fade-up">
          {/* Persona card */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(124,92,252,0.15), rgba(0,212,164,0.08))',
            border: '1px solid rgba(124,92,252,0.3)',
            borderRadius: 20, padding: '40px 32px', textAlign: 'center', marginBottom: 24,
          }}>
            <div style={{ fontSize: 52, marginBottom: 16 }}>🧠</div>
            <div className="badge badge-purple" style={{ marginBottom: 16 }}>Your persona</div>
            <h1 style={{ fontFamily: 'Syne, sans-serif', fontSize: 32, marginBottom: 12, background: 'linear-gradient(135deg, #a688ff, #00d4a4)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              {result.persona_name}
            </h1>
            {result.working_style_summary && (
              <p style={{ color: '#9590b8', fontSize: 15, maxWidth: 480, margin: '0 auto', lineHeight: 1.7 }}>
                {result.working_style_summary}
              </p>
            )}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 20 }}>
            {result.strengths?.length > 0 && (
              <div className="card">
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, color: '#a688ff', marginBottom: 14 }}>⚡ Strengths</h3>
                {result.strengths.map((s, i) => (
                  <div key={i} style={{ fontSize: 13, color: '#9590b8', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>{s}</div>
                ))}
              </div>
            )}
            {result.ideal_environment?.length > 0 && (
              <div className="card">
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, color: '#00d4a4', marginBottom: 14 }}>🌿 Ideal environment</h3>
                {result.ideal_environment.map((e, i) => (
                  <div key={i} style={{ fontSize: 13, color: '#9590b8', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>{e}</div>
                ))}
              </div>
            )}
            {result.accommodation_requests?.length > 0 && (
              <div className="card">
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, color: '#ffb347', marginBottom: 14 }}>🤝 Accommodations to request</h3>
                {result.accommodation_requests.map((a, i) => (
                  <div key={i} style={{ fontSize: 13, color: '#9590b8', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>{a}</div>
                ))}
              </div>
            )}
          </div>

          {result.employer_message && (
            <div className="card">
              <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, marginBottom: 12 }}>💬 What to tell your employer</h3>
              <p style={{ color: '#9590b8', fontSize: 14, lineHeight: 1.7, fontStyle: 'italic' }}>"{result.employer_message}"</p>
              <button onClick={() => navigator.clipboard.writeText(result.employer_message)}
                style={{ marginTop: 12, fontSize: 12, color: '#7c5cfc', background: 'none', border: '1px solid rgba(124,92,252,0.3)', borderRadius: 6, padding: '5px 12px', cursor: 'pointer', fontFamily: 'DM Sans, sans-serif' }}>
                Copy message
              </button>
            </div>
          )}

          <div style={{ display: 'flex', gap: 12, marginTop: 20, justifyContent: 'center' }}>
            <button className="btn-primary" onClick={() => { setStep(0); setAnswers({}); setResult(null) }}>
              Retake quiz
            </button>
            <a href="/match" className="btn-secondary">
              Now find matching jobs →
            </a>
          </div>
        </div>
      )}
    </div>
  )

  // Quiz question
  return (
    <div style={{ maxWidth: 620, margin: '0 auto', padding: '48px 24px' }}>
      {/* Progress */}
      <div style={{ marginBottom: 40 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
          <span style={{ fontSize: 12, color: '#5a5570' }}>Question {step} of {questions.length}</span>
          <span style={{ fontSize: 12, color: '#5a5570' }}>{Math.round(progress)}% complete</span>
        </div>
        <div style={{ height: 3, background: 'rgba(255,255,255,0.06)', borderRadius: 99 }}>
          <div style={{ height: '100%', width: `${progress}%`, background: 'linear-gradient(90deg, #7c5cfc, #00d4a4)', borderRadius: 99, transition: 'width 0.3s ease' }} />
        </div>
      </div>

      <h2 style={{ fontFamily: 'Syne, sans-serif', fontSize: 24, marginBottom: 28, lineHeight: 1.3 }}>
        {currentQ.text}
      </h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {currentQ.options.map(opt => (
          <button key={opt} onClick={() => selectAnswer(opt)}
            style={{
              background: '#111118', border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: 12, padding: '16px 20px',
              color: '#9590b8', fontSize: 15, textAlign: 'left', cursor: 'pointer',
              transition: 'all 0.15s', fontFamily: 'DM Sans, sans-serif',
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = '#7c5cfc'; e.currentTarget.style.color = '#f0effe'; e.currentTarget.style.background = 'rgba(124,92,252,0.08)' }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'; e.currentTarget.style.color = '#9590b8'; e.currentTarget.style.background = '#111118' }}>
            {opt}
          </button>
        ))}
      </div>

      {step > 1 && (
        <button onClick={() => setStep(step - 1)}
          style={{ marginTop: 20, fontSize: 13, color: '#5a5570', background: 'none', border: 'none', cursor: 'pointer', fontFamily: 'DM Sans, sans-serif' }}>
          ← Back
        </button>
      )}
    </div>
  )
}