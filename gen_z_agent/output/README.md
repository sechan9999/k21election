# Output Directory

Gen Z Agent가 생성한 분석 보고서들이 저장되는 디렉토리입니다.

## 생성되는 파일 형식

### 1. Excel 분석 보고서
- **파일명**: `Analysis_{analysis_id}.xlsx`
- **내용**:
  - Sheet 1: raw_data (원본 추출 데이터)
  - Sheet 2: enriched_data (검증/보강된 데이터)
  - Sheet 3: analysis (상세 분석)
  - Sheet 4: summary (요약)

### 2. Markdown 보고서
- **파일명**: `Report_{analysis_id}.md`
- **내용**:
  - 임원 요약 (Executive Summary)
  - 후보자별 분석
  - 투표 패턴 분석
  - 이상치 및 권장사항

### 3. 이메일 요약
- **파일명**: `Email_Summary_{analysis_id}.md`
- **내용**: 한 페이지 분량의 간결한 요약

## 예시 파일명

```
Analysis_sejong_2025_jan.xlsx
Report_sejong_2025_jan.md
Email_Summary_sejong_2025_jan.md
```

## 주의사항

- 이 디렉토리의 파일들은 `.gitignore`에 의해 Git에서 제외됩니다
- 생성된 보고서는 자동으로 이메일로 전송됩니다
- 보안이 필요한 보고서는 별도로 암호화하여 보관하세요

## 파일 보존 정책

- 생성된 파일은 자동으로 삭제되지 않습니다
- 주기적으로 오래된 파일을 정리하는 것을 권장합니다
- 중요한 보고서는 별도의 안전한 위치에 백업하세요
