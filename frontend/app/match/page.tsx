'use client'
import { useState } from 'react'

const questions = [
  { id: 'q1', text: 'How do you prefer to receive new tasks?', options: ['Detailed written brief upfront', 'Quick verbal overview then figure it out', 'Collaborative planning session', 'Just dive in and learn as I go'] },
  { id: 'q2', text: 'Your ideal work environment is...', options: ['Quiet, private, minimal interruptions', 'Open, social, collaborative buzz', 'Flexible — I switch between both', 'Remote, fully async'] },
  { id: 'q3', text: 'How do you handle ambiguous projects?', options: ['I need clear requirements first', 'I thrive with creative freedom', 'I ask lots of clarifying questions', 'I make assumptions and adjust later'] },
  { id: 'q4', text: 'Your communication style is...', options: ['Written first — I think in text', 'Visual — diagrams and whiteboards', 'Verbal — I process by talking', 'Direct and concise, no small talk'] },
  { id: 'q5', text: 'Under deadline pressure, you...', options: ['Focus deeply on one thing at a time', 'Context-switch rapidly between tasks', 'Need to step back and re-prioritize', 'Thrive — pressure helps me focus'] },
]

interface MatchResult {
  match_percentage: number
  match_label: string
  explanation: string
  strengths: string[]
  risks: string[]
}

export default function MatchPage() {
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [jd, setJd] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<MatchResult | null>(null)
  const [error, setError] = useState('')

  const allAnswered = Object.keys(answers).length === questions.length && jd.trim()

  const runMatch = async () => {
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await fetch('http://localhost:8000/api/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: Object.values(answers), job_description: jd }),
      })
      if (!res.ok) throw new Error('API error')
      setResult(await res.json())
    } catch {
      setError('Could not reach the AI engine. Make sure FastAPI is running on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  const scoreColor = result
    ? result.match_percentage >= 70 ? '#00d4a4'
    : result.match_percentage >= 40 ? '#ffb347'
    : '#ff6b6b'
    : '#7c5cfc'

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '48px 24px' }}>
      <div style={{ marginBottom: 40 }}>
        <div className="badge badge-purple" style={{ marginBottom: 14 }}>🎯 match_score.py</div>
        <h1 style={{ fontFamily: 'Syne, sans-serif', fontSize: 36, marginBottom: 10 }}>Working style match score</h1>
        <p style={{ color: '#9590b8' }}>Answer 5 questions, paste a job description — get your match % powered by vector embeddings.</p>
      </div>

      {/* Questions */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20, marginBottom: 28 }}>
        {questions.map((q, qi) => (
          <div key={q.id} className="card">
            <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', marginBottom: 14 }}>
              <div style={{
                width: 28, height: 28, borderRadius: 8, background: 'rgba(124,92,252,0.15)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontFamily: 'Syne, sans-serif', fontSize: 13, fontWeight: 700, color: '#a688ff', flexShrink: 0,
              }}>{qi + 1}</div>
              <p style={{ fontWeight: 500, fontSize: 15, color: '#f0effe', lineHeight: 1.4 }}>{q.text}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {q.options.map(opt => (
                <button key={opt} onClick={() => setAnswers(a => ({ ...a, [q.id]: opt }))}
                  style={{
                    background: answers[q.id] === opt ? 'rgba(124,92,252,0.15)' : '#1a1a24',
                    border: `1px solid ${answers[q.id] === opt ? '#7c5cfc' : 'rgba(255,255,255,0.06)'}`,
                    borderRadius: 8, padding: '11px 16px',
                    color: answers[q.id] === opt ? '#a688ff' : '#9590b8',
                    fontSize: 14, textAlign: 'left', cursor: 'pointer', transition: 'all 0.15s',
                    fontFamily: 'DM Sans, sans-serif',
                  }}>
                  {answers[q.id] === opt ? '✓ ' : ''}{opt}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* JD input */}
      <div className="card" style={{ marginBottom: 24 }}>
        <label className="label">Paste the job description</label>
        <textarea className="textarea" placeholder="Paste the full job description here..." value={jd} onChange={e => setJd(e.target.value)} rows={6} />
      </div>

      <button className="btn-primary" onClick={runMatch} disabled={!allAnswered || loading}
        style={{ opacity: !allAnswered || loading ? 0.6 : 1, width: '100%', justifyContent: 'center', padding: '14px' }}>
        {loading ? <><span className="spinner" /> Calculating match...</> : '🎯 Get my match score →'}
      </button>

      {error && (
        <div style={{ background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.25)', borderRadius: 10, padding: '14px 18px', color: '#ff6b6b', fontSize: 14, marginTop: 20 }}>
          ⚠️ {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="fade-up" style={{ marginTop: 32 }}>
          {/* Big score */}
          <div style={{
            textAlign: 'center', padding: '40px 20px', marginBottom: 24,
            background: '#111118', border: `1px solid ${scoreColor}30`, borderRadius: 16,
            boxShadow: `0 0 60px ${scoreColor}15`,
          }}>
            <div style={{ fontSize: 72, fontWeight: 800, fontFamily: 'Syne, sans-serif', color: scoreColor, lineHeight: 1 }}>
              {result.match_percentage}%
            </div>
            <div style={{ fontSize: 18, fontFamily: 'Syne, sans-serif', color: scoreColor, marginTop: 8 }}>
              {result.match_label}
            </div>
          </div>

          {/* Explanation */}
          <div className="card" style={{ marginBottom: 20, fontSize: 14, color: '#9590b8', lineHeight: 1.7 }}>
            <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 16, marginBottom: 12, color: '#f0effe' }}>What this means</h3>
            {result.explanation}
          </div>

          {/* Strengths + risks */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            {result.strengths?.length > 0 && (
              <div className="card">
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, color: '#00d4a4', marginBottom: 14 }}>✓ Strengths</h3>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {result.strengths.map((s, i) => (
                    <li key={i} style={{ fontSize: 13, color: '#9590b8', paddingLeft: 14, borderLeft: '2px solid rgba(0,212,164,0.3)' }}>{s}</li>
                  ))}
                </ul>
              </div>
            )}
            {result.risks?.length > 0 && (
              <div className="card">
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, color: '#ff6b6b', marginBottom: 14 }}>⚠ Mismatch risks</h3>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {result.risks.map((r, i) => (
                    <li key={i} style={{ fontSize: 13, color: '#9590b8', paddingLeft: 14, borderLeft: '2px solid rgba(255,107,107,0.3)' }}>{r}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}