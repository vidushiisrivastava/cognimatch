'use client'
import { useState } from 'react'

interface BiasResult {
  bias_score: number
  flagged_phrases: Array<{ phrase: string; reason: string; replacement: string; severity: string }>
  rewritten_jd: string
  summary: string
}

const SAMPLE_JD = `We're looking for a rockstar developer who thrives in a fast-paced environment. The ideal candidate must be thick-skinned, able to handle pressure and aggressive deadlines. We need a ninja who can hit the ground running and crush it from day one. Must have no fear of failure and be willing to work crazy hours when needed.`

export default function BiasScanPage() {
  const [jd, setJd] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<BiasResult | null>(null)
  const [error, setError] = useState('')

  const scanJD = async () => {
    if (!jd.trim()) return
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const res = await fetch('http://localhost:8000/api/bias-scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_description: jd }),
      })
      if (!res.ok) throw new Error('API error')
      const data = await res.json()
      setResult(data)
    } catch {
      setError('Could not connect to the AI engine. Make sure the FastAPI server is running on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  const scoreColor = result
    ? result.bias_score > 60 ? '#ff6b6b' : result.bias_score > 30 ? '#ffb347' : '#00d4a4'
    : '#7c5cfc'

  const severityColor = (s: string) =>
    s === 'high' ? '#ff6b6b' : s === 'medium' ? '#ffb347' : '#00d4a4'

  return (
    <div style={{ maxWidth: 860, margin: '0 auto', padding: '48px 24px' }}>
      {/* Header */}
      <div style={{ marginBottom: 40 }}>
        <div className="badge badge-coral" style={{ marginBottom: 14 }}>🚩 bias_scanner.py</div>
        <h1 style={{ fontFamily: 'Syne, sans-serif', fontSize: 36, marginBottom: 10 }}>JD bias scanner</h1>
        <p style={{ color: '#9590b8', fontSize: 15 }}>
          Detect exclusionary language that filters out neurodivergent talent — before you post.
        </p>
      </div>

      {/* Input */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <label className="label" style={{ margin: 0 }}>Job description</label>
          <button
            onClick={() => setJd(SAMPLE_JD)}
            style={{ fontSize: 12, color: '#7c5cfc', background: 'none', border: 'none', cursor: 'pointer', fontFamily: 'DM Sans, sans-serif' }}>
            Use sample JD
          </button>
        </div>
        <textarea
          className="textarea"
          placeholder="Paste your job description here..."
          value={jd}
          onChange={e => setJd(e.target.value)}
          rows={7}
        />
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 14 }}>
          <button className="btn-primary" onClick={scanJD} disabled={loading || !jd.trim()}
            style={{ opacity: loading || !jd.trim() ? 0.6 : 1 }}>
            {loading ? <><span className="spinner" /> Scanning...</> : '🚩 Scan for bias →'}
          </button>
        </div>
      </div>

      {error && (
        <div style={{ background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.25)', borderRadius: 10, padding: '14px 18px', color: '#ff6b6b', fontSize: 14, marginBottom: 20 }}>
          ⚠️ {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="fade-up">
          {/* Score cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 14, marginBottom: 24 }}>
            <div className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 11, color: '#5a5570', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>Bias score</div>
              <div style={{ fontSize: 40, fontWeight: 800, fontFamily: 'Syne, sans-serif', color: scoreColor, lineHeight: 1 }}>{result.bias_score}</div>
              <div style={{ fontSize: 12, color: scoreColor, marginTop: 4 }}>
                {result.bias_score > 60 ? 'High risk' : result.bias_score > 30 ? 'Moderate' : 'Low risk'}
              </div>
            </div>
            <div className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 11, color: '#5a5570', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 8 }}>Phrases flagged</div>
              <div style={{ fontSize: 40, fontWeight: 800, fontFamily: 'Syne, sans-serif', color: '#f0effe', lineHeight: 1 }}>{result.flagged_phrases?.length ?? 0}</div>
              <div style={{ fontSize: 12, color: '#9590b8', marginTop: 4 }}>in this JD</div>
            </div>
          </div>

          {/* Summary */}
          {result.summary && (
            <div style={{ background: 'rgba(124,92,252,0.08)', border: '1px solid rgba(124,92,252,0.2)', borderRadius: 12, padding: '16px 20px', marginBottom: 20, fontSize: 14, color: '#c4bef5', lineHeight: 1.7 }}>
              {result.summary}
            </div>
          )}

          {/* Flagged phrases */}
          {result.flagged_phrases?.length > 0 && (
            <div className="card" style={{ marginBottom: 20 }}>
              <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 16, marginBottom: 18 }}>Flagged phrases</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                {result.flagged_phrases.map((f, i) => (
                  <div key={i} style={{ display: 'flex', gap: 14, padding: '14px', background: '#1a1a24', borderRadius: 10 }}>
                    <span style={{
                      background: severityColor(f.severity) + '20',
                      color: severityColor(f.severity),
                      border: `1px solid ${severityColor(f.severity)}40`,
                      borderRadius: 99, padding: '3px 10px', fontSize: 11, fontWeight: 600,
                      height: 'fit-content', whiteSpace: 'nowrap', marginTop: 2,
                    }}>{f.severity}</span>
                    <div>
                      <div style={{ fontWeight: 600, color: '#f0effe', marginBottom: 4, fontSize: 14 }}>"{f.phrase}"</div>
                      <div style={{ fontSize: 13, color: '#9590b8', marginBottom: 6 }}>{f.reason}</div>
                      <div style={{ fontSize: 13, color: '#00d4a4' }}>✓ Try: "{f.replacement}"</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Rewritten JD */}
          {result.rewritten_jd && (
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 16 }}>✨ AI-rewritten (inclusive) JD</h3>
                <button
                  onClick={() => navigator.clipboard.writeText(result.rewritten_jd)}
                  style={{ fontSize: 12, color: '#7c5cfc', background: 'none', border: '1px solid rgba(124,92,252,0.3)', borderRadius: 6, padding: '5px 12px', cursor: 'pointer', fontFamily: 'DM Sans, sans-serif' }}>
                  Copy
                </button>
              </div>
              <div style={{ background: '#1a1a24', borderRadius: 10, padding: '16px', fontSize: 14, color: '#9590b8', lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>
                {result.rewritten_jd}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}