# 대용량 선거 데이터 관리 가이드

## 📦 문제 상황

- **세종시**: 126페이지 (manageable)
- **대도시**: 수백~수천 페이지 가능
- **전국 통합**: 수십 GB 이상
- **Git 제한**: 단일 파일 100MB, 저장소 5GB 권장

## 🎯 해결 전략

### 1. Git LFS (Large File Storage) 사용

#### 1.1 Git LFS 설치

```bash
# Ubuntu/Debian
sudo apt-get install git-lfs

# macOS
brew install git-lfs

# Windows
# https://git-lfs.github.com/ 에서 설치

# 초기화
git lfs install
```

#### 1.2 LFS 트래킹 설정

```bash
# .gitattributes 파일 생성
cat > .gitattributes << 'EOF'
# PDF 파일
*.pdf filter=lfs diff=lfs merge=lfs -text

# 대용량 이미지
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text

# 압축 파일
*.zip filter=lfs diff=lfs merge=lfs -text
*.tar.gz filter=lfs diff=lfs merge=lfs -text

# 데이터 파일
data/**/* filter=lfs diff=lfs merge=lfs -text
election_data/**/*.pdf filter=lfs diff=lfs merge=lfs -text
EOF

# LFS 파일 트래킹
git lfs track "*.pdf"
git lfs track "data/**/*"

# 커밋
git add .gitattributes
git commit -m "Add Git LFS configuration"
```

#### 1.3 LFS 파일 관리

```bash
# 추적 중인 파일 확인
git lfs ls-files

# LFS 상태 확인
git lfs status

# 특정 파일을 LFS로 마이그레이션
git lfs migrate import --include="*.pdf"

# LFS 파일 푸시
git push origin main

# LFS 파일 풀
git lfs pull
```

### 2. 외부 스토리지 활용

#### 2.1 클라우드 스토리지 옵션

**A. AWS S3**
```python
import boto3

# S3 클라이언트
s3 = boto3.client('s3')

# 업로드
s3.upload_file('seoul.pdf', 'election-data-bucket', 'pdfs/seoul.pdf')

# 다운로드
s3.download_file('election-data-bucket', 'pdfs/seoul.pdf', 'seoul.pdf')

# URL 생성 (공개 링크)
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'election-data-bucket', 'Key': 'pdfs/seoul.pdf'},
    ExpiresIn=3600  # 1시간 유효
)
```

**B. Google Drive**
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive API
service = build('drive', 'v3', credentials=creds)

# 업로드
file_metadata = {'name': 'seoul.pdf'}
media = MediaFileUpload('seoul.pdf', mimetype='application/pdf')
file = service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'
).execute()

print(f'File ID: {file.get("id")}')
```

**C. Azure Blob Storage**
```python
from azure.storage.blob import BlobServiceClient

# Blob 클라이언트
blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client("election-data")

# 업로드
with open("seoul.pdf", "rb") as data:
    blob_client = container_client.upload_blob(name="seoul.pdf", data=data)
```

#### 2.2 데이터 매니페스트 시스템

**파일 구조**:
```
project/
├── .git/
├── code/                    # Git에 포함
│   ├── ocr_processor.py
│   └── batch_processor.py
├── data/                    # Git에서 제외 (.gitignore)
│   ├── seoul.pdf           (외부 스토리지)
│   ├── busan.pdf           (외부 스토리지)
│   └── ...
├── data_manifest.json      # Git에 포함 (메타데이터만)
└── .gitignore
```

**data_manifest.json**:
```json
{
  "cities": [
    {
      "city_name": "서울특별시",
      "city_code": "seoul",
      "file_name": "seoul.pdf",
      "file_size_mb": 450.5,
      "total_pages": 2500,
      "file_hash": "a1b2c3d4e5f6...",
      "storage": {
        "type": "s3",
        "bucket": "election-data-kr",
        "key": "pdfs/seoul.pdf",
        "download_url": "https://s3.amazonaws.com/election-data-kr/pdfs/seoul.pdf"
      }
    }
  ]
}
```

**다운로드 스크립트**:
```bash
#!/bin/bash
# download_data.sh

# data_manifest.json에서 URL 읽어서 다운로드
python3 << 'PYTHON'
import json
import urllib.request
from pathlib import Path

with open('data_manifest.json') as f:
    manifest = json.load(f)

Path('data').mkdir(exist_ok=True)

for city in manifest['cities']:
    url = city['storage']['download_url']
    filename = f"data/{city['file_name']}"

    print(f"Downloading {city['city_name']}...")
    urllib.request.urlretrieve(url, filename)
    print(f"  ✓ Saved to {filename}")

print("All files downloaded!")
PYTHON
```

### 3. 분산 처리 전략

#### 3.1 도시별 분할 처리

```bash
# 각 도시를 독립적으로 처리
python3 batch_processor.py --city seoul --workers 8
python3 batch_processor.py --city busan --workers 8
python3 batch_processor.py --city daegu --workers 8

# 결과만 Git에 커밋 (PDF는 제외)
git add election_data/seoul/ocr_results/*.json
git commit -m "Add Seoul OCR results"
```

#### 3.2 페이지 범위별 분할

```bash
# 대용량 PDF를 여러 청크로 분할 처리
python3 ocr_processor_multiprocessing.py seoul.pdf \
    --first-page 1 --last-page 500 \
    --output-dir results/seoul_chunk1 &

python3 ocr_processor_multiprocessing.py seoul.pdf \
    --first-page 501 --last-page 1000 \
    --output-dir results/seoul_chunk2 &

python3 ocr_processor_multiprocessing.py seoul.pdf \
    --first-page 1001 --last-page 1500 \
    --output-dir results/seoul_chunk3 &

# 결과 병합
python3 merge_results.py results/seoul_chunk* \
    --output results/seoul_complete
```

#### 3.3 클러스터 처리 (선택사항)

```python
# Dask를 사용한 분산 처리
from dask.distributed import Client, as_completed
from dask import delayed

client = Client()  # 로컬 클러스터

@delayed
def process_page_range(pdf_path, start, end):
    from ocr_processor_multiprocessing import MultiProcessingOCR
    processor = MultiProcessingOCR()
    return processor.process_pdf_parallel(
        pdf_path, first_page=start, last_page=end
    )

# 작업 생성
tasks = []
chunk_size = 100
for i in range(0, 2500, chunk_size):
    task = process_page_range('seoul.pdf', i+1, min(i+chunk_size, 2500))
    tasks.append(task)

# 병렬 실행
results = client.compute(tasks)
client.gather(results)
```

### 4. 결과물 압축 및 아카이빙

#### 4.1 처리 결과 압축

```bash
# 도시별 결과 압축
cd election_data/seoul/ocr_results
tar -czf ../seoul_ocr_results.tar.gz *.json *.png

# Git에는 압축 파일만 커밋
cd ../..
git add seoul/seoul_ocr_results.tar.gz
git commit -m "Add Seoul OCR results (compressed)"
```

#### 4.2 선택적 데이터 보관

```
보관 우선순위:
1. 원본 PDF        → 외부 스토리지 (S3, Drive)
2. OCR JSON 결과   → Git (압축)
3. 처리된 이미지    → 선택적 보관 (외부 스토리지)
4. 임시 파일       → 삭제
```

### 5. .gitignore 설정

```bash
cat > .gitignore << 'EOF'
# 대용량 데이터 파일
*.pdf
data/
election_data/**/*.pdf
election_data/**/*.png

# 임시 처리 파일
ocr_results/
ocr_results_mp/
pdf_analysis/
temp/
cache/

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.pytest_cache/
venv/
.venv/

# 시스템
.DS_Store
Thumbs.db
*.swp
*.swo

# 설정 파일 (민감정보)
config.local.json
credentials.json
.env

# 로그
*.log
logs/

# 압축 파일 (선택적)
# *.tar.gz
# *.zip
EOF

git add .gitignore
git commit -m "Add comprehensive .gitignore"
```

### 6. 실전 워크플로우

#### 시나리오 1: 새로운 도시 데이터 추가

```bash
# 1. PDF를 외부 스토리지에 업로드
aws s3 cp incheon.pdf s3://election-data-kr/pdfs/incheon.pdf

# 2. 매니페스트에 추가
python3 batch_processor.py --add-city \
    --name "인천광역시" \
    --code incheon \
    --url "https://s3.amazonaws.com/election-data-kr/pdfs/incheon.pdf"

# 3. 로컬에 다운로드 (필요시)
python3 download_data.py --city incheon

# 4. OCR 처리
python3 ocr_processor_multiprocessing.py data/incheon.pdf \
    --workers 8 \
    --output-dir election_data/incheon/ocr_results

# 5. 결과 압축 및 커밋
cd election_data/incheon
tar -czf incheon_ocr_results.tar.gz ocr_results/*.json
git add incheon_ocr_results.tar.gz
git commit -m "Add Incheon OCR results"

# 6. 원본 PDF 삭제 (외부 스토리지에 있으므로)
rm ../../data/incheon.pdf

# 7. 푸시
git push origin main
```

#### 시나리오 2: 전국 통합 처리

```bash
# 1. 설정 로드
python3 batch_processor.py --load-config

# 2. Dry-run으로 계획 확인
python3 batch_processor.py --process --dry-run

# 3. 우선순위 높은 도시부터 처리
python3 batch_processor.py --process --priority 1

# 4. 야간에 전체 처리
nohup python3 batch_processor.py --process --all \
    > batch_processing.log 2>&1 &

# 5. 진행상황 모니터링
tail -f batch_processing.log
```

### 7. 성능 예측

#### 7.1 처리 시간 추정

```python
# 세종시 기준 (126페이지)
base_time_per_page = 2  # 초 (200 DPI, 8 워커)

def estimate_processing_time(total_pages, num_workers=8):
    """처리 시간 예측"""
    # 세종시 대비 스케일링
    time_per_page = base_time_per_page * (8 / num_workers)
    total_seconds = total_pages * time_per_page

    return {
        'total_seconds': total_seconds,
        'minutes': total_seconds / 60,
        'hours': total_seconds / 3600,
        'pages': total_pages,
        'workers': num_workers
    }

# 예시
cities = {
    '세종': 126,
    '서울': 2500,
    '경기': 5000,
    '부산': 1500
}

for city, pages in cities.items():
    est = estimate_processing_time(pages, num_workers=8)
    print(f"{city}: {pages}페이지 → {est['hours']:.1f}시간")

# 출력:
# 세종: 126페이지 → 0.1시간
# 서울: 2500페이지 → 1.4시간
# 경기: 5000페이지 → 2.8시간
# 부산: 1500페이지 → 0.8시간
```

#### 7.2 스토리지 예측

```python
def estimate_storage(total_pages):
    """스토리지 요구량 예측"""
    # 페이지당 평균 크기
    png_per_page_mb = 0.25      # 전처리된 이미지
    json_per_page_kb = 5        # OCR 결과 JSON

    total_png_mb = total_pages * png_per_page_mb
    total_json_mb = total_pages * json_per_page_kb / 1024

    return {
        'images_mb': total_png_mb,
        'images_gb': total_png_mb / 1024,
        'json_mb': total_json_mb,
        'total_gb': (total_png_mb + total_json_mb) / 1024
    }

# 전국 추정
total_pages_nationwide = 50000  # 가정
storage = estimate_storage(total_pages_nationwide)

print(f"전국 50,000페이지:")
print(f"  이미지: {storage['images_gb']:.1f} GB")
print(f"  JSON: {storage['json_mb']:.0f} MB")
print(f"  총합: {storage['total_gb']:.1f} GB")

# 출력:
# 전국 50,000페이지:
#   이미지: 12.2 GB
#   JSON: 244 MB
#   총합: 12.4 GB
```

## 📊 권장 설정

### 소규모 프로젝트 (< 10개 도시)
- **Git**: 직접 사용 + Git LFS
- **처리**: 로컬 멀티프로세싱
- **스토리지**: Git LFS (PDF) + GitHub (결과)

### 중규모 프로젝트 (10-50개 도시)
- **Git**: 결과만 커밋
- **처리**: 로컬 + 클라우드 VM
- **스토리지**: S3 (PDF) + Git (결과 압축)

### 대규모 프로젝트 (전국)
- **Git**: 코드 + 매니페스트만
- **처리**: 클라우드 분산 처리
- **스토리지**: S3/GCS (모든 데이터)
- **DB**: PostgreSQL/MongoDB (결과 저장)

## 🚀 시작하기

```bash
# 1. Git LFS 설정
git lfs install
git lfs track "*.pdf"

# 2. 배치 프로세서 설정
python3 batch_processor.py --setup

# 3. 매니페스트 생성
python3 batch_processor.py --manifest

# 4. Dry-run 테스트
python3 batch_processor.py --process --dry-run

# 5. 실제 처리
python3 batch_processor.py --process
```

---

**작성일**: 2025-11-18
**버전**: 1.0
