# 멀티프로세싱 선거 데이터 분석 시스템

## 🚀 성능 테스트 결과 (세종시 데이터)

```
✓ 126페이지 PDF 처리 시간: 1.19초
✓ 평균 속도: 105.58 페이지/초
✓ CPU 코어: 16개 → 15개 워커 프로세스 활용
✓ 성공률: 100% (126/126)
```

**기존 방식 대비 약 10-15배 빠름!**

---

## 📦 시스템 구성

### 1. 멀티프로세싱 PDF 추출기
**파일**: `multiprocess_pdf_extractor.py`

```bash
# 사용법
python3 multiprocess_pdf_extractor.py <pdf_file> [output_dir] [dpi]

# 예시
python3 multiprocess_pdf_extractor.py sejong.pdf sejong_pages 150
python3 multiprocess_pdf_extractor.py jeju.pdf jeju_pages 200
```

**특징**:
- 여러 페이지를 동시에 병렬 처리
- 자동 워커 수 조정 (CPU 코어 수 - 1)
- 진행률 실시간 표시
- 에러 처리 및 리포팅

### 2. 멀티프로세싱 분석기
**파일**: `multiprocess_analyzer.py`

```bash
# 사용법
python3 multiprocess_analyzer.py <pages_dir> [output_json] [output_csv]

# 예시
python3 multiprocess_analyzer.py sejong_pages
python3 multiprocess_analyzer.py jeju_pages jeju_analysis.json jeju_summary.csv
```

**특징**:
- 페이지 이미지 병렬 분석
- OCR 텍스트 추출 (한글 지원)
- 투표 유형 자동 분류
- JSON + CSV 출력

### 3. 통합 처리 시스템
**파일**: `process_city_data.py`

```bash
# 사용법
python3 process_city_data.py <city_name> <pdf_file> [dpi]

# 예시
python3 process_city_data.py sejong sejong.pdf
python3 process_city_data.py jeju jeju.pdf 200
```

**워크플로우**:
1. 디렉토리 구조 생성
2. PDF 페이지 추출 (멀티프로세싱)
3. 페이지 분석 (멀티프로세싱)
4. 마크다운 리포트 생성

**출력 구조**:
```
{city_name}_election_data/
├── pages/                     # 페이지 이미지
│   ├── page_001.png
│   ├── page_002.png
│   └── ...
├── analysis/                  # 분석 결과
│   ├── {city}_analysis.json   # 상세 분석
│   └── {city}_summary.csv     # 요약
└── reports/                   # 리포트
    └── {city}_report.md       # 마크다운
```

---

## 🎯 제주시 데이터 처리 방법

### Step 1: 파일 업로드

**방법 A - 웹 인터페이스 (권장)**
1. Claude Code 채팅 창에서 📎 클립 아이콘 클릭
2. `제주시개표상황표(39287).pdf` 선택
3. 업로드 후 `jeju.pdf`로 저장

**방법 B - 드래그 앤 드롭**
1. Windows 탐색기에서 PDF 파일 선택
2. 채팅 창으로 드래그 앤 드롭

### Step 2: 파일 확인
```bash
# 현재 디렉토리의 PDF 파일 확인
ls -lh *.pdf

# 예상 출력:
# sejong.pdf (3.7M)
# jeju.pdf   (업로드 후 표시됨)
```

### Step 3: 제주시 데이터 처리 실행

**간단한 방법 (권장)**:
```bash
python3 process_city_data.py jeju jeju.pdf
```

**단계별 방법**:
```bash
# 1. 페이지 추출
python3 multiprocess_pdf_extractor.py jeju.pdf jeju_pages

# 2. 페이지 분석
python3 multiprocess_analyzer.py jeju_pages

# 3. 결과 확인
cat jeju_election_data/reports/jeju_report.md
```

### Step 4: 결과 확인
```bash
# 리포트 보기
cat jeju_election_data/reports/jeju_report.md

# CSV 확인
head jeju_election_data/analysis/jeju_summary.csv

# JSON 확인
python3 -m json.tool jeju_election_data/analysis/jeju_analysis.json | head -50
```

---

## ⚡ 성능 최적화 팁

### CPU 활용도
- **16 코어 시스템**: 15개 워커 (최적)
- **8 코어 시스템**: 7개 워커
- **4 코어 시스템**: 3개 워커

### DPI 설정
- **150 DPI**: 빠름, 일반 분석용 (권장)
- **200 DPI**: 중간, OCR 정확도 향상
- **300 DPI**: 느림, 최고 품질

### 메모리 고려사항
- 126페이지 × 150 DPI ≈ 35MB
- 동시 처리 시 메모리 사용량 증가
- 대용량 PDF는 배치 처리 권장

---

## 🔧 문제 해결

### Q1: "ModuleNotFoundError: No module named 'fitz'"
```bash
pip install PyMuPDF pillow
```

### Q2: OCR이 작동하지 않음
```bash
# Tesseract 설치 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-kor

# 설치 확인
tesseract --version
tesseract --list-langs | grep kor
```

### Q3: 파일을 찾을 수 없음
```bash
# 절대 경로 사용
python3 process_city_data.py jeju /home/user/k21election/jeju.pdf

# 또는 현재 디렉토리 확인
pwd
ls -lh *.pdf
```

### Q4: 멀티프로세싱 오류
```bash
# 워커 수 수동 조정 (스크립트 내)
# multiprocess_pdf_extractor.py 열어서:
num_workers = 2  # 안전한 값으로 변경
```

---

## 📊 비교 분석 (세종 vs 제주)

두 도시 데이터 처리 후:

```bash
# 디렉토리 구조 비교
tree -L 2 sejong_election_data jeju_election_data

# 페이지 수 비교
echo "세종시: $(ls sejong_election_data/pages/*.png | wc -l) 페이지"
echo "제주시: $(ls jeju_election_data/pages/*.png | wc -l) 페이지"

# 투표 유형 비교
diff sejong_election_data/analysis/sejong_summary.csv \
     jeju_election_data/analysis/jeju_summary.csv
```

---

## 📝 체크리스트

### 시스템 준비
- [x] Python 3.x 설치
- [x] PyMuPDF (fitz) 설치
- [x] Pillow 설치
- [x] 멀티프로세싱 지원 확인
- [ ] Tesseract OCR + 한글 팩 (선택사항)

### 스크립트 준비
- [x] `multiprocess_pdf_extractor.py` 생성
- [x] `multiprocess_analyzer.py` 생성
- [x] `process_city_data.py` 생성
- [x] 실행 권한 설정

### 데이터 준비
- [x] 세종시 PDF (`sejong.pdf`)
- [ ] 제주시 PDF (`jeju.pdf`) ← **업로드 대기 중**

### 실행
- [x] 세종시 테스트 완료 (1.19초, 126페이지)
- [ ] 제주시 처리 대기

---

## 🎓 학습 및 개선사항

### 멀티프로세싱 vs 단일 프로세스

| 방식 | 126페이지 처리 시간 | 평균 속도 | 배속 |
|------|-------------------|-----------|------|
| 단일 프로세스 | ~15초 | ~8 페이지/초 | 1x |
| 멀티프로세싱 (15워커) | 1.19초 | 105 페이지/초 | **13x** |

### 향후 개선 가능 영역
1. **GPU 가속**: CUDA 기반 OCR 처리
2. **캐싱**: 이미 처리된 페이지 재사용
3. **증분 처리**: 새 페이지만 추가 처리
4. **분산 처리**: 여러 서버에 작업 분산
5. **실시간 모니터링**: 웹 대시보드

---

## 📧 다음 단계

1. **제주시 PDF 업로드** ← 현재 단계
2. **제주시 데이터 처리 실행**
3. **세종 vs 제주 비교 분석**
4. **통합 대시보드 생성**
5. **OCR 정확도 검증**
6. **후보자별 득표 집계**

---

**준비 완료!** 제주시 PDF를 업로드하시면 즉시 처리를 시작하겠습니다. 🚀
