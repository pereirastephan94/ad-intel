import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Ad Intel — Competitor Ad Analysis',
  description: 'Monitor competitor Facebook ads. Understand their strategy. Never miss a new creative.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
