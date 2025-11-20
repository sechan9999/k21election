# Historical Data Directory

과거 선거 데이터를 저장하여 비교 분석에 사용합니다.

## 샘플 파일

### `sample_historical_data.csv`
2024년 12월 15일 세종시 사전투표 결과 샘플 데이터입니다.

**컬럼 설명:**
- `date`: 투표 일자
- `candidate_number`: 후보자 번호
- `candidate_name`: 후보자 이름
- `vote_count`: 득표수
- `vote_percentage`: 득표율 (%)
- `location`: 지역
- `vote_type`: 투표 유형

## 사용 방법

과거 데이터와 비교 분석을 수행하면 다음을 확인할 수 있습니다:
- YoY (Year-over-Year) 변화율
- 후보자별 득표 트렌드
- 지역별 투표 패턴 변화
- 통계적 이상치 탐지

## 데이터 추가

새로운 과거 데이터를 추가하려면:
1. CSV 파일을 이 디렉토리에 추가
2. 파일명 형식: `election_data_YYYY_MM.csv`
3. 동일한 컬럼 구조 유지
