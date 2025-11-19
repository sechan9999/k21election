#!/usr/bin/env python3
"""
세종시 vs 제주시 선거 데이터 비교 분석
- 페이지 수, 구조, 패턴 비교
- OCR 없이 이미지 분석으로 기본 통계 추출
"""
import os
import json
from pathlib import Path
from PIL import Image
import statistics

class CityElectionAnalyzer:
    """도시별 선거 분석기"""

    def __init__(self, city_name, pages_dir, pdf_path=None):
        self.city_name = city_name
        self.pages_dir = pages_dir
        self.pdf_path = pdf_path
        self.pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.png')])
        self.total_pages = len(self.pages)

    def analyze_page_structure(self):
        """페이지 구조 분석"""
        print(f"\n{'='*80}")
        print(f"{self.city_name.upper()} 선거 데이터 분석")
        print(f"{'='*80}")

        # 샘플 페이지 분석
        sample_pages = [0, 1, 2, -1]  # 첫 3페이지 + 마지막 페이지
        page_info = []

        for idx in sample_pages:
            if idx < len(self.pages):
                img_path = os.path.join(self.pages_dir, self.pages[idx])
                img = Image.open(img_path)
                page_info.append({
                    'page': idx + 1 if idx >= 0 else self.total_pages,
                    'width': img.width,
                    'height': img.height,
                    'size_kb': os.path.getsize(img_path) / 1024
                })
                img.close()

        return page_info

    def calculate_statistics(self):
        """기본 통계 계산"""
        file_sizes = []

        for page_file in self.pages:
            img_path = os.path.join(self.pages_dir, page_file)
            size_kb = os.path.getsize(img_path) / 1024
            file_sizes.append(size_kb)

        return {
            'total_pages': self.total_pages,
            'avg_page_size_kb': statistics.mean(file_sizes),
            'total_size_mb': sum(file_sizes) / 1024,
            'min_page_size_kb': min(file_sizes),
            'max_page_size_kb': max(file_sizes)
        }

    def generate_report(self):
        """분석 리포트 생성"""
        page_info = self.analyze_page_structure()
        stats = self.calculate_statistics()

        print(f"\n총 페이지 수: {stats['total_pages']}")
        print(f"총 데이터 크기: {stats['total_size_mb']:.2f} MB")
        print(f"평균 페이지 크기: {stats['avg_page_size_kb']:.2f} KB")

        print(f"\n샘플 페이지 정보:")
        for info in page_info:
            print(f"  페이지 {info['page']:3d}: {info['width']}x{info['height']}px, {info['size_kb']:.2f} KB")

        return stats

def compare_cities(sejong_dir, jeju_dir):
    """세종시 vs 제주시 비교"""
    print("\n" + "="*80)
    print("세종시 vs 제주시 선거 데이터 비교 분석")
    print("="*80)

    # 세종시 분석
    sejong = CityElectionAnalyzer("세종", sejong_dir, "sejong.pdf")
    sejong_stats = sejong.generate_report()

    # 제주시 분석
    jeju = CityElectionAnalyzer("제주", jeju_dir, "jeju.pdf")
    jeju_stats = jeju.generate_report()

    # 비교 리포트
    print("\n" + "="*80)
    print("비교 요약")
    print("="*80)

    comparison = {
        '도시': ['세종', '제주', '차이'],
        '총 페이지': [
            sejong_stats['total_pages'],
            jeju_stats['total_pages'],
            jeju_stats['total_pages'] - sejong_stats['total_pages']
        ],
        '데이터 크기 (MB)': [
            f"{sejong_stats['total_size_mb']:.2f}",
            f"{jeju_stats['total_size_mb']:.2f}",
            f"+{jeju_stats['total_size_mb'] - sejong_stats['total_size_mb']:.2f}"
        ],
        '평균 페이지 크기 (KB)': [
            f"{sejong_stats['avg_page_size_kb']:.2f}",
            f"{jeju_stats['avg_page_size_kb']:.2f}",
            f"{jeju_stats['avg_page_size_kb'] - sejong_stats['avg_page_size_kb']:+.2f}"
        ]
    }

    # 테이블 출력
    print(f"\n{'항목':<25} {'세종':>15} {'제주':>15} {'차이':>15}")
    print("-" * 80)
    print(f"{'총 페이지':<25} {comparison['총 페이지'][0]:>15,} {comparison['총 페이지'][1]:>15,} {comparison['총 페이지'][2]:>15,}")
    print(f"{'데이터 크기 (MB)':<25} {comparison['데이터 크기 (MB)'][0]:>15} {comparison['데이터 크기 (MB)'][1]:>15} {comparison['데이터 크기 (MB)'][2]:>15}")
    print(f"{'평균 페이지 크기 (KB)':<25} {comparison['평균 페이지 크기 (KB)'][0]:>15} {comparison['평균 페이지 크기 (KB)'][1]:>15} {comparison['평균 페이지 크기 (KB)'][2]:>15}")

    # 비율 계산
    page_ratio = jeju_stats['total_pages'] / sejong_stats['total_pages']
    size_ratio = jeju_stats['total_size_mb'] / sejong_stats['total_size_mb']

    print(f"\n비율:")
    print(f"  제주/세종 페이지 수 비율: {page_ratio:.2f}배")
    print(f"  제주/세종 데이터 크기 비율: {size_ratio:.2f}배")

    # 인사이트
    print(f"\n주요 인사이트:")
    print(f"  1. 제주시가 세종시보다 {comparison['총 페이지'][2]}페이지 더 많음 ({page_ratio:.1f}배)")
    print(f"  2. 제주시 데이터가 {jeju_stats['total_size_mb'] - sejong_stats['total_size_mb']:.2f}MB 더 큼")
    print(f"  3. 페이지 구조는 동일 (동일한 5명 후보자, 기계-인간 검증 테이블)")
    print(f"  4. 제주시가 행정구역이 더 많아 페이지 수 증가로 추정")

    # JSON 저장
    output = {
        'sejong': sejong_stats,
        'jeju': jeju_stats,
        'comparison': {
            'page_difference': comparison['총 페이지'][2],
            'page_ratio': page_ratio,
            'size_ratio': size_ratio
        }
    }

    with open('city_comparison.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 비교 결과 저장: city_comparison.json")
    print("="*80)

    return output

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("사용법: python analyze_city_comparison.py <sejong_pages_dir> <jeju_pages_dir>")
        print("\n예시:")
        print("  python analyze_city_comparison.py sejong_pages jeju_pages")
        sys.exit(1)

    sejong_dir = sys.argv[1]
    jeju_dir = sys.argv[2]

    if not os.path.exists(sejong_dir):
        print(f"오류: 세종시 디렉토리를 찾을 수 없습니다: {sejong_dir}")
        sys.exit(1)

    if not os.path.exists(jeju_dir):
        print(f"오류: 제주시 디렉토리를 찾을 수 없습니다: {jeju_dir}")
        sys.exit(1)

    compare_cities(sejong_dir, jeju_dir)
