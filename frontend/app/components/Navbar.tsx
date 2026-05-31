'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'

const links = [
  { href: '/match',     label: 'Match score' },
  { href: '/bias-scan', label: 'Bias scanner' },
  { href: '/culture',   label: 'Culture report' },
  { href: '/onboarding',label: 'Get my persona' },
]

export default function Navbar() {
  const path = usePathname()
  const [open, setOpen] = useState(false)

  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
      height: '64px', display: 'flex', alignItems: 'center',
      padding: '0 24px', justifyContent: 'space-between',
      background: 'rgba(10,10,15,0.85)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid rgba(255,255,255,0.06)',
    }}>
      {/* Logo */}
      <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
        <div style={{
          width: 32, height: 32, borderRadius: 8,
          background: 'linear-gradient(135deg, #7c5cfc, #00d4a4)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 16,
        }}>🧠</div>
        <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: 18, color: '#f0effe', letterSpacing: '-0.01em' }}>
          CogniMatch
        </span>
      </Link>

      {/* Desktop links */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }} className="desktop-nav">
        {links.map(l => (
          <Link key={l.href} href={l.href} style={{
            padding: '6px 14px',
            borderRadius: 8,
            fontSize: 13,
            fontWeight: 500,
            color: path === l.href ? '#a688ff' : '#9590b8',
            background: path === l.href ? 'rgba(124,92,252,0.12)' : 'transparent',
            transition: 'all 0.15s',
            textDecoration: 'none',
          }}>{l.label}</Link>
        ))}
      </div>

      {/* Auth buttons */}
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
        <Link href="/login" style={{
          padding: '7px 16px', borderRadius: 8, fontSize: 13, fontWeight: 600,
          color: '#9590b8', border: '1px solid rgba(255,255,255,0.1)',
          background: 'transparent', cursor: 'pointer', textDecoration: 'none',
          fontFamily: 'Syne, sans-serif',
        }}>Login</Link>
        <Link href="/signup" style={{
          padding: '7px 16px', borderRadius: 8, fontSize: 13, fontWeight: 600,
          color: '#fff', background: '#7c5cfc', textDecoration: 'none',
          fontFamily: 'Syne, sans-serif',
        }}>Sign up</Link>
      </div>

      <style>{`
        @media (max-width: 768px) { .desktop-nav { display: none !important; } }
      `}</style>
    </nav>
  )
}