'use client'
import { useState } from 'react'

interface CultureResult {
  inclusion_score: number
  strengths: string[]
  gaps: string[]
  recommendations: string[]
  summary: string
}

export default function CulturePage() {
  const [desc, setDesc] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<CultureResult | null>(null)
  const [error, setError] = useState('')

  const generate = async () => {
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await fetch('http://localhost:8000/api/culture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company_description: desc }),
      })
      if (!res.ok) throw new Error()
      setResult(await res.json())
    } catch {
      setError('Could not reach the AI engine. Make sure FastAPI is running on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  const score = result?.inclusion_score ?? 0
  const scoreColor = score >= 70 ? '#00d4a4' : score >= 40 ? '#ffb347' : '#ff6b6b'
  const circumference = 2 * Math.PI * 52

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '48px 24px' }}>
      <div style={{ marginBottom: 40 }}>
        <div className="badge badge-teal" style={{ marginBottom: 14 }}>📊 report.py</div>
        <h1 style={{ fontFamily: 'Syne, sans-serif', fontSize: 36, marginBottom: 10 }}>Culture intelligence report</h1>
        <p style={{ color: '#9590b8' }}>Describe your company's culture. Get an AI inclusion score, strengths, gaps, and specific recommendations.</p>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <label className="label">Describe your company culture</label>
        <textarea
          className="textarea"
          rows={7}
          placeholder={`Describe your company's work environment, communication style, pace, meeting culture, remote/office setup, how decisions are made, what a typical day looks like for a new hire...`}
          value={desc}
          onChange={e => setDesc(e.target.value)}
        />
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 14 }}>
          <button className="btn-primary" onClick={generate} disabled={loading || desc.trim().length < 20}
            style={{ opacity: loading || desc.trim().length < 20 ? 0.6 : 1 }}>
            {loading ? <><span className="spinner" /> Generating report...</> : '📊 Generate culture report →'}
          </button>
        </div>
      </div>

      {error && (
        <div style={{ background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.25)', borderRadius: 10, padding: '14px 18px', color: '#ff6b6b', fontSize: 14 }}>
          ⚠️ {error}
        </div>
      )}

      {result && (
        <div className="fade-up">
          {/* Score ring */}
          <div className="card" style={{ textAlign: 'center', marginBottom: 20, padding: '36px' }}>
            <svg width="130" height="130" viewBox="0 0 130 130" style={{ margin: '0 auto 16px', display: 'block' }}>
              <circle cx="65" cy="65" r="52" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="10"/>
              <circle cx="65" cy="65" r="52" fill="none" stroke={scoreColor} strokeWidth="10"
                strokeLinecap="round"
                strokeDasharray={`${(score / 100) * circumference} ${circumference}`}
                strokeDashoffset={circumference * 0.25}
                style={{ transition: 'stroke-dasharray 1s ease' }}
              />
              <text x="65" y="60" textAnchor="middle" fill={scoreColor} fontSize="28" fontWeight="800" fontFamily="Syne, sans-serif">{score}</text>
              <text x="65" y="78" textAnchor="middle" fill="#5a5570" fontSize="11" fontFamily="DM Sans, sans-serif">/100</text>
            </svg>
            <h2 style={{ fontFamily: 'Syne, sans-serif', fontSize: 20, marginBottom: 8 }}>Inclusion score</h2>
            <p style={{ color: scoreColor, fontWeight: 600, fontSize: 15 }}>
              {score >= 70 ? '🌟 Highly inclusive' : score >= 40 ? '⚠️ Improvements needed' : '🚨 Significant gaps'}
            </p>
            {result.summary && <p style={{ color: '#9590b8', fontSize: 14, marginTop: 14, lineHeight: 1.6, maxWidth: 500, margin: '14px auto 0' }}>{result.summary}</p>}
          </div>

          {/* 3 columns */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 }}>
            {result.strengths?.length > 0 && (
              <div className="card">
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, color: '#00d4a4', marginBottom: 14 }}>✓ Strengths</h3>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {result.strengths.map((s, i) => (
                    <li key={i} style={{ fontSize: 13, color: '#9590b8', display: 'flex', gap: 8 }}>
                      <span style={{ color: '#00d4a4', flexShrink: 0 }}>•</span>{s}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {result.gaps?.length > 0 && (
              <div className="card">
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, color: '#ff6b6b', marginBottom: 14 }}>⚠ Gaps</h3>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {result.gaps.map((g, i) => (
                    <li key={i} style={{ fontSize: 13, color: '#9590b8', display: 'flex', gap: 8 }}>
                      <span style={{ color: '#ff6b6b', flexShrink: 0 }}>•</span>{g}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {result.recommendations?.length > 0 && (
              <div className="card">
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 15, color: '#a688ff', marginBottom: 14 }}>💡 Recommendations</h3>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {result.recommendations.map((r, i) => (
                    <li key={i} style={{ fontSize: 13, color: '#9590b8', display: 'flex', gap: 8 }}>
                      <span style={{ color: '#a688ff', flexShrink: 0 }}>→</span>{r}
                    </li>
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