# 세종시 제21대 대선 개표 분석 - 웹사이트

> 현대적이고 세련된 웹 인터페이스로 만나는 선거 데이터 분석

[![Next.js](https://img.shields.io/badge/Next.js-16.0-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.1-38bdf8)](https://tailwindcss.com/)

## 🌟 특징

- ✨ **현대적인 디자인**: 그라데이션, 애니메이션, 글래스모피즘 효과
- 📱 **완전 반응형**: 모바일, 태블릿, 데스크톱 최적화
- ⚡ **빠른 성능**: Next.js 16 App Router + Static Export
- 🎨 **Tailwind CSS**: 유틸리티 우선 CSS 프레임워크
- 🚀 **즉시 배포 가능**: Vercel, Netlify, GitHub Pages

## 🛠️ 기술 스택

- **프레임워크**: Next.js 16 (App Router)
- **언어**: TypeScript 5.9
- **스타일링**: Tailwind CSS 4.1
- **배포**: Vercel (권장)

## 📦 설치 및 실행

### 1. 의존성 설치

```bash
npm install
```

### 2. 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:3000 을 열어 확인하세요.

### 3. 프로덕션 빌드

```bash
npm run build
```

정적 파일이 `out/` 디렉토리에 생성됩니다.

## 🚀 배포

### Vercel (권장)

1. GitHub 저장소에 푸시
2. [Vercel](https://vercel.com)에 가입
3. "New Project" 클릭
4. GitHub 저장소 선택
5. Root Directory를 `k21election-web`로 설정
6. Deploy 클릭

자동으로 배포되며, URL이 제공됩니다.

### GitHub Pages

```bash
npm run build
```

`out/` 폴더의 내용을 GitHub Pages 저장소에 푸시하세요.

### Netlify

1. [Netlify](https://netlify.com)에 가입
2. "Add new site" → "Import from Git"
3. 저장소 선택
4. Build command: `npm run build`
5. Publish directory: `out`
6. Deploy

## 📁 프로젝트 구조

```
k21election-web/
├── app/
│   ├── layout.tsx          # 루트 레이아웃
│   ├── page.tsx            # 메인 페이지
│   └── globals.css         # 글로벌 스타일
├── public/                 # 정적 파일
├── next.config.js          # Next.js 설정
├── tailwind.config.ts      # Tailwind 설정
├── tsconfig.json           # TypeScript 설정
└── package.json
```

## 🎨 디자인 특징

### 색상 팔레트

- **Primary**: 보라색 (#667eea, #764ba2)
- **Candidates**:
  - 이재명: 파란색 (#1976D2)
  - 김문수: 빨간색 (#D32F2F)
  - 이준석: 주황색 (#F57C00)
  - 권영국: 보라색 (#7B1FA2)
  - 송진호: 녹색 (#558B2F)

### 애니메이션

- **Blob Animation**: 배경 그라데이션 효과
- **Fade In**: 히어로 텍스트 애니메이션
- **Bounce**: 스크롤 다운 화살표
- **Hover Effects**: 카드 호버 시 그림자 효과

## 📱 반응형 브레이크포인트

```css
sm: 640px   /* 모바일 가로 */
md: 768px   /* 태블릿 */
lg: 1024px  /* 데스크톱 */
xl: 1280px  /* 대형 데스크톱 */
```

## 🔗 링크

- **GitHub 저장소**: https://github.com/sechan9999/k21election
- **Velog 블로그**: https://velog.io/@tcgyver
- **분석 문서**: [README.md](../README.md)

## 📝 라이선스

MIT License

## 👨‍💻 개발자

분석: Claude Sonnet 4.5 (Anthropic AI)
날짜: 2025년 11월

---

**이 웹사이트는 AI가 분석한 세종시 제21대 대통령선거 개표 데이터를 시각화합니다.**
