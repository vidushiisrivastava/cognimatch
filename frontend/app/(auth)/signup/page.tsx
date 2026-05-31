'use client'
import { useState } from 'react'
import Link from 'next/link'

const roles = [
  { id: 'candidate', label: 'Job seeker', desc: 'Find the right workplace fit', icon: '🧠' },
  { id: 'hr', label: 'HR / Hiring', desc: 'Hire more inclusively', icon: '🏢' },
]

export default function SignupPage() {
  const [role, setRole] = useState('candidate')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setTimeout(() => { window.location.href = role === 'candidate' ? '/onboarding' : '/culture' }, 1000)
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '40px 24px' }}>
      <div style={{ width: '100%', maxWidth: 440, position: 'relative', zIndex: 1 }}>
        <div style={{ textAlign: 'center', marginBottom: 36 }}>
          <div style={{ width: 48, height: 48, borderRadius: 12, margin: '0 auto 16px', background: 'linear-gradient(135deg, #7c5cfc, #00d4a4)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 24 }}>🧠</div>
          <h1 style={{ fontFamily: 'Syne, sans-serif', fontSize: 24, marginBottom: 6 }}>Create your account</h1>
          <p style={{ color: '#9590b8', fontSize: 14 }}>No diagnosis required. No labels.</p>
        </div>
        <div className="card-glow">
          <div style={{ marginBottom: 24 }}>
            <label className="label">I am a...</label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
              {roles.map(r => (
                <button key={r.id} type="button" onClick={() => setRole(r.id)} style={{ background: role === r.id ? 'rgba(124,92,252,0.15)' : '#1a1a24', border: `1px solid ${role === r.id ? '#7c5cfc' : 'rgba(255,255,255,0.06)'}`, borderRadius: 10, padding: '14px 12px', cursor: 'pointer', textAlign: 'left', transition: 'all 0.15s' }}>
                  <div style={{ fontSize: 20, marginBottom: 6 }}>{r.icon}</div>
                  <div style={{ fontFamily: 'Syne, sans-serif', fontSize: 13, fontWeight: 600, color: '#f0effe', marginBottom: 3 }}>{r.label}</div>
                  <div style={{ fontSize: 11, color: '#9590b8' }}>{r.desc}</div>
                </button>
              ))}
            </div>
          </div>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: 16 }}>
              <label className="label">Full name</label>
              <input className="input" type="text" placeholder="Your name" value={name} onChange={e => setName(e.target.value)} required />
            </div>
            <div style={{ marginBottom: 16 }}>
              <label className="label">Email</label>
              <input className="input" type="email" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} required />
            </div>
            <div style={{ marginBottom: 24 }}>
              <label className="label">Password</label>
              <input className="input" type="password" placeholder="Min 8 characters" value={password} onChange={e => setPassword(e.target.value)} required />
            </div>
            <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', padding: '13px' }}>
              {loading ? <span className="spinner" /> : 'Create account →'}
            </button>
          </form>
          <div className="divider" />
          <p style={{ textAlign: 'center', fontSize: 14, color: '#9590b8' }}>
            Already have an account? <Link href="/login" style={{ color: '#a688ff', fontWeight: 500 }}>Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}