# 세종시 선거 개표상황표 OCR 시스템

## 📋 개요

세종특별자치시 제21대 대통령선거 개표상황표 PDF를 자동으로 OCR 처리하고 데이터 품질을 검증하는 시스템입니다.

## 🎯 주요 기능

### 1. 한글 특화 OCR 처리
- **EasyOCR** 기반 한글/영어 동시 인식
- 이미지 전처리 (노이즈 제거, 대비 향상, 이진화)
- 고해상도 PDF → 이미지 변환
- 페이지별 독립 처리 및 결과 저장

### 2. 자동 데이터 추출
- 5명 후보자 정보 자동 인식
  - 이재명 (더불어민주당)
  - 김문수 (국민의힘)
  - 이준석 (개혁신당)
  - 권영국 (민주노동당)
  - 송진호 (무소속)
- 투표 유형 분류 (관외사전/관내사전/선거일투표)
- 득표수 자동 추출

### 3. 품질 검증 시스템
- 후보자 인식 일관성 검증
- OCR 신뢰도 측정
- 투표 유형 분포 분석
- 종합 품질 점수 계산 (A~F 등급)

### 4. 결과 리포팅
- JSON 형식 상세 결과
- Excel 요약 보고서
- 페이지별/후보자별 통계

## 🔧 설치 방법

### 시스템 요구사항
- Python 3.8 이상
- Linux/macOS/Windows

### 패키지 설치

```bash
# 필수 패키지 설치
pip install easyocr pdf2image opencv-python-headless numpy pandas pillow matplotlib openpyxl

# poppler-utils 설치 (PDF 변환용)
# Ubuntu/Debian:
sudo apt-get install poppler-utils

# macOS:
brew install poppler

# Windows:
# https://github.com/oschwartz10612/poppler-windows/releases/ 에서 다운로드
```

## 🚀 사용 방법

### 1. 빠른 시작 (샘플 5페이지)

```bash
# 테스트 실행 스크립트 사용
python3 run_ocr_test.py
```

이 명령은 자동으로:
1. 의존성 확인
2. sejong.pdf의 처음 5페이지 OCR 처리
3. 검증 시스템 실행
4. 보고서 생성

### 2. 직접 실행

#### OCR 처리

```bash
# 샘플 5페이지 처리
python3 ocr_processor.py sejong.pdf \
    --first-page 1 \
    --last-page 5 \
    --dpi 300 \
    --output-dir ./ocr_results

# 전체 126페이지 처리
python3 ocr_processor.py sejong.pdf \
    --dpi 300 \
    --output-dir ./ocr_results

# GPU 사용 (CUDA 설치된 경우)
python3 ocr_processor.py sejong.pdf \
    --gpu \
    --dpi 300
```

#### 검증 시스템

```bash
# 기본 검증
python3 verification_system.py \
    --results-dir ./ocr_results

# Excel 보고서 포함
python3 verification_system.py \
    --results-dir ./ocr_results \
    --excel
```

## 📊 결과 파일 구조

```
ocr_results/
├── all_results.json          # 전체 결과 통합
├── page_001_result.json      # 페이지별 상세 결과
├── page_002_result.json
├── ...
├── verification_report.json  # 검증 보고서 (JSON)
└── verification_report.xlsx  # 검증 보고서 (Excel)
```

### JSON 결과 형식

```json
{
  "page_number": 1,
  "vote_data": {
    "candidates": {
      "이재명": {
        "number": 1,
        "party": "더불어민주당",
        "possible_counts": [1234, 1230, 4],
        "confidence": 0.95
      }
    },
    "metadata": {
      "vote_type": "관내사전"
    }
  },
  "avg_confidence": 0.87
}
```

### Excel 보고서 내용

1. **페이지별요약** 시트
   - 페이지 번호
   - 투표 유형
   - 텍스트 블록 수
   - 평균 신뢰도
   - 인식된 후보자 수

2. **후보자별통계** 시트
   - 후보자명
   - 발견 횟수
   - 누락 횟수
   - 인식률

3. **품질요약** 시트
   - 종합 점수
   - 등급 (A~F)
   - 후보자 인식률
   - OCR 신뢰도

## 🎨 시스템 아키텍처

### 처리 파이프라인

```
PDF 입력 (sejong.pdf)
    ↓
PDF → 이미지 변환 (pdf2image, 300 DPI)
    ↓
이미지 전처리 (cv2)
    ├─ 그레이스케일 변환
    ├─ 노이즈 제거
    ├─ 대비 향상 (CLAHE)
    └─ 이진화
    ↓
OCR 처리 (EasyOCR)
    ├─ 한글 인식
    ├─ 영어 인식
    └─ 신뢰도 계산
    ↓
데이터 추출
    ├─ 후보자 정보
    ├─ 득표수
    └─ 투표 유형
    ↓
검증 시스템
    ├─ 일관성 검증
    ├─ 품질 측정
    └─ 등급 평가
    ↓
보고서 생성 (JSON + Excel)
```

## 📈 성능 최적화

### 처리 속도 향상

1. **DPI 조정**
   ```bash
   # 빠른 처리 (낮은 품질)
   --dpi 150

   # 표준 처리 (권장)
   --dpi 300

   # 고품질 처리 (느림)
   --dpi 600
   ```

2. **GPU 사용**
   ```bash
   # CUDA 설치 후
   --gpu
   ```

3. **병렬 처리** (수동)
   ```bash
   # 페이지 범위별로 분할 처리
   python3 ocr_processor.py sejong.pdf --first-page 1 --last-page 42 &
   python3 ocr_processor.py sejong.pdf --first-page 43 --last-page 84 &
   python3 ocr_processor.py sejong.pdf --first-page 85 --last-page 126 &
   ```

### 예상 처리 시간

| 페이지 수 | DPI | GPU | 예상 시간 |
|----------|-----|-----|----------|
| 5        | 200 | No  | ~5분     |
| 5        | 300 | No  | ~8분     |
| 126      | 200 | No  | ~2시간   |
| 126      | 300 | No  | ~3시간   |
| 126      | 300 | Yes | ~30분    |

## 🔍 품질 등급 기준

| 등급 | 점수 범위 | 설명 |
|------|----------|------|
| A    | 90~100%  | 우수 - 대부분의 데이터 정확히 인식 |
| B    | 80~89%   | 양호 - 일부 수동 검토 필요 |
| C    | 70~79%   | 보통 - 상당한 수동 검토 필요 |
| D    | 60~69%   | 미흡 - 대부분 수동 검토 필요 |
| F    | <60%     | 불량 - 재처리 권장 |

종합 점수 계산:
```
종합점수 = (후보자인식률 × 0.6) + (OCR신뢰도 × 0.4)
```

## 🛠️ 문제 해결

### 자주 발생하는 오류

1. **`poppler-utils` 설치 안됨**
   ```
   오류: pdf2image.exceptions.PDFInfoNotInstalledError
   해결: sudo apt-get install poppler-utils
   ```

2. **메모리 부족**
   ```
   오류: MemoryError
   해결: DPI 낮추기 (--dpi 150) 또는 페이지 분할 처리
   ```

3. **한글 인식 실패**
   ```
   오류: 한글이 깨지거나 인식 안됨
   해결: EasyOCR 재설치 - pip install --upgrade easyocr
   ```

4. **GPU 오류**
   ```
   오류: CUDA not available
   해결: --gpu 옵션 제거 또는 PyTorch CUDA 버전 설치
   ```

## 📝 개발 정보

### 파일 구조

```
k21election/
├── sejong.pdf                  # 원본 PDF (126페이지)
├── ocr_processor.py            # OCR 처리 메인 모듈
├── verification_system.py      # 검증 시스템 모듈
├── run_ocr_test.py            # 빠른 테스트 스크립트
├── README_OCR.md              # 이 파일
└── ocr_results/               # 결과 저장 디렉토리
    ├── all_results.json
    ├── page_*.json
    ├── verification_report.json
    └── verification_report.xlsx
```

### 주요 클래스

1. **KoreanElectionOCR** (ocr_processor.py)
   - `convert_pdf_to_images()`: PDF → 이미지
   - `preprocess_image()`: 이미지 전처리
   - `extract_text_from_image()`: OCR 수행
   - `extract_vote_counts()`: 득표수 추출
   - `process_page()`: 페이지 처리
   - `process_pdf()`: 전체 PDF 처리

2. **ElectionDataVerifier** (verification_system.py)
   - `load_results()`: 결과 로드
   - `verify_candidate_consistency()`: 후보자 일관성 검증
   - `verify_ocr_quality()`: OCR 품질 검증
   - `generate_quality_report()`: 보고서 생성
   - `export_to_excel()`: Excel 내보내기

## 🔬 고급 사용법

### Python API 사용

```python
from ocr_processor import KoreanElectionOCR
from verification_system import ElectionDataVerifier

# OCR 처리
ocr = KoreanElectionOCR(gpu=False)
results = ocr.process_pdf(
    'sejong.pdf',
    output_dir='./results',
    first_page=1,
    last_page=10
)

# 검증
verifier = ElectionDataVerifier(results_dir='./results')
verifier.load_results()
report = verifier.generate_quality_report()

# 결과 접근
print(f"평균 신뢰도: {report['ocr_quality']['average_confidence']:.2%}")
print(f"종합 등급: {report['overall_quality']['grade']}")
```

### 커스텀 후보자 설정

```python
# ocr_processor.py에서 수정
self.candidates = {
    1: {'name': '후보1', 'party': '정당1'},
    2: {'name': '후보2', 'party': '정당2'},
    # ...
}
```

## 📚 참고 자료

- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)
- [pdf2image Documentation](https://github.com/Belval/pdf2image)
- [OpenCV Python Tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

## 🤝 기여

개선 사항이나 버그 리포트는 Issues에 등록해주세요.

## 📄 라이선스

교육 및 연구 목적으로 자유롭게 사용 가능합니다.

---

**작성**: 2025-11-18
**버전**: 1.0
**AI 어시스턴트**: Claude Sonnet 4.5 (Anthropic)
