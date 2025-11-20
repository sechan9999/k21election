# Invoices Directory

이 디렉토리는 분석할 청구서 및 선거 개표상황표 파일들을 저장합니다.

## 지원 파일 형식

- PDF (.pdf)
- JSON (.json)
- HTML (.html)
- Excel (.xlsx, .xls)

## 샘플 파일

### `sample_election_data.json`
세종특별자치시 아름동 제1투표소의 관외사전투표 개표 결과 샘플입니다.
이 파일은 Gen Z Agent 시스템을 테스트하기 위한 예제 데이터입니다.

**포함 정보:**
- 5명 후보자 득표수
- 기계 분류 vs 인간 확인 데이터
- 투표소 정보
- 검증 정보

## 실제 PDF 파일 사용

실제 선거 개표상황표 PDF를 분석하려면:

1. PDF 파일을 이 디렉토리에 복사
2. 다음 명령어로 실행:
   ```bash
   python main.py ./invoices/your_file.pdf --id your_analysis_id
   ```

## 테스트 실행

샘플 JSON 파일로 테스트:
```bash
python main.py ./invoices/sample_election_data.json --id test_run
```

## 주의사항

- 개인정보나 민감한 선거 데이터는 공개 저장소에 커밋하지 마세요
- 대용량 PDF 파일은 .gitignore에 추가하는 것을 권장합니다
- 실제 운영 환경에서는 별도의 보안 스토리지 사용을 권장합니다
