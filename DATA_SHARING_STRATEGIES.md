# 대용량 선거 데이터 공유 및 분석 전략

GitHub 파일 크기 제한 문제 해결 방법

---

## ⚠️ GitHub 제한사항

### 기본 제한
- **단일 파일**: 100MB 이상 경고, 50MB 이상 권장하지 않음
- **저장소 크기**: 1GB 이하 권장, 5GB 경고
- **푸시 크기**: 한 번에 2GB까지
- **대역폭**: 월 100GB (무료 계정)

### 현재 상황
- 세종시: 126페이지, 35MB
- 제주시: 172페이지, 69MB
- **전국 17개 시도**: 약 2,000~3,000페이지, **1~2GB 예상**

---

## 🎯 해결 방법 (난이도별)

## 방법 1: Git LFS (Large File Storage) ⭐⭐⭐
**가장 권장되는 방법**

### 장점
- ✅ GitHub와 완벽히 통합
- ✅ 버전 관리 가능
- ✅ 클론 시 선택적 다운로드
- ✅ 대용량 파일 전용

### 제한
- 무료: 1GB 스토리지 + 1GB/월 대역폭
- 유료: $5/월 (50GB 스토리지 + 50GB 대역폭)

### 설치 및 사용

```bash
# 1. Git LFS 설치
# Ubuntu/Debian
sudo apt-get install git-lfs

# macOS
brew install git-lfs

# Windows
# https://git-lfs.github.com/ 에서 다운로드

# 2. 저장소에서 초기화
cd /home/user/k21election
git lfs install

# 3. 추적할 파일 패턴 지정
git lfs track "*.pdf"
git lfs track "*.png"
git lfs track "jeju_data/pages/*.png"
git lfs track "sejong_data/pages/*.png"

# 4. .gitattributes 커밋
git add .gitattributes
git commit -m "Add Git LFS tracking for PDF and PNG files"

# 5. 기존 파일을 LFS로 마이그레이션
git lfs migrate import --include="*.pdf,*.png"

# 6. 정상 푸시
git push origin <branch>
```

### LFS 파일 확인
```bash
# LFS 상태 확인
git lfs status

# LFS 파일 목록
git lfs ls-files

# LFS 스토리지 사용량
git lfs env
```

### 비용 최적화
```bash
# 필요한 파일만 다운로드
GIT_LFS_SKIP_SMUDGE=1 git clone <repo>

# 특정 파일만 가져오기
git lfs pull --include="jeju_data/*.pdf"
```

---

## 방법 2: 외부 클라우드 스토리지 + GitHub 링크 ⭐⭐⭐⭐⭐
**가장 실용적이고 경제적**

### A. Google Drive

#### 장점
- ✅ 무료 15GB
- ✅ 무제한 다운로드
- ✅ 쉬운 공유
- ✅ 웹 인터페이스

#### 사용 방법

```bash
# 1. Google Drive에 업로드
# - drive.google.com 접속
# - 폴더 생성: "K21_Election_Data"
# - PDF 파일들 업로드

# 2. 공유 링크 생성
# - 우클릭 → "링크 가져오기"
# - "링크가 있는 모든 사용자" 선택
# - 링크 복사

# 3. GitHub에 메타데이터 저장
```

**예시 구조:**
```
k21election/
├── data_links.md          # 다운로드 링크 모음
├── scripts/               # 분석 스크립트
├── results/               # 분석 결과만 (경량)
└── README.md
```

**data_links.md 예시:**
```markdown
# 선거 데이터 다운로드 링크

## 세종시
- PDF: https://drive.google.com/file/d/xxxxx/view?usp=sharing
- 페이지 이미지: https://drive.google.com/drive/folders/xxxxx

## 제주시
- PDF: https://drive.google.com/file/d/yyyyy/view?usp=sharing
- 페이지 이미지: https://drive.google.com/drive/folders/yyyyy

## 전체 데이터 (압축)
- 전국 17개 시도: https://drive.google.com/file/d/zzzzz/view
  - 크기: 1.5GB (압축)
  - 포함: 모든 PDF + 분석 결과
```

#### 자동 다운로드 스크립트
```python
# download_data.py
import gdown
import os

DATASETS = {
    'sejong': {
        'pdf': 'https://drive.google.com/uc?id=FILE_ID',
        'pages': 'https://drive.google.com/uc?id=FOLDER_ID'
    },
    'jeju': {
        'pdf': 'https://drive.google.com/uc?id=FILE_ID',
        'pages': 'https://drive.google.com/uc?id=FOLDER_ID'
    }
}

def download_dataset(city):
    """특정 도시 데이터 다운로드"""
    os.makedirs(f'{city}_data', exist_ok=True)

    # PDF 다운로드
    gdown.download(DATASETS[city]['pdf'],
                   f'{city}_data/{city}.pdf',
                   quiet=False)

    # 페이지 다운로드 (선택적)
    # gdown.download_folder(DATASETS[city]['pages'],
    #                       f'{city}_data/pages',
    #                       quiet=False)

if __name__ == "__main__":
    import sys
    city = sys.argv[1] if len(sys.argv) > 1 else 'sejong'
    download_dataset(city)
```

사용법:
```bash
pip install gdown
python download_data.py sejong
python download_data.py jeju
```

### B. Dropbox

```bash
# 공유 링크 생성 후 직접 다운로드 가능
# 예시: https://www.dropbox.com/s/xxxxx/sejong.pdf?dl=1
#       (dl=1로 변경하면 직접 다운로드)

wget "https://www.dropbox.com/s/xxxxx/sejong.pdf?dl=1" -O sejong.pdf
```

### C. OneDrive

```bash
# OneDrive 공유 링크 → 직접 다운로드 변환
# 원본: https://onedrive.live.com/embed?cid=xxxxx&resid=yyyyy
# 다운로드: https://onedrive.live.com/download?cid=xxxxx&resid=yyyyy
```

---

## 방법 3: 데이터 압축 및 분할 ⭐⭐⭐

### A. 고효율 압축

```bash
# 1. 7zip으로 최대 압축
sudo apt-get install p7zip-full

# 단일 압축
7z a -t7z -m0=lzma2 -mx=9 sejong_data.7z sejong_data/

# 결과: 69MB → 약 20~30MB (70% 압축률)

# 2. 압축 파일 분할 (50MB 단위)
7z a -v50m -t7z -mx=9 korea_election_data.7z data/

# 결과:
# korea_election_data.7z.001 (50MB)
# korea_election_data.7z.002 (50MB)
# korea_election_data.7z.003 (...)

# 3. Git에 커밋
git add *.7z.*
git commit -m "Add compressed election data"

# 4. 압축 해제 (사용자)
7z x korea_election_data.7z.001
```

### B. 이미지 최적화

```python
# optimize_images.py
from PIL import Image
import os
from pathlib import Path

def optimize_png(input_path, output_path, quality=85):
    """PNG 이미지 최적화"""
    img = Image.open(input_path)

    # RGB로 변환 (알파 채널 제거)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # JPEG로 저장 (품질 85%)
    img.save(output_path, 'JPEG', quality=quality, optimize=True)

def optimize_directory(input_dir, output_dir):
    """디렉토리 전체 최적화"""
    Path(output_dir).mkdir(exist_ok=True)

    total_before = 0
    total_after = 0

    for png_file in Path(input_dir).glob('*.png'):
        output_file = Path(output_dir) / f"{png_file.stem}.jpg"

        size_before = png_file.stat().st_size
        optimize_png(png_file, output_file, quality=85)
        size_after = output_file.stat().st_size

        total_before += size_before
        total_after += size_after

        print(f"{png_file.name}: {size_before/1024:.1f}KB → {size_after/1024:.1f}KB "
              f"({(1-size_after/size_before)*100:.1f}% 감소)")

    print(f"\n총 압축률: {total_before/1024/1024:.1f}MB → {total_after/1024/1024:.1f}MB "
          f"({(1-total_after/total_before)*100:.1f}% 감소)")

if __name__ == "__main__":
    optimize_directory('jeju_data/pages', 'jeju_data/pages_optimized')
```

사용:
```bash
python optimize_images.py

# 예상 결과:
# 69MB PNG → 15~20MB JPEG (70~75% 감소)
```

---

## 방법 4: 전용 데이터 호스팅 서비스 ⭐⭐⭐⭐

### A. Zenodo (학술 데이터 호스팅)

**장점:**
- ✅ 무료 50GB/데이터셋
- ✅ DOI 발급 (영구 인용 가능)
- ✅ 무제한 다운로드
- ✅ 학술 목적 최적

**사용 방법:**
1. https://zenodo.org/ 가입
2. "Upload" → "New upload"
3. 데이터셋 업로드 (PDF, 이미지 등)
4. 메타데이터 입력 (제목, 설명, 키워드)
5. "Publish" → DOI 받기

**예시:**
```
DOI: 10.5281/zenodo.1234567
Title: 제21대 대통령선거 개표상황표 데이터셋
Link: https://zenodo.org/record/1234567
```

GitHub README에 추가:
```markdown
## 데이터셋 다운로드

**Zenodo (권장)**
- DOI: 10.5281/zenodo.1234567
- 크기: 1.5GB (전국 17개 시도)
- 라이선스: CC BY 4.0
```

### B. Kaggle Datasets

**장점:**
- ✅ 무료 100GB
- ✅ 데이터 과학 커뮤니티
- ✅ Kaggle API 지원
- ✅ 버전 관리

**업로드:**
```bash
# 1. Kaggle CLI 설치
pip install kaggle

# 2. API 키 설정 (~/.kaggle/kaggle.json)

# 3. 데이터셋 생성
kaggle datasets init -p /path/to/data

# 4. metadata 수정 (dataset-metadata.json)

# 5. 업로드
kaggle datasets create -p /path/to/data
```

**다운로드:**
```bash
# GitHub README에 명시
kaggle datasets download -d username/korea-election-data

# Python에서
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
api.dataset_download_files('username/korea-election-data',
                           path='./data',
                           unzip=True)
```

### C. Hugging Face Datasets

**장점:**
- ✅ 무료 무제한
- ✅ AI/ML 커뮤니티
- ✅ 자동 버전 관리
- ✅ Python API

```python
# 업로드
from huggingface_hub import HfApi

api = HfApi()
api.upload_folder(
    folder_path="./election_data",
    repo_id="username/korea-election-data",
    repo_type="dataset"
)

# 다운로드
from datasets import load_dataset

dataset = load_dataset("username/korea-election-data")
```

---

## 방법 5: 자체 서버 호스팅 ⭐⭐

### A. GitHub Pages + 외부 링크

```bash
# docs/ 폴더에 다운로드 페이지 생성
mkdir -p docs
cat > docs/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>K21 선거 데이터</title>
</head>
<body>
    <h1>제21대 대통령선거 데이터</h1>
    <h2>다운로드</h2>
    <ul>
        <li><a href="https://drive.google.com/...">세종시 (35MB)</a></li>
        <li><a href="https://drive.google.com/...">제주시 (69MB)</a></li>
        <li><a href="https://drive.google.com/...">전체 (1.5GB)</a></li>
    </ul>
    <h2>문서</h2>
    <ul>
        <li><a href="./reports/sejong.html">세종시 분석</a></li>
        <li><a href="./reports/jeju.html">제주시 분석</a></li>
    </ul>
</body>
</html>
EOF

# GitHub Pages 활성화
# Settings → Pages → Source: main/docs
```

### B. 간단한 파일 서버

```python
# simple_server.py
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='./data', **kwargs)

if __name__ == '__main__':
    port = 8000
    print(f"서버 시작: http://localhost:{port}")
    HTTPServer(('', port), CustomHandler).serve_forever()
```

---

## 📊 방법 비교표

| 방법 | 무료 용량 | 대역폭 | 난이도 | 추천도 | 용도 |
|------|----------|--------|--------|--------|------|
| **Git LFS** | 1GB | 1GB/월 | ⭐⭐ | ⭐⭐⭐ | 중소 규모 |
| **Google Drive** | 15GB | 무제한 | ⭐ | ⭐⭐⭐⭐⭐ | 개인/팀 |
| **Dropbox** | 2GB | 제한 | ⭐ | ⭐⭐ | 소규모 |
| **OneDrive** | 5GB | 제한 | ⭐ | ⭐⭐⭐ | 중소 규모 |
| **Zenodo** | 50GB | 무제한 | ⭐⭐ | ⭐⭐⭐⭐ | 학술 연구 |
| **Kaggle** | 100GB | 무제한 | ⭐⭐ | ⭐⭐⭐⭐ | 데이터 과학 |
| **HuggingFace** | 무제한 | 무제한 | ⭐⭐ | ⭐⭐⭐⭐ | AI/ML |
| **압축** | N/A | N/A | ⭐ | ⭐⭐⭐ | 보조 수단 |

---

## 🎯 권장 전략 (프로젝트 규모별)

### 소규모 (< 500MB)
```
Git LFS + 압축
- PDF만 Git LFS
- 이미지는 최적화 + 압축
```

### 중규모 (500MB ~ 2GB)
```
Google Drive + GitHub
- 원본 데이터: Google Drive
- 분석 스크립트: GitHub
- 결과 요약: GitHub
- 자동 다운로드 스크립트 제공
```

### 대규모 (> 2GB, 학술 목적)
```
Zenodo + GitHub
- 전체 데이터셋: Zenodo (DOI 발급)
- 분석 코드: GitHub
- 논문/리포트: GitHub Pages
```

### 협업/오픈소스
```
Kaggle/HuggingFace + GitHub
- 데이터셋: Kaggle or HuggingFace
- 코드: GitHub
- 커뮤니티 기여 환영
```

---

## 💡 최적 워크플로우 (추천)

### 구조
```
k21election/  (GitHub)
├── README.md                    # 프로젝트 소개 + 데이터 링크
├── DATA_SOURCES.md              # 데이터 다운로드 가이드
├── scripts/                     # 분석 스크립트
│   ├── download_data.py         # 자동 다운로드
│   ├── multiprocess_extractor.py
│   └── analyze_city.py
├── results/                     # 분석 결과만 (경량)
│   ├── sejong_summary.json
│   ├── jeju_summary.json
│   └── comparison.csv
├── reports/                     # 리포트 (Markdown)
│   ├── SEJONG_ANALYSIS.md
│   ├── JEJU_ANALYSIS.md
│   └── COMPARISON.md
└── docs/                        # GitHub Pages
    └── index.html

External Storage (Google Drive/Zenodo)
├── sejong.pdf (35MB)
├── jeju.pdf (69MB)
├── sejong_pages/ (compressed)
├── jeju_pages/ (compressed)
└── korea_all_cities.7z (1.5GB)
```

### DATA_SOURCES.md 예시
```markdown
# 데이터 다운로드

## 자동 다운로드 (권장)
```bash
python scripts/download_data.py --city all
```

## 수동 다운로드

### Google Drive (무료)
- [세종시 PDF (35MB)](https://drive.google.com/...)
- [제주시 PDF (69MB)](https://drive.google.com/...)
- [전체 압축 (1.5GB)](https://drive.google.com/...)

### Zenodo (학술용, DOI 있음)
- DOI: 10.5281/zenodo.xxxxxxx
- [전체 데이터셋 다운로드](https://zenodo.org/record/...)

## 데이터 구조
다운로드 후 다음과 같이 배치:
```
data/
├── sejong/
│   ├── sejong.pdf
│   └── pages/
└── jeju/
    ├── jeju.pdf
    └── pages/
```

## 검증
```bash
python scripts/verify_data.py
```
```

### download_data.py 예시
```python
#!/usr/bin/env python3
"""
선거 데이터 자동 다운로드 스크립트
"""
import os
import gdown
import argparse
from pathlib import Path

# Google Drive 파일 ID
DATASETS = {
    'sejong': {
        'pdf': 'GOOGLE_DRIVE_FILE_ID_1',
        'pages': 'GOOGLE_DRIVE_FOLDER_ID_1',
        'size': '35MB'
    },
    'jeju': {
        'pdf': 'GOOGLE_DRIVE_FILE_ID_2',
        'pages': 'GOOGLE_DRIVE_FOLDER_ID_2',
        'size': '69MB'
    },
    'all': {
        'archive': 'GOOGLE_DRIVE_FILE_ID_ALL',
        'size': '1.5GB'
    }
}

def download_city(city, include_pages=False):
    """도시 데이터 다운로드"""
    print(f"=== {city.upper()} 데이터 다운로드 ===")

    output_dir = Path(f'data/{city}')
    output_dir.mkdir(parents=True, exist_ok=True)

    # PDF 다운로드
    pdf_url = f"https://drive.google.com/uc?id={DATASETS[city]['pdf']}"
    pdf_path = output_dir / f'{city}.pdf'

    print(f"PDF 다운로드 중... ({DATASETS[city]['size']})")
    gdown.download(pdf_url, str(pdf_path), quiet=False)
    print(f"✓ 완료: {pdf_path}")

    # 페이지 다운로드 (선택)
    if include_pages:
        pages_url = f"https://drive.google.com/drive/folders/{DATASETS[city]['pages']}"
        pages_dir = output_dir / 'pages'

        print(f"페이지 이미지 다운로드 중...")
        gdown.download_folder(pages_url, str(pages_dir), quiet=False)
        print(f"✓ 완료: {pages_dir}")

def main():
    parser = argparse.ArgumentParser(description='선거 데이터 다운로드')
    parser.add_argument('--city', choices=['sejong', 'jeju', 'all'],
                       default='sejong',
                       help='다운로드할 도시')
    parser.add_argument('--pages', action='store_true',
                       help='페이지 이미지도 다운로드')

    args = parser.parse_args()

    if args.city == 'all':
        # 전체 압축 파일 다운로드
        print("전체 데이터 다운로드 중... (1.5GB)")
        gdown.download(
            f"https://drive.google.com/uc?id={DATASETS['all']['archive']}",
            'korea_election_data.7z',
            quiet=False
        )
        print("압축 해제 중...")
        os.system('7z x korea_election_data.7z -odata/')
    else:
        download_city(args.city, args.pages)

if __name__ == '__main__':
    main()
```

---

## 🚀 실전 적용 예시

### 현재 프로젝트에 적용

```bash
# 1. Google Drive에 데이터 업로드
# - sejong.pdf → 공유 링크 생성
# - jeju.pdf → 공유 링크 생성
# - 압축 파일 생성 및 업로드

# 2. 다운로드 스크립트 작성
cat > download_data.py <<'EOF'
import gdown

# Google Drive 파일 ID (공유 링크에서 추출)
SEJONG_PDF = "YOUR_FILE_ID_HERE"
JEJU_PDF = "YOUR_FILE_ID_HERE"

gdown.download(f"https://drive.google.com/uc?id={SEJONG_PDF}",
               "sejong.pdf", quiet=False)
gdown.download(f"https://drive.google.com/uc?id={JEJU_PDF}",
               "jeju.pdf", quiet=False)
EOF

# 3. README 업데이트
cat >> README.md <<'EOF'

## 데이터 다운로드

원본 PDF는 용량이 커서 외부 스토리지에 저장되어 있습니다.

### 자동 다운로드
```bash
pip install gdown
python download_data.py
```

### 수동 다운로드
- [세종시 PDF (35MB)](https://drive.google.com/file/d/...)
- [제주시 PDF (69MB)](https://drive.google.com/file/d/...)
EOF

# 4. Git에서 대용량 파일 제거
git rm --cached *.pdf
git rm --cached -r */pages/
echo "*.pdf" >> .gitignore
echo "*/pages/" >> .gitignore
git add .gitignore download_data.py
git commit -m "Move large files to external storage"
```

---

## 📝 결론 및 권장사항

### 당신의 프로젝트에 최적: **Google Drive + GitHub**

**이유:**
1. ✅ 무료 15GB (충분함)
2. ✅ 설정 간단 (5분)
3. ✅ 무제한 다운로드
4. ✅ 자동화 가능 (gdown)
5. ✅ 팀 협업 용이

### 실행 계획
```bash
# 1단계: Google Drive에 업로드 (10분)
# 2단계: 공유 링크 생성 및 기록 (5분)
# 3단계: download_data.py 작성 (10분)
# 4단계: README 업데이트 (5분)
# 5단계: Git에서 대용량 파일 제거 (5분)

총 소요 시간: 30분
```

### 향후 확장 시: **Zenodo (학술) or Kaggle (데이터 과학)**

학술 논문 발표 예정이라면 **Zenodo**를 추천합니다 (DOI 발급).

---

**문의사항이 있으면 언제든지 알려주세요!** 🚀
