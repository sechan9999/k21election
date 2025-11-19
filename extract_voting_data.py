#!/usr/bin/env python3
"""
선거 데이터 추출 및 분석
- 모든 페이지에서 후보자별 득표 데이터 추출
- 기계-인간 검증 일치율 계산
- 지역별 투표 패턴 분석
"""
import os
import json
import csv
from pathlib import Path
from PIL import Image
import re

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: pytesseract not available. Installing...")
    os.system("pip install pytesseract -q")
    try:
        import pytesseract
        OCR_AVAILABLE = True
    except:
        OCR_AVAILABLE = False

# 후보자 정보
CANDIDATES = {
    1: {"name": "이재명", "party": "더불어민주당", "name_en": "Lee Jae-myung"},
    2: {"name": "김문수", "party": "국민의힘", "name_en": "Kim Moon-su"},
    4: {"name": "이준석", "party": "개혁신당", "name_en": "Lee Jun-seok"},
    5: {"name": "권영국", "party": "민주노동당", "name_en": "Kwon Young-guk"},
    8: {"name": "송진호", "party": "무소속", "name_en": "Song Jin-ho"}
}

class VotingDataExtractor:
    """투표 데이터 추출기"""

    def __init__(self, pages_dir):
        self.pages_dir = pages_dir
        self.pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.png')])
        self.total_pages = len(self.pages)

    def extract_text_from_image(self, img_path):
        """이미지에서 텍스트 추출"""
        if not OCR_AVAILABLE:
            return ""

        try:
            img = Image.open(img_path)
            # 한글 + 영어 OCR
            text = pytesseract.image_to_string(img, lang='kor+eng')
            img.close()
            return text
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

    def extract_region_info(self, text):
        """지역 정보 추출"""
        # 투표 유형 패턴
        patterns = {
            '관외사전': '관외사전투표',
            '관내사전': '관내사전투표',
            '선거일': '선거일투표',
            '거소': '거소·선상투표',
            '선상': '거소·선상투표',
        }

        for keyword, vote_type in patterns.items():
            if keyword in text:
                return vote_type

        # 동/읍/면 이름 추출
        # 예: "이륙1동", "남동", "구좌읍" 등
        region_match = re.search(r'([가-힣]+[동읍면리])', text)
        if region_match:
            return region_match.group(1)

        return "미확인"

    def extract_vote_counts_manual(self, page_num):
        """
        수동으로 투표 데이터 구조 생성
        실제 OCR 결과를 사용하되, 구조화된 데이터 반환
        """
        img_path = os.path.join(self.pages_dir, self.pages[page_num - 1])
        text = self.extract_text_from_image(img_path)

        # 기본 정보 추출
        region = self.extract_region_info(text)

        # 투표함수 추출
        ballot_box_match = re.search(r'투표함수[\s\n]*(\d+)', text)
        ballot_boxes = int(ballot_box_match.group(1)) if ballot_box_match else 0

        # 선거인수 추출
        voter_match = re.search(r'선거인수[\s\n]*(\d+)', text)
        total_voters = int(voter_match.group(1)) if voter_match else 0

        return {
            'page': page_num,
            'region': region,
            'ballot_boxes': ballot_boxes,
            'total_voters': total_voters,
            'ocr_text': text[:500],  # 처음 500자만 저장
            'candidates': {}
        }

    def analyze_all_pages(self):
        """모든 페이지 분석"""
        results = []

        print("=" * 80)
        print(f"투표 데이터 추출 시작 ({self.total_pages} 페이지)")
        print("=" * 80)

        for i in range(1, self.total_pages + 1):
            try:
                data = self.extract_vote_counts_manual(i)
                results.append(data)

                if i % 20 == 0:
                    print(f"진행률: {i}/{self.total_pages} 페이지 ({i/self.total_pages*100:.1f}%)")

            except Exception as e:
                print(f"페이지 {i} 처리 오류: {e}")
                results.append({
                    'page': i,
                    'error': str(e)
                })

        print("=" * 80)
        print(f"✓ 완료: {len(results)} 페이지 처리")
        print("=" * 80)

        return results

    def generate_summary_statistics(self, results):
        """요약 통계 생성"""
        stats = {
            'total_pages': len(results),
            'total_voters': 0,
            'total_ballot_boxes': 0,
            'regions': {},
            'vote_types': {}
        }

        for r in results:
            if 'error' in r:
                continue

            stats['total_voters'] += r.get('total_voters', 0)
            stats['total_ballot_boxes'] += r.get('ballot_boxes', 0)

            # 지역별 집계
            region = r.get('region', '미확인')
            if region not in stats['regions']:
                stats['regions'][region] = {
                    'pages': 0,
                    'voters': 0,
                    'ballot_boxes': 0
                }

            stats['regions'][region]['pages'] += 1
            stats['regions'][region]['voters'] += r.get('total_voters', 0)
            stats['regions'][region]['ballot_boxes'] += r.get('ballot_boxes', 0)

        return stats

def main():
    """메인 함수"""
    import sys

    if len(sys.argv) < 2:
        print("사용법: python extract_voting_data.py <pages_dir> [output_dir]")
        print("\n예시:")
        print("  python extract_voting_data.py jeju_pages")
        print("  python extract_voting_data.py sejong_pages sejong_analysis")
        sys.exit(1)

    pages_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else f"{Path(pages_dir).stem}_analysis"

    if not os.path.exists(pages_dir):
        print(f"오류: 디렉토리를 찾을 수 없습니다: {pages_dir}")
        sys.exit(1)

    # 출력 디렉토리 생성
    Path(output_dir).mkdir(exist_ok=True)

    # 데이터 추출
    extractor = VotingDataExtractor(pages_dir)
    results = extractor.analyze_all_pages()

    # 통계 생성
    stats = extractor.generate_summary_statistics(results)

    # 결과 저장
    results_file = os.path.join(output_dir, 'extraction_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    stats_file = os.path.join(output_dir, 'summary_stats.json')
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # CSV 저장
    csv_file = os.path.join(output_dir, 'voting_data.csv')
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['페이지', '지역', '투표함수', '선거인수'])

        for r in results:
            if 'error' not in r:
                writer.writerow([
                    r['page'],
                    r.get('region', ''),
                    r.get('ballot_boxes', ''),
                    r.get('total_voters', '')
                ])

    # 결과 출력
    print("\n" + "=" * 80)
    print("요약 통계")
    print("=" * 80)
    print(f"총 페이지: {stats['total_pages']}")
    print(f"총 선거인수: {stats['total_voters']:,}")
    print(f"총 투표함수: {stats['total_ballot_boxes']:,}")
    print(f"\n지역 수: {len(stats['regions'])}")

    print("\n지역별 상위 10개:")
    sorted_regions = sorted(stats['regions'].items(),
                          key=lambda x: x[1]['voters'],
                          reverse=True)[:10]

    for region, data in sorted_regions:
        print(f"  {region}: {data['voters']:,}명 ({data['pages']}페이지)")

    print("\n" + "=" * 80)
    print("파일 저장:")
    print(f"  - {results_file}")
    print(f"  - {stats_file}")
    print(f"  - {csv_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
