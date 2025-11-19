import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '세종시 제21대 대선 개표 분석 | K21 Election',
  description: 'AI로 분석한 세종특별자치시 제21대 대통령선거 개표상황표 - 126페이지의 숨겨진 이야기',
  keywords: ['선거', '개표', '세종시', '데이터 분석', 'AI', '대통령선거'],
  authors: [{ name: 'K21 Election Team' }],
  openGraph: {
    title: '세종시 제21대 대선 개표 분석',
    description: 'AI로 분석한 126페이지의 개표상황표',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ko">
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
