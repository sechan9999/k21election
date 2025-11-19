export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 text-white overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
          <div className="absolute top-40 right-20 w-72 h-72 bg-yellow-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
          <div className="absolute bottom-20 left-40 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
        </div>

        <div className="relative z-10 text-center px-6 max-w-5xl mx-auto">
          <h1 className="text-6xl md:text-7xl font-bold mb-6 animate-fade-in">
            🗳️ 세종시 제21대 대선<br />개표 분석
          </h1>
          <p className="text-xl md:text-2xl mb-4 text-gray-100">
            AI가 분석한 126페이지의 숨겨진 이야기
          </p>
          <p className="text-lg md:text-xl mb-12 text-gray-200">
            2시간 만에 개표상황표를 완전히 해부하다
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="#insights"
              className="px-8 py-4 bg-white text-purple-700 rounded-lg font-semibold text-lg hover:bg-gray-100 transition shadow-lg"
            >
              핵심 인사이트 보기
            </a>
            <a
              href="https://github.com/sechan9999/k21election"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-transparent border-2 border-white text-white rounded-lg font-semibold text-lg hover:bg-white hover:text-purple-700 transition"
            >
              GitHub 바로가기
            </a>
          </div>
        </div>

        <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition">
              <div className="text-5xl font-bold text-blue-600 mb-2">126</div>
              <div className="text-gray-600">분석 페이지</div>
            </div>
            <div className="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition">
              <div className="text-5xl font-bold text-purple-600 mb-2">97%</div>
              <div className="text-gray-600">기계 분류 정확도</div>
            </div>
            <div className="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition">
              <div className="text-5xl font-bold text-indigo-600 mb-2">5명</div>
              <div className="text-gray-600">대통령 후보자</div>
            </div>
            <div className="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition">
              <div className="text-5xl font-bold text-pink-600 mb-2">2시간</div>
              <div className="text-gray-600">분석 소요 시간</div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Insights Section */}
      <section id="insights" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">
            💡 핵심 발견사항
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Insight 1 */}
            <div className="p-8 bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl hover:shadow-xl transition">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-2xl font-bold mb-4 text-gray-900">이중 검증 시스템</h3>
              <p className="text-gray-700 leading-relaxed">
                기계 분류(97%) + 인간 검증(3%)의 완벽한 조화.
                최종 집계는 양쪽 결과를 모두 합산하여 정확성을 보장합니다.
              </p>
            </div>

            {/* Insight 2 */}
            <div className="p-8 bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl hover:shadow-xl transition">
              <div className="text-4xl mb-4">✓</div>
              <h3 className="text-2xl font-bold mb-4 text-gray-900">4중 검증 프로세스</h3>
              <p className="text-gray-700 leading-relaxed">
                투표용지 대조, 불일치 추적, 8명 위원 검증, 타임스탬프 기록.
                데이터 품질에 대한 철저한 집착이 돋보입니다.
              </p>
            </div>

            {/* Insight 3 */}
            <div className="p-8 bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-2xl hover:shadow-xl transition">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-2xl font-bold mb-4 text-gray-900">완전한 투명성</h3>
              <p className="text-gray-700 leading-relaxed">
                각 페이지는 하나의 투표함 결과를 완전히 문서화.
                모든 단계가 추적 가능하고 검증 가능합니다.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Candidates Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">
            👥 대통령 후보자
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            {[
              { num: 1, name: '이재명', party: '더불어민주당', color: 'bg-blue-600' },
              { num: 2, name: '김문수', party: '국민의힘', color: 'bg-red-600' },
              { num: 4, name: '이준석', party: '개혁신당', color: 'bg-orange-600' },
              { num: 5, name: '권영국', party: '민주노동당', color: 'bg-purple-600' },
              { num: 8, name: '송진호', party: '무소속', color: 'bg-green-600' },
            ].map((candidate) => (
              <div key={candidate.num} className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition text-center">
                <div className={`w-16 h-16 ${candidate.color} text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4`}>
                  {candidate.num}
                </div>
                <h3 className="text-xl font-bold mb-2 text-gray-900">{candidate.name}</h3>
                <p className="text-gray-600 text-sm">{candidate.party}</p>
              </div>
            ))}
          </div>

          <div className="mt-8 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
            <p className="text-gray-700">
              ⚠️ <strong>주의:</strong> 후보 번호 3, 6, 7은 존재하지 않습니다.
            </p>
          </div>
        </div>
      </section>

      {/* Technical Stack Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">
            🛠️ 기술 스택
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 border-2 border-gray-200 rounded-xl hover:border-purple-400 transition">
              <h3 className="text-xl font-bold mb-4 text-gray-900">🐍 데이터 처리</h3>
              <ul className="space-y-2 text-gray-700">
                <li>• Python 3.12</li>
                <li>• PyPDF2</li>
                <li>• pdf2image</li>
                <li>• Tesseract OCR (한글)</li>
              </ul>
            </div>

            <div className="p-6 border-2 border-gray-200 rounded-xl hover:border-purple-400 transition">
              <h3 className="text-xl font-bold mb-4 text-gray-900">📊 시각화</h3>
              <ul className="space-y-2 text-gray-700">
                <li>• matplotlib</li>
                <li>• Pillow</li>
                <li>• 고해상도 다이어그램</li>
                <li>• 색상 코딩 시스템</li>
              </ul>
            </div>

            <div className="p-6 border-2 border-gray-200 rounded-xl hover:border-purple-400 transition">
              <h3 className="text-xl font-bold mb-4 text-gray-900">🤖 AI 분석</h3>
              <ul className="space-y-2 text-gray-700">
                <li>• Claude Sonnet 4.5</li>
                <li>• 문서 구조 분석</li>
                <li>• 패턴 인식</li>
                <li>• 인사이트 추출</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="py-20 bg-gradient-to-br from-purple-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">
            📋 분석 프로세스
          </h2>

          <div className="space-y-8">
            {[
              { step: 1, title: 'PDF 이미지 변환', desc: '126페이지를 고해상도 PNG로 변환 (150 DPI)', icon: '📄' },
              { step: 2, title: '한글 OCR 처리', desc: 'Tesseract 한글팩으로 텍스트 추출', icon: '🔍' },
              { step: 3, title: '표 구조 인식', desc: '좌측(기계) vs 우측(최종) 테이블 구분', icon: '📊' },
              { step: 4, title: '데이터 검증', desc: '불일치 추적 및 품질 확인', icon: '✓' },
              { step: 5, title: '최종 집계', desc: '후보별/유형별 통합 분석', icon: '📈' },
            ].map((process) => (
              <div key={process.step} className="flex items-start gap-6 p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition">
                <div className="flex-shrink-0 w-16 h-16 bg-gradient-to-br from-purple-600 to-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">
                  {process.step}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-3xl">{process.icon}</span>
                    <h3 className="text-2xl font-bold text-gray-900">{process.title}</h3>
                  </div>
                  <p className="text-gray-700">{process.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-purple-600 to-blue-600 text-white">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-8">
            더 자세한 분석이 궁금하신가요?
          </h2>
          <p className="text-xl mb-12 text-gray-100">
            GitHub 저장소에서 전체 문서와 데이터를 확인하실 수 있습니다.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="https://github.com/sechan9999/k21election"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-white text-purple-700 rounded-lg font-semibold text-lg hover:bg-gray-100 transition shadow-lg"
            >
              📦 GitHub 저장소
            </a>
            <a
              href="https://velog.io/@tcgyver"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-transparent border-2 border-white rounded-lg font-semibold text-lg hover:bg-white hover:text-purple-700 transition"
            >
              ✍️ Velog 블로그
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <h3 className="text-xl font-bold mb-4">K21 Election</h3>
              <p className="text-gray-400">
                세종시 제21대 대선 개표 분석 프로젝트
              </p>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-4">문서</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="https://github.com/sechan9999/k21election/blob/main/README.md" className="hover:text-white transition">README</a></li>
                <li><a href="https://github.com/sechan9999/k21election/blob/main/sejong_election_data_analysis.md" className="hover:text-white transition">상세 분석</a></li>
                <li><a href="https://github.com/sechan9999/k21election/blob/main/quick_reference_guide.md" className="hover:text-white transition">빠른 참조</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-xl font-bold mb-4">리소스</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="https://github.com/sechan9999/k21election" className="hover:text-white transition">GitHub</a></li>
                <li><a href="https://velog.io/@tcgyver" className="hover:text-white transition">Velog</a></li>
                <li><span className="text-gray-500">Claude Sonnet 4.5 (Anthropic AI)</span></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
            <p>© 2025 K21 Election Analysis. AI-powered by Claude Sonnet 4.5</p>
            <p className="mt-2 text-sm">분석 시간: 약 2시간 | 생성일: 2025년 11월</p>
          </div>
        </div>
      </footer>
    </main>
  )
}
