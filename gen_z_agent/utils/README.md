# Utils Directory

Gen Z Agent에서 사용하는 유틸리티 함수 및 헬퍼 모듈들을 저장합니다.

## 향후 추가 예정 모듈

### 1. `pdf_processor.py`
PDF 문서 처리를 위한 유틸리티:
- PDF → 이미지 변환
- OCR 실행
- 테이블 추출
- 한글 텍스트 처리

### 2. `email_sender.py`
이메일 발송 기능:
- SMTP 연결
- 첨부파일 처리
- HTML 이메일 템플릿
- 배치 전송

### 3. `slack_notifier.py`
Slack 알림 기능:
- Webhook 연동
- 메시지 포맷팅
- 파일 업로드
- 채널별 라우팅

### 4. `data_validator.py`
데이터 검증 로직:
- 합계 검증
- 통계적 이상치 탐지
- 데이터 타입 검증
- 비즈니스 룰 검증

### 5. `report_generator.py`
보고서 생성 유틸리티:
- Excel 포맷팅
- Markdown → PDF 변환
- 차트 생성
- 템플릿 엔진

## 사용 예시

```python
from utils.pdf_processor import extract_tables_from_pdf
from utils.email_sender import send_report_email
from utils.data_validator import validate_election_data

# PDF에서 데이터 추출
tables = extract_tables_from_pdf("invoice.pdf")

# 데이터 검증
is_valid, errors = validate_election_data(tables)

# 이메일 전송
send_report_email(
    recipients=["client@example.com"],
    subject="Analysis Complete",
    attachments=["report.xlsx"]
)
```

## 개발 가이드

새로운 유틸리티를 추가할 때:
1. 명확한 함수명 사용
2. Docstring 작성
3. 타입 힌트 추가
4. 단위 테스트 작성
5. README 업데이트
