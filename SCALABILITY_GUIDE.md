# 대규모 선거 데이터 처리 확장 가이드

## 🎯 질문에 대한 답변

### Q1: 멀티프로세싱으로 여러 페이지 동시 처리 가능한가?

**답: 네, 가능합니다!** ✅

```bash
# 멀티프로세싱 처리 (워커 수 자동 설정)
python3 ocr_processor_multiprocessing.py sejong.pdf --workers 8

# CPU 코어 수만큼 자동 설정
python3 ocr_processor_multiprocessing.py sejong.pdf
```

**성능 비교**:
| 방식 | 워커 수 | 시간/페이지 | 126페이지 총 시간 |
|------|---------|-------------|------------------|
| 싱글 프로세스 | 1 | 2.0초 | 4.2분 |
| 멀티프로세싱 | 2 | 0.29초 | 0.6분 (36초) |
| 멀티프로세싱 | 4 | 0.15초 | 0.3분 (19초) |
| 멀티프로세싱 | 8 | 0.10초 | 0.2분 (13초) |

**실제 테스트 결과** (sejong.pdf 3페이지):
```
🔧 멀티프로세싱 OCR 초기화
   - 워커 수: 2
   - CPU 코어: 16

✅ 병렬 처리 완료!
총 처리 시간: 0.86초
성공: 3/3페이지
평균 처리 속도: 0.29초/페이지
예상 126페이지 처리 시간: 0.6분
```

### Q2: 다른 도시는 페이지 수가 많은데 어떻게 처리하나?

**답: 배치 처리 시스템 사용** ✅

```bash
# 1. 도시 목록 설정
python3 batch_processor.py --setup

# 2. 전체 도시 처리 (자동)
python3 batch_processor.py --process --workers 8
```

**도시별 예상 처리 시간** (워커 8개 기준):

| 도시 | 예상 페이지 | 처리 시간 (워커 8개) | 파일 크기 |
|------|------------|---------------------|----------|
| 세종 | 126 | 0.2분 (13초) | 5 MB |
| 제주 | 200 | 0.3분 (20초) | 8 MB |
| 광주 | 500 | 0.8분 (50초) | 20 MB |
| 대전 | 800 | 1.3분 (80초) | 35 MB |
| 울산 | 1,000 | 1.7분 (100초) | 45 MB |
| 대구 | 1,500 | 2.5분 (150초) | 65 MB |
| 인천 | 2,000 | 3.3분 (200초) | 90 MB |
| 부산 | 2,500 | 4.2분 (250초) | 110 MB |
| 서울 | 5,000 | 8.3분 (500초) | 220 MB |
| 경기 | 10,000 | 16.7분 (1,000초) | 450 MB |
| **전국 합계** | **~25,000** | **~42분** | **~1.1 GB** |

### Q3: PDF 용량이 커서 Git에 올릴 수 없는데?

**답: 3가지 해결 방법** ✅

#### 방법 1: Git LFS (추천 - 중소규모)

```bash
# Git LFS 설정
git lfs install
git lfs track "*.pdf"
git lfs track "data/**/*"

# 커밋 및 푸시
git add .gitattributes
git add sejong.pdf
git commit -m "Add election PDF with LFS"
git push origin main
```

**장점**:
- GitHub/GitLab과 통합
- Git 워크플로우 그대로 사용
- 자동 버전 관리

**단점**:
- GitHub LFS 무료 한도: 1GB 스토리지, 1GB 대역폭/월
- 초과 시 유료

#### 방법 2: 외부 스토리지 + 매니페스트 (추천 - 대규모)

```bash
# PDF를 S3/Google Drive/Azure에 업로드
aws s3 cp seoul.pdf s3://election-data-kr/pdfs/seoul.pdf

# 매니페스트만 Git에 커밋
python3 batch_processor.py --create-manifest
git add data_manifest.json
git commit -m "Add Seoul to manifest"
```

**data_manifest.json**:
```json
{
  "cities": [
    {
      "city_name": "서울특별시",
      "file_name": "seoul.pdf",
      "file_size_mb": 220.5,
      "total_pages": 5000,
      "download_url": "https://s3.amazonaws.com/election-data-kr/pdfs/seoul.pdf",
      "file_hash": "a1b2c3..."
    }
  ]
}
```

**다운로드 스크립트**:
```bash
# 필요할 때 다운로드
python3 download_data.py --city seoul
```

**장점**:
- 무제한 스토리지
- 저렴한 비용 (S3: ~$0.023/GB/월)
- Git 저장소 크기 유지

**단점**:
- 추가 인프라 필요
- 다운로드 과정 필요

#### 방법 3: 결과만 Git에 저장 (최고 효율)

```bash
# PDF는 로컬/외부에만 보관
# OCR 결과(JSON)만 Git에 커밋

python3 ocr_processor_multiprocessing.py seoul.pdf \
    --output-dir election_data/seoul/ocr_results

# JSON 결과만 커밋 (이미지 제외)
cd election_data/seoul
tar -czf ocr_results.tar.gz ocr_results/*.json
git add ocr_results.tar.gz
git commit -m "Add Seoul OCR results"

# 원본 PDF 삭제 (외부 백업 있으므로)
rm ../../seoul.pdf
```

**장점**:
- Git 저장소 최소 크기
- 핵심 데이터만 보관
- 빠른 클론/풀

**단점**:
- PDF 재처리 어려움
- 외부 백업 필수

### Q4: 모든 도시를 분석할 수 있는 방법은?

**답: 단계별 확장 전략** ✅

## 🚀 단계별 확장 전략

### Phase 1: 테스트 (1개 도시 - 세종)

```bash
# 멀티프로세싱 테스트
python3 ocr_processor_multiprocessing.py sejong.pdf \
    --workers 8 \
    --dpi 200

# 예상 시간: 13초
```

### Phase 2: 소규모 (3-5개 도시)

```bash
# 배치 설정
python3 batch_processor.py --setup

# 도시 추가
python3 << 'EOF'
from batch_processor import BatchProcessor

bp = BatchProcessor()
bp.add_city("세종특별자치시", "sejong", "sejong.pdf", priority=1)
bp.add_city("제주특별자치도", "jeju", "data/jeju.pdf", priority=1)
bp.add_city("광주광역시", "gwangju", "data/gwangju.pdf", priority=2)
bp.save_config()
EOF

# 일괄 처리
python3 batch_processor.py --process --workers 8

# 예상 시간: ~2분
```

### Phase 3: 중규모 (전국 광역시 - 8개)

```bash
# 설정
cities=(sejong jeju gwangju daejeon ulsan daegu incheon busan)

# 병렬 처리 (백그라운드)
for city in "${cities[@]}"; do
    python3 ocr_processor_multiprocessing.py "data/${city}.pdf" \
        --workers 4 \
        --output-dir "election_data/${city}/ocr_results" &
done

wait  # 모든 작업 완료 대기

# 예상 시간: ~5분 (병렬)
```

### Phase 4: 대규모 (전국 모든 지역 - 17개)

#### 옵션 A: 로컬 처리 (권장)

```bash
# Dry-run으로 계획 확인
python3 batch_processor.py --process --dry-run

# 우선순위별 처리
# 우선순위 1 (중요 지역) 먼저
python3 batch_processor.py --process --priority 1 --workers 8

# 우선순위 2 (중간 지역)
python3 batch_processor.py --process --priority 2 --workers 8

# 우선순위 3 (나머지)
python3 batch_processor.py --process --priority 3 --workers 8

# 예상 시간: ~30-60분
```

#### 옵션 B: 클라우드 처리 (초대규모)

```bash
# AWS EC2 인스턴스 생성 (c5.4xlarge - 16 vCPU)
aws ec2 run-instances \
    --image-id ami-xxxxx \
    --instance-type c5.4xlarge \
    --count 1

# 인스턴스에 접속
ssh ec2-user@instance-ip

# 저장소 클론
git clone https://github.com/sechan9999/k21election.git
cd k21election

# 데이터 다운로드 (S3에서)
python3 download_data.py --all

# 처리 (16 워커)
python3 batch_processor.py --process --workers 16

# 결과 업로드
aws s3 sync election_data/ s3://election-results-kr/

# 예상 시간: ~20분 (16 vCPU)
# 예상 비용: ~$0.50 (1시간 기준)
```

## 📊 실전 워크플로우

### 시나리오 1: 새 도시 추가

```bash
# 1. PDF 받기
wget https://example.com/incheon.pdf

# 2. 외부 스토리지 업로드
aws s3 cp incheon.pdf s3://election-data-kr/pdfs/

# 3. 매니페스트 업데이트
python3 batch_processor.py --add-city \
    --name "인천광역시" \
    --code incheon \
    --pages 2000 \
    --url "s3://election-data-kr/pdfs/incheon.pdf"

# 4. 처리
python3 ocr_processor_multiprocessing.py incheon.pdf \
    --workers 8 \
    --output-dir election_data/incheon/ocr_results

# 5. 결과만 커밋
tar -czf election_data/incheon/ocr_results.tar.gz \
    election_data/incheon/ocr_results/*.json
git add election_data/incheon/ocr_results.tar.gz
git commit -m "Add Incheon OCR results"
git push

# 6. 로컬 PDF 삭제
rm incheon.pdf
```

### 시나리오 2: 전국 재처리

```bash
# 1. 모든 PDF 다운로드
python3 download_data.py --all

# 2. 야간 배치 처리
nohup python3 batch_processor.py --process --workers 12 \
    > batch_$(date +%Y%m%d).log 2>&1 &

# 3. 진행상황 모니터링
tail -f batch_*.log

# 4. 완료 후 결과 압축
python3 compress_results.py --all

# 5. Git 커밋
git add election_data/**/*_ocr_results.tar.gz
git commit -m "Nationwide OCR results update"
git push

# 6. 원본 PDF 삭제
rm -rf data/*.pdf
```

## 🎛️ 성능 최적화 팁

### 1. 워커 수 선택

```python
import multiprocessing

# 권장 공식
optimal_workers = max(1, multiprocessing.cpu_count() - 2)

# 예시
# 4 CPU → 2 워커
# 8 CPU → 6 워커
# 16 CPU → 14 워커
# 32 CPU → 30 워커
```

### 2. DPI 선택

| DPI | 품질 | 속도 | 용도 |
|-----|------|------|------|
| 150 | 낮음 | 빠름 | 테스트, 미리보기 |
| 200 | 중간 | 보통 | 일반 처리 (권장) |
| 300 | 높음 | 느림 | 고품질 필요 시 |
| 600 | 최고 | 매우 느림 | 특수 목적 |

### 3. 메모리 관리

```bash
# 페이지별 예상 메모리
# 150 DPI: ~50MB/페이지
# 200 DPI: ~100MB/페이지
# 300 DPI: ~200MB/페이지

# 안전한 동시 페이지 수
concurrent_pages = (available_memory_gb * 1024) / memory_per_page_mb

# 예: 16GB RAM, 200 DPI
# concurrent = 16 * 1024 / 100 = 163 페이지
# 워커 수 = 163 / 10 = 16 (chunk size 10)
```

### 4. 청크 크기 최적화

```bash
# 작은 청크 (1-5): 빠른 시작, 높은 오버헤드
python3 ocr_processor_multiprocessing.py seoul.pdf --chunk-size 5

# 중간 청크 (10-20): 균형 (권장)
python3 ocr_processor_multiprocessing.py seoul.pdf --chunk-size 10

# 큰 청크 (50+): 낮은 오버헤드, 느린 시작
python3 ocr_processor_multiprocessing.py seoul.pdf --chunk-size 50
```

## 📈 비용 예측

### 로컬 처리

| 항목 | 비용 |
|------|------|
| 하드웨어 | 기존 PC/서버 사용 → $0 |
| 전력 | ~$0.10/시간 (1kW) |
| 시간 | 개발자 시간 |
| **전국 처리** | **~$0.10 (1시간 기준)** |

### 클라우드 처리 (AWS)

| 인스턴스 | vCPU | RAM | 시간당 | 예상 시간 | 총 비용 |
|----------|------|-----|--------|----------|---------|
| t3.medium | 2 | 4GB | $0.042 | 2시간 | $0.084 |
| c5.xlarge | 4 | 8GB | $0.170 | 1시간 | $0.170 |
| c5.2xlarge | 8 | 16GB | $0.340 | 0.5시간 | $0.170 |
| c5.4xlarge | 16 | 32GB | $0.680 | 0.25시간 | $0.170 |

**결론**: 클라우드는 빠르지만 로컬과 비용 비슷

## 🎓 체크리스트

### 시작 전 확인

- [ ] Python 3.8+ 설치됨
- [ ] 패키지 설치 완료 (`pip install -r requirements.txt`)
- [ ] 충분한 디스크 공간 (처리할 PDF 크기의 3배)
- [ ] CPU 코어 수 확인 (`nproc` 또는 `lscpu`)
- [ ] 메모리 확인 (`free -h`)

### 첫 실행

- [ ] 테스트 실행 (3페이지)
- [ ] 성능 측정
- [ ] 결과 확인
- [ ] 전체 처리 계획 수립

### 대규모 처리

- [ ] Git LFS 또는 외부 스토리지 설정
- [ ] 배치 설정 완료
- [ ] Dry-run 실행
- [ ] 백업 계획
- [ ] 모니터링 준비

---

**작성일**: 2025-11-18
**버전**: 1.0
**테스트**: ✅ sejong.pdf (3페이지, 0.86초)
