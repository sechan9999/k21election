# 선거 데이터 소스 및 다운로드 가이드

제21대 대통령선거 개표상황표 데이터 다운로드 방법

---

## 📥 빠른 시작

### 자동 다운로드 (권장)

```bash
# gdown 설치
pip install gdown requests

# 세종시 데이터
python download_data.py --city sejong

# 제주시 데이터
python download_data.py --city jeju

# 페이지 이미지 포함
python download_data.py --city jeju --include-pages

# 다운로드 검증
python download_data.py --verify
```

---

## 🌐 데이터 소스

### 현재 사용 가능

#### 1. GitHub (직접 액세스)
- **세종시 PDF**: [sejong.pdf](https://github.com/sechan9999/k21election/raw/main/sejong.pdf) (3.7MB)
- **제주시 PDF**: [jeju.pdf](https://github.com/sechan9999/k21election/raw/main/jeju.pdf) (8.6MB)

다운로드:
```bash
# wget
wget https://github.com/sechan9999/k21election/raw/main/sejong.pdf
wget https://github.com/sechan9999/k21election/raw/main/jeju.pdf

# curl
curl -L -o sejong.pdf https://github.com/sechan9999/k21election/raw/main/sejong.pdf
curl -L -o jeju.pdf https://github.com/sechan9999/k21election/raw/main/jeju.pdf

# 스크립트
python download_data.py --city sejong --github
```

#### 2. Google Drive (대용량 데이터)

**설정 필요**: `download_data.py`에서 파일 ID 업데이트 필요

Google Drive에 업로드 후:
1. 파일 우클릭 → "공유" → "링크가 있는 모든 사용자"
2. 링크 복사: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
3. `FILE_ID` 추출
4. `download_data.py`의 `DATASETS` 딕셔너리 업데이트

```python
DATASETS = {
    'sejong': {
        'pdf_id': 'YOUR_ACTUAL_FILE_ID_HERE',  # 여기에 실제 ID 입력
        ...
    }
}
```

#### 3. Zenodo (학술용, DOI 발급)

**준비 중**

향후 Zenodo에 업로드 예정:
- DOI 발급으로 영구 인용 가능
- 50GB 무료 스토리지
- 무제한 다운로드

---

## 📦 데이터 구조

### 다운로드 후 디렉토리 구조

```
k21election/
├── data/
│   ├── sejong/
│   │   ├── sejong.pdf (3.7MB)
│   │   └── pages/ (126개 PNG, 선택사항)
│   │       ├── page_001.png
│   │       ├── page_002.png
│   │       └── ...
│   └── jeju/
│       ├── jeju.pdf (8.6MB)
│       └── pages/ (172개 PNG, 선택사항)
│           ├── page_001.png
│           ├── page_002.png
│           └── ...
├── scripts/
│   └── ... (분석 스크립트)
└── results/
    └── ... (분석 결과)
```

---

## 📊 데이터 세부 정보

### 세종시
- **파일명**: sejong.pdf
- **크기**: 3.7MB
- **페이지**: 126페이지
- **추출 이미지**: 35MB (126개 PNG)
- **추정 선거인**: ~250,000명
- **투표함**: ~180개

### 제주시
- **파일명**: jeju.pdf
- **크기**: 8.6MB
- **페이지**: 172페이지
- **추출 이미지**: 69MB (172개 PNG)
- **추정 선거인**: ~350,000명
- **투표함**: ~230개

---

## 🔧 수동 다운로드

### 방법 1: 브라우저
1. GitHub 저장소 방문
2. 파일 클릭 (예: `sejong.pdf`)
3. "Download" 버튼 클릭

### 방법 2: Git Clone
```bash
# 전체 저장소 클론
git clone https://github.com/sechan9999/k21election.git
cd k21election

# PDF 파일은 Git LFS로 관리될 수 있음
git lfs pull
```

### 방법 3: 직접 URL
```bash
# 브라우저에서 직접 열기
https://github.com/sechan9999/k21election/blob/main/sejong.pdf

# 직접 다운로드 URL
https://github.com/sechan9999/k21election/raw/main/sejong.pdf
```

---

## ✅ 데이터 검증

### 파일 크기 확인
```bash
# 예상 크기
ls -lh data/sejong/sejong.pdf  # ~3.7MB
ls -lh data/jeju/jeju.pdf      # ~8.6MB
```

### 페이지 수 확인
```python
import fitz  # PyMuPDF

doc = fitz.open('data/sejong/sejong.pdf')
print(f"세종시 페이지: {len(doc)}")  # 126

doc = fitz.open('data/jeju/jeju.pdf')
print(f"제주시 페이지: {len(doc)}")  # 172
```

### 자동 검증
```bash
python download_data.py --verify
```

예상 출력:
```
다운로드 파일 검증
================================================================================

SEJONG:
  PDF: ✓ data/sejong/sejong.pdf
       크기: 3.70 MB

JEJU:
  PDF: ✓ data/jeju/jeju.pdf
       크기: 8.60 MB
  페이지: ✓ 172개
```

---

## 🚀 빠른 분석 시작

### 1. 데이터 다운로드
```bash
python download_data.py --city sejong
python download_data.py --city jeju
```

### 2. 페이지 추출
```bash
python multiprocess_pdf_extractor.py data/sejong/sejong.pdf data/sejong/pages 150
python multiprocess_pdf_extractor.py data/jeju/jeju.pdf data/jeju/pages 150
```

### 3. 분석 실행
```bash
python analyze_city_comparison.py data/sejong/pages data/jeju/pages
```

---

## 🔗 외부 링크

### GitHub 저장소
- **메인**: https://github.com/sechan9999/k21election
- **브랜치**: claude/analyze-ocr-html-data-01XMPg3BASF9rYFZFEpbDS4Z

### 관련 문서
- [DATA_SHARING_STRATEGIES.md](DATA_SHARING_STRATEGIES.md) - 대용량 데이터 공유 전략
- [README_MULTIPROCESSING.md](README_MULTIPROCESSING.md) - 멀티프로세싱 가이드
- [jeju_data/README.md](jeju_data/README.md) - 제주 데이터 문서

---

## ❓ 문제 해결

### Q1: "gdown 설치 실패"
```bash
pip install --upgrade pip
pip install gdown
```

### Q2: "Google Drive 다운로드 실패"
```bash
# GitHub에서 직접 다운로드 사용
python download_data.py --city sejong --github
```

### Q3: "파일이 손상됨"
```bash
# 파일 재다운로드
rm data/sejong/sejong.pdf
python download_data.py --city sejong
```

### Q4: "페이지 이미지가 필요 없음"
```bash
# PDF만 다운로드 (기본 동작)
python download_data.py --city sejong
# --include-pages 옵션 생략
```

---

## 📝 향후 계획

### 추가 예정 데이터 소스

1. **Zenodo** (학술용)
   - DOI 발급 예정
   - 전체 데이터셋 (1~2GB)
   - 영구 보존

2. **Kaggle Datasets**
   - 데이터 과학 커뮤니티 공유
   - Kaggle API 지원
   - 버전 관리

3. **전국 17개 시도**
   - 서울, 부산, 인천, 대구, 광주, 대전, 울산
   - 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주
   - 세종 (완료), 제주시 (완료)

---

## 📧 문의

- **GitHub Issues**: https://github.com/sechan9999/k21election/issues
- **Repository**: https://github.com/sechan9999/k21election

---

**최종 업데이트**: 2025-11-19
