# 제주시 선거 데이터 분석 설정 가이드

## 문제: Windows 로컬 경로 접근 불가

제공하신 경로는 Windows 로컬 파일 시스템입니다:
```
file:///C:/Users/secha/Downloads/Kelec/K21/제주시개표상황표(39287).pdf
```

현재 Linux 환경(`/home/user/k21election`)에서는 직접 접근할 수 없습니다.

---

## 해결 방법

### 방법 1: 파일 업로드 (가장 간단)

1. **Claude Code 웹 인터페이스 사용**
   - 파일 드래그 앤 드롭
   - 또는 파일 선택 버튼 클릭

2. **명령어 사용 (터미널에서)**
   ```bash
   # 현재 디렉토리 확인
   pwd
   # /home/user/k21election

   # 파일 업로드 후 확인
   ls -lh *.pdf
   ```

### 방법 2: SCP로 파일 전송 (고급)

Windows PowerShell에서:
```powershell
# 서버로 파일 전송
scp "C:/Users/secha/Downloads/Kelec/K21/제주시개표상황표(39287).pdf" `
    user@[서버주소]:/home/user/k21election/jeju.pdf
```

### 방법 3: 임시 웹 링크 (대안)

Google Drive, Dropbox 등에 업로드 후 직접 다운로드 링크 제공

---

## 파일 업로드 후 실행 명령어

### 1. 간단한 방법 (통합 스크립트)
```bash
# 제주시 데이터 완전 처리 (추출 + 분석 + 리포트)
python3 process_city_data.py jeju jeju.pdf

# 또는 고해상도로
python3 process_city_data.py jeju jeju.pdf 200
```

### 2. 단계별 방법

**Step 1: 페이지 추출**
```bash
python3 multiprocess_pdf_extractor.py jeju.pdf jeju_pages 150
```

**Step 2: 페이지 분석**
```bash
python3 multiprocess_analyzer.py jeju_pages jeju_analysis.json jeju_summary.csv
```

---

## 예상 출력 구조

```
jeju_election_data/
├── pages/                    # 추출된 페이지 이미지
│   ├── page_001.png
│   ├── page_002.png
│   └── ...
├── analysis/                 # 분석 결과
│   ├── jeju_analysis.json    # 상세 분석 (JSON)
│   └── jeju_summary.csv      # 요약 (CSV)
└── reports/                  # 리포트
    └── jeju_report.md        # 마크다운 리포트
```

---

## 성능 최적화

### 멀티프로세싱 설정
- **CPU 코어 수**: 자동 감지 (최대 코어 수 - 1)
- **수동 설정 가능**: 스크립트 수정

### 예상 처리 시간
- **세종시 (126페이지)**: ~30초 (멀티프로세싱)
- **제주시**: 페이지 수에 따라 다름
- **단일 프로세스 대비**: 약 3-5배 빠름

---

## 세종시 vs 제주시 비교 분석

두 도시 데이터 모두 처리 후:

```bash
# 비교 스크립트 실행 (예정)
python3 compare_cities.py sejong_election_data jeju_election_data
```

---

## 체크리스트

- [ ] 제주시 PDF 파일 업로드 (`jeju.pdf`)
- [ ] 필요한 라이브러리 설치 확인
  ```bash
  pip install PyMuPDF pillow pytesseract
  ```
- [ ] Tesseract OCR 한글 팩 설치
  ```bash
  sudo apt-get install tesseract-ocr tesseract-ocr-kor
  ```
- [ ] 멀티프로세싱 스크립트 실행 권한
  ```bash
  chmod +x multiprocess_pdf_extractor.py
  chmod +x multiprocess_analyzer.py
  chmod +x process_city_data.py
  ```
- [ ] 통합 스크립트 실행
  ```bash
  python3 process_city_data.py jeju jeju.pdf
  ```

---

## 문제 해결

### Q: "파일을 찾을 수 없습니다" 오류
```bash
# 현재 디렉토리의 PDF 파일 확인
ls -lh *.pdf

# 예상 출력:
# sejong.pdf
# jeju.pdf  ← 이 파일이 있어야 함
```

### Q: OCR이 작동하지 않음
```bash
# Tesseract 설치 확인
tesseract --version

# 한글 언어 팩 확인
tesseract --list-langs
# kor이 목록에 있어야 함
```

### Q: 멀티프로세싱 오류
```bash
# CPU 코어 수 확인
python3 -c "import multiprocessing; print(multiprocessing.cpu_count())"

# 워커 수 수동 조정 (스크립트 내에서)
num_workers = 2  # 안전한 값으로 변경
```

---

## 다음 단계

1. ✅ 멀티프로세싱 스크립트 작성 완료
2. ⏳ 제주시 PDF 파일 업로드 대기
3. 📋 파일 업로드 후 자동 처리 시작
4. 📊 세종시와 제주시 데이터 비교 분석
5. 📈 통합 대시보드 생성

---

**준비 완료!** 제주시 PDF 파일을 업로드해주시면 즉시 처리를 시작하겠습니다.
