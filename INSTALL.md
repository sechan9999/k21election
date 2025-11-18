# 설치 가이드 (Installation Guide)

## 📋 시스템 요구사항

- **Python**: 3.8 이상
- **운영체제**: Linux, macOS, Windows
- **메모리**: 최소 4GB RAM (8GB 권장)
- **디스크**: 최소 2GB 여유 공간 (PyTorch 포함 시 4GB)

## 🚀 빠른 설치 (Quick Install)

### 1. 저장소 클론

```bash
git clone https://github.com/sechan9999/k21election.git
cd k21election
```

### 2. Python 패키지 설치

```bash
# 기본 설치 (CPU 버전)
pip install -r requirements.txt

# 또는 개별 설치
pip install easyocr PyMuPDF opencv-python-headless numpy pandas matplotlib openpyxl
```

**주의**: EasyOCR 설치는 시간이 오래 걸립니다 (10-20분, PyTorch 포함).

### 3. 시스템 패키지 설치 (선택사항)

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install poppler-utils tesseract-ocr tesseract-ocr-kor
```

#### macOS
```bash
brew install poppler tesseract tesseract-lang
```

#### Windows
- Poppler: https://github.com/oschwartz10612/poppler-windows/releases/
- Tesseract: https://github.com/UB-Mannheim/tesseract/wiki

## 🔍 설치 확인

### 의존성 확인

```bash
python3 -c "import easyocr; print('EasyOCR:', easyocr.__version__)"
python3 -c "import fitz; print('PyMuPDF:', fitz.version)"
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
```

### PDF 분석 테스트

```bash
# 간단한 PDF 분석 (OCR 없음)
python3 simple_pdf_analyzer.py sejong.pdf
```

출력 예시:
```
📄 PDF 분석 시작: sejong.pdf
   총 페이지 수: 126
   제목:
   작성자:

📸 처음 3페이지 이미지 추출 중...
   ✓ 페이지 1: 1241x1755 → ./pdf_analysis/page_001.png
   ✓ 페이지 2: 1241x1755 → ./pdf_analysis/page_002.png
   ✓ 페이지 3: 1241x1755 → ./pdf_analysis/page_003.png

✅ 분석 완료!
```

## 🎯 OCR 시스템 테스트

### 방법 1: 빠른 테스트 스크립트

```bash
python3 run_ocr_test.py
```

이 스크립트는 자동으로:
1. 필요한 패키지 확인
2. sejong.pdf 처음 5페이지 OCR 처리
3. 검증 시스템 실행
4. 보고서 생성

### 방법 2: 직접 실행

```bash
# 1. OCR 처리 (5페이지 샘플)
python3 ocr_processor.py sejong.pdf \
    --first-page 1 \
    --last-page 5 \
    --dpi 200 \
    --output-dir ./ocr_results

# 2. 결과 검증
python3 verification_system.py \
    --results-dir ./ocr_results \
    --excel
```

## ⚡ GPU 가속 (선택사항)

### CUDA 설치 확인

```bash
nvidia-smi
```

### PyTorch GPU 버전 설치

```bash
# CUDA 11.8 기준
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 설치 확인
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

### GPU로 실행

```bash
python3 ocr_processor.py sejong.pdf --gpu --dpi 300
```

## 🔧 문제 해결

### 1. EasyOCR 설치 실패

**증상**: `pip install easyocr` 실패

**해결책**:
```bash
# 최신 pip로 업그레이드
pip install --upgrade pip setuptools wheel

# 재시도
pip install easyocr
```

### 2. PDF 변환 오류

**증상**: `pdf2image.exceptions.PDFInfoNotInstalledError`

**해결책**:
```bash
# poppler-utils 설치 필요
sudo apt-get install poppler-utils  # Ubuntu/Debian
brew install poppler                 # macOS
```

또는 PyMuPDF 사용 (시스템 패키지 불필요):
```bash
pip install PyMuPDF
python3 simple_pdf_analyzer.py sejong.pdf
```

### 3. 메모리 부족

**증상**: `MemoryError` 또는 프로세스 강제 종료

**해결책**:
```bash
# DPI 낮추기
python3 ocr_processor.py sejong.pdf --dpi 150

# 페이지별 처리
python3 ocr_processor.py sejong.pdf --first-page 1 --last-page 10
python3 ocr_processor.py sejong.pdf --first-page 11 --last-page 20
# ...
```

### 4. 한글 인식 안됨

**증상**: 한글이 깨지거나 인식되지 않음

**해결책**:
```bash
# EasyOCR 재설치
pip uninstall easyocr
pip install --no-cache-dir easyocr

# 한글 모델 수동 다운로드 (처음 실행 시 자동)
python3 -c "import easyocr; reader = easyocr.Reader(['ko'])"
```

### 5. OpenCV 오류

**증상**: `ImportError: libGL.so.1: cannot open shared object file`

**해결책**:
```bash
# Ubuntu/Debian
sudo apt-get install libgl1-mesa-glx

# 또는 headless 버전 사용
pip uninstall opencv-python
pip install opencv-python-headless
```

## 📦 가상환경 사용 (권장)

```bash
# 가상환경 생성
python3 -m venv venv

# 활성화
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 패키지 설치
pip install -r requirements.txt

# 사용 후 비활성화
deactivate
```

## 🐳 Docker 사용 (선택사항)

```bash
# Dockerfile 생성
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리
WORKDIR /app

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY . .

# 실행
CMD ["python3", "run_ocr_test.py"]
EOF

# 이미지 빌드
docker build -t k21election-ocr .

# 실행
docker run -v $(pwd)/ocr_results:/app/ocr_results k21election-ocr
```

## ✅ 설치 완료 확인

모든 것이 정상적으로 설치되었다면:

```bash
python3 run_ocr_test.py
```

다음과 같은 출력이 나와야 합니다:

```
🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
                    세종시 선거 개표상황표 OCR 시스템
                         Korean Election Ballot OCR
🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟

============================================================
🚀 세종시 선거 개표상황표 OCR 테스트 시작
============================================================

📦 의존성 확인 중...
✅ easyocr
✅ cv2
✅ numpy
✅ PIL
✅ pdf2image

...
```

## 📚 다음 단계

설치가 완료되었다면:

1. **문서 읽기**: [README_OCR.md](README_OCR.md) 참조
2. **샘플 테스트**: 5페이지 처리
3. **전체 처리**: 126페이지 OCR
4. **결과 분석**: 검증 보고서 확인

## 💬 지원

문제가 발생하면:
- GitHub Issues: https://github.com/sechan9999/k21election/issues
- 문서 참조: README_OCR.md, CLAUDE.md

---

**작성일**: 2025-11-18
**버전**: 1.0
