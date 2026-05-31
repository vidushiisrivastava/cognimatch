import type { Metadata } from 'next'
import './globals.css'
import Navbar from './components/Navbar'

export const metadata: Metadata = {
  title: 'CogniMatch — Inclusive Hiring AI',
  description: 'AI-powered hiring platform for neurodivergent talent',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main style={{ minHeight: '100vh', paddingTop: '64px', position: 'relative', zIndex: 1 }}>
          {children}
        </main>
      </body>
    </html>
  )
}