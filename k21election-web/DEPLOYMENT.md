# 배포 가이드

> 세종시 선거 분석 웹사이트를 배포하는 방법

## 🚀 Vercel 배포 (권장)

Vercel은 Next.js를 개발한 팀의 호스팅 플랫폼으로, 가장 쉽고 빠른 배포 방법입니다.

### 1단계: GitHub에 푸시

```bash
# 모든 변경사항 커밋
cd /home/user/k21election
git add k21election-web/
git commit -m "Add modern Next.js website"
git push origin claude/modern-homepage-setup-01KA9JN9ts6gCbUHh7Uqc3Bm
```

### 2단계: Vercel에 배포

1. **Vercel 계정 생성**
   - https://vercel.com 방문
   - GitHub 계정으로 로그인

2. **새 프로젝트 생성**
   - "Add New..." → "Project" 클릭
   - GitHub 저장소 `sechan9999/k21election` 선택

3. **프로젝트 설정**
   ```
   Framework Preset: Next.js
   Root Directory: k21election-web
   Build Command: npm run build (자동 감지)
   Output Directory: .next (자동 감지)
   Install Command: npm install (자동 감지)
   ```

4. **Deploy 클릭**
   - 약 2-3분 후 배포 완료
   - 자동으로 URL 생성 (예: `k21election-web.vercel.app`)

### 3단계: 도메인 설정 (선택사항)

1. Project Settings → Domains
2. 원하는 도메인 추가
3. DNS 레코드 설정 (Vercel이 안내)

---

## 📦 GitHub Pages 배포

무료로 정적 사이트를 호스팅할 수 있습니다.

### 1단계: 빌드

```bash
cd /home/user/k21election/k21election-web
npm run build
```

`out/` 디렉토리에 정적 파일이 생성됩니다.

### 2단계: GitHub Pages 설정

#### 방법 A: GitHub Actions (자동 배포)

`.github/workflows/deploy.yml` 파일 생성:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
    paths:
      - 'k21election-web/**'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd k21election-web
          npm install

      - name: Build
        run: |
          cd k21election-web
          npm run build

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./k21election-web/out
```

#### 방법 B: 수동 배포

```bash
# 빌드 파일을 gh-pages 브랜치에 푸시
cd /home/user/k21election/k21election-web
npm run build
cd out
git init
git add .
git commit -m "Deploy to GitHub Pages"
git branch -M gh-pages
git remote add origin https://github.com/sechan9999/k21election.git
git push -f origin gh-pages
```

### 3단계: GitHub Pages 활성화

1. GitHub 저장소 → Settings → Pages
2. Source: `gh-pages` 브랜치 선택
3. Save 클릭

URL: `https://sechan9999.github.io/k21election/`

---

## 🌐 Netlify 배포

### 1단계: Netlify 계정 생성

- https://netlify.com 방문
- GitHub 계정으로 로그인

### 2단계: 새 사이트 추가

1. "Add new site" → "Import an existing project"
2. GitHub 저장소 `sechan9999/k21election` 선택

### 3단계: 빌드 설정

```
Base directory: k21election-web
Build command: npm run build
Publish directory: k21election-web/out
```

### 4단계: Deploy

자동으로 배포되며 URL이 제공됩니다.

---

## ⚙️ 환경 변수 (필요시)

프로덕션에서 API 키 등이 필요한 경우:

### Vercel
1. Project Settings → Environment Variables
2. 키-값 추가

### Netlify
1. Site settings → Environment variables
2. 키-값 추가

### GitHub Pages
`.env.production` 파일은 빌드 시에만 사용됩니다.
민감한 정보는 포함하지 마세요.

---

## 🔧 빌드 문제 해결

### 문제: 빌드 실패

```bash
# 의존성 재설치
cd k21election-web
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 문제: TypeScript 에러

```bash
# TypeScript 타입 체크 무시 (권장하지 않음)
npm run build -- --no-lint
```

### 문제: 메모리 부족

```bash
# Node.js 메모리 증가
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

---

## 📊 배포 후 확인사항

- [ ] 모든 페이지가 정상적으로 로드되는가?
- [ ] 이미지가 올바르게 표시되는가?
- [ ] 링크가 모두 작동하는가?
- [ ] 모바일에서 정상적으로 보이는가?
- [ ] SEO 메타 태그가 올바른가?

---

## 🎯 추천 배포 방법 비교

| 플랫폼 | 난이도 | 속도 | 비용 | 자동 배포 |
|--------|--------|------|------|----------|
| **Vercel** | ⭐ 매우 쉬움 | ⚡ 매우 빠름 | 무료 | ✅ |
| **Netlify** | ⭐ 매우 쉬움 | ⚡ 빠름 | 무료 | ✅ |
| **GitHub Pages** | ⭐⭐ 보통 | 🐢 보통 | 무료 | ⚠️ 설정 필요 |

**권장**: Vercel (Next.js와 완벽 호환)

---

## 🔗 유용한 링크

- [Vercel 문서](https://vercel.com/docs)
- [Next.js 배포 가이드](https://nextjs.org/docs/deployment)
- [GitHub Pages 문서](https://docs.github.com/en/pages)
- [Netlify 문서](https://docs.netlify.com/)

---

**배포 후 문제가 있으시면 GitHub Issues에 등록해주세요!**
