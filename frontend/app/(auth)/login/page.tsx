'use client'
import { useState } from 'react'
import Link from 'next/link'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setTimeout(() => { window.location.href = '/dashboard' }, 1000)
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '40px 24px' }}>
      <div style={{ width: '100%', maxWidth: 400, position: 'relative', zIndex: 1 }}>
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <div style={{ width: 48, height: 48, borderRadius: 12, margin: '0 auto 16px', background: 'linear-gradient(135deg, #7c5cfc, #00d4a4)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 24 }}>🧠</div>
          <h1 style={{ fontFamily: 'Syne, sans-serif', fontSize: 24, marginBottom: 6 }}>Welcome back</h1>
          <p style={{ color: '#9590b8', fontSize: 14 }}>Sign in to your CogniMatch account</p>
        </div>
        <div className="card-glow">
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: 20 }}>
              <label className="label">Email address</label>
              <input className="input" type="email" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} required />
            </div>
            <div style={{ marginBottom: 28 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <label className="label" style={{ margin: 0 }}>Password</label>
                <a href="#" style={{ fontSize: 12, color: '#7c5cfc' }}>Forgot password?</a>
              </div>
              <input className="input" type="password" placeholder="••••••••" value={password} onChange={e => setPassword(e.target.value)} required />
            </div>
            <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', padding: '13px' }}>
              {loading ? <span className="spinner" /> : 'Sign in →'}
            </button>
          </form>
          <div className="divider" />
          <p style={{ textAlign: 'center', fontSize: 14, color: '#9590b8' }}>
            No account? <Link href="/signup" style={{ color: '#a688ff', fontWeight: 500 }}>Sign up free</Link>
          </p>
        </div>
      </div>
    </div>
  )
}