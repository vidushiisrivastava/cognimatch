'use client'
import Link from 'next/link'

const features = [
  { icon: '🎯', title: 'Working style match', desc: 'Answer 5 questions about how you work. Get a % match with any job — powered by vector embeddings, not keywords.', color: '#7c5cfc', href: '/match', tag: 'match_score.py' },
  { icon: '🚩', title: 'JD bias scanner', desc: 'Paste any job description. AI flags exclusionary language like "rockstar", "fast-paced", and rewrites it inclusively.', color: '#ff6b6b', href: '/bias-scan', tag: 'bias_scanner.py' },
  { icon: '📊', title: 'Culture intelligence', desc: 'Describe your company. Get an inclusion score 0–100, strengths, gaps, and specific recommendations.', color: '#00d4a4', href: '/culture', tag: 'report.py' },
  { icon: '🧠', title: 'Candidate persona', desc: 'Answer 6 working style questions. Get a shareable neurodivergent professional profile with your strengths and ideal environment.', color: '#ffb347', href: '/onboarding', tag: 'cognimatch_ai.py' },
]

export default function Home() {
  return (
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: '0 24px' }}>

      {/* Hero */}
      <section style={{ textAlign: 'center', padding: '80px 0 64px', position: 'relative' }}>
        <div style={{
          position: 'absolute', top: '10%', left: '50%', transform: 'translateX(-50%)',
          width: 500, height: 300, borderRadius: '50%',
          background: 'radial-gradient(ellipse, rgba(124,92,252,0.12) 0%, transparent 70%)',
          pointerEvents: 'none',
        }}/>
        <div className="badge badge-purple" style={{ marginBottom: 24, display: 'inline-flex' }}>
        
        </div>
        <h1 style={{
          fontSize: 'clamp(40px, 7vw, 76px)',
          fontFamily: 'Syne, sans-serif', fontWeight: 800,
          lineHeight: 1.05, letterSpacing: '-0.03em', marginBottom: 24,
          background: 'linear-gradient(135deg, #f0effe 0%, #a688ff 50%, #00d4a4 100%)',
          WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
        }}>
          Hiring that fits<br/>how your brain works
        </h1>
        <p style={{ fontSize: 18, color: '#9590b8', maxWidth: 520, margin: '0 auto 40px', lineHeight: 1.7 }}>
          CogniMatch uses AI to match neurodivergent talent by working style — not resume keywords. No diagnosis required.
        </p>
        <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link href="/onboarding" className="btn-primary" style={{ fontSize: 15, padding: '14px 28px' }}>Get my persona →</Link>
          <Link href="/bias-scan" className="btn-secondary" style={{ fontSize: 15, padding: '14px 28px' }}>Scan a job description</Link>
        </div>
      </section>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 16, marginBottom: 80 }}>
        {[{ num: '4', label: 'AI models' }, { num: '10k+', label: 'Bias phrases found' }, { num: '92%', label: 'Retention boost' }, { num: '0', label: 'Diagnoses required' }].map(s => (
          <div key={s.label} style={{ background: '#111118', border: '1px solid rgba(255,255,255,0.06)', borderRadius: 12, padding: '20px 16px', textAlign: 'center' }}>
            <div style={{ fontSize: 32, fontWeight: 800, fontFamily: 'Syne, sans-serif', color: '#a688ff', lineHeight: 1 }}>{s.num}</div>
            <div style={{ fontSize: 12, color: '#5a5570', marginTop: 6, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Features */}
      <section style={{ marginBottom: 80 }}>
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <h2 style={{ fontSize: 36, fontFamily: 'Syne, sans-serif', marginBottom: 12 }}>4 AI features</h2>
          <p style={{ color: '#9590b8' }}>Powered by LLaMA 3.3 70B via Groq + sentence transformers</p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 20 }}>
          {features.map(f => (
            <Link key={f.href} href={f.href} style={{ textDecoration: 'none' }}>
              <div style={{
                background: '#111118', border: '1px solid rgba(255,255,255,0.06)',
                borderRadius: 16, padding: '28px 24px', height: '100%',
                transition: 'all 0.2s', cursor: 'pointer',
              }}
              onMouseEnter={e => { const el = e.currentTarget; el.style.borderColor = f.color + '40'; el.style.transform = 'translateY(-2px)'; el.style.boxShadow = `0 0 40px ${f.color}20` }}
              onMouseLeave={e => { const el = e.currentTarget; el.style.borderColor = 'rgba(255,255,255,0.06)'; el.style.transform = 'none'; el.style.boxShadow = 'none' }}>
                <div style={{ fontSize: 32, marginBottom: 16 }}>{f.icon}</div>
                <h3 style={{ fontFamily: 'Syne, sans-serif', fontSize: 18, marginBottom: 10, color: '#f0effe' }}>{f.title}</h3>
                <p style={{ fontSize: 14, color: '#9590b8', lineHeight: 1.6, marginBottom: 16 }}>{f.desc}</p>
                <div style={{ fontFamily: 'monospace', fontSize: 11, color: '#5a5570', background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 99, padding: '3px 10px', display: 'inline-block' }}>{f.tag}</div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section style={{ textAlign: 'center', padding: '60px 40px', background: 'linear-gradient(135deg, rgba(124,92,252,0.1), rgba(0,212,164,0.08))', border: '1px solid rgba(124,92,252,0.2)', borderRadius: 20, marginBottom: 80 }}>
        <h2 style={{ fontSize: 32, fontFamily: 'Syne, sans-serif', marginBottom: 12 }}>Ready to find your fit?</h2>
        <p style={{ color: '#9590b8', marginBottom: 28 }}>No diagnosis required. No labels. Just your working style.</p>
        <Link href="/signup" className="btn-primary" style={{ fontSize: 15, padding: '14px 32px' }}>Start for free →</Link>
      </section>
    </div>
  )
}