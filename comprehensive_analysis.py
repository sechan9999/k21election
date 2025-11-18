#!/usr/bin/env python3
"""
Comprehensive analysis by reading all page images and extracting comparison data
Since we need to manually review handwritten numbers, this script organizes the task
"""
import os
from pathlib import Path

def main():
    """Main analysis function"""

    pages_dir = "pdf_pages_all"
    pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.png')])

    print("="*80)
    print("COMPREHENSIVE MACHINE vs HUMAN VERIFICATION ANALYSIS")
    print("="*80)
    print(f"\nTotal pages: {len(pages)}")
    print(f"Pages to analyze: {len(pages) - 2} (excluding pages 1 and 126)")

    # Batch pages for systematic review
    batches = [
        {"name": "Early Voting Pages", "range": range(2, 10), "description": "관외투표, 관내사전 초기 페이지"},
        {"name": "Main Voting - Batch 1", "range": range(10, 30), "description": "투표함 번호별 개표"},
        {"name": "Main Voting - Batch 2", "range": range(30, 50), "description": "투표함 번호별 개표"},
        {"name": "Main Voting - Batch 3", "range": range(50, 70), "description": "동별 선거일 투표"},
        {"name": "Main Voting - Batch 4", "range": range(70, 90), "description": "동별 선거일 투표"},
        {"name": "Main Voting - Batch 5", "range": range(90, 110), "description": "동별 선거일 투표"},
        {"name": "Main Voting - Batch 6", "range": range(110, 126), "description": "최종 투표함들"},
    ]

    print("\n\nBatch Organization:")
    for i, batch in enumerate(batches, 1):
        page_count = len(list(batch["range"]))
        print(f"{i}. {batch['name']}: Pages {min(batch['range'])+1}-{max(batch['range'])+1} ({page_count} pages)")
        print(f"   {batch['description']}")

    print("\n" + "="*80)
    print("KEY OBSERVATIONS FROM SAMPLE PAGES:")
    print("="*80)

    observations = [
        {
            "page": 2,
            "type": "관외투표",
            "observation": "우측 테이블에 수기 작성 숫자 있음 - 기계와 인간 검증 비교 필요"
        },
        {
            "page": 3,
            "type": "관외사전",
            "observation": "33,676개 투표지 중 33,674개 기계 분류, 33,672개 최종 투표수, 차이 2표"
        },
        {
            "page": 4,
            "type": "1투표함",
            "observation": "3,000개 투표 중 123개 재확인 대상"
        },
        {
            "page": 20,
            "type": "관내",
            "observation": "2,073개 투표, 68개 재확인 대상"
        },
        {
            "page": 50,
            "type": "초전동/제11투",
            "observation": "3,316개 발급, 2,429개 투표"
        },
    ]

    for obs in observations:
        print(f"\nPage {obs['page']} ({obs['type']}):")
        print(f"  {obs['observation']}")

    print("\n" + "="*80)
    print("ANALYSIS METHOD:")
    print("="*80)
    print("""
Since the PDF contains handwritten numbers in the human verification columns,
automated OCR would require training for Korean handwriting recognition.

For accurate analysis, we will:
1. Systematically review each page (2-125)
2. Compare the left table (machine) with right table (human)
3. Check if all values match for each candidate
4. Record voting type and match status
5. Generate summary statistics by voting type

Key comparison formula:
  Machine ② (분류된) = Human (a) (확인결과-분류된)
  AND
  Machine ③ (재확인대상) = Human (b) (확인결과-재확인대상)

If both conditions are true for ALL 5 candidates + invalid votes,
then the page shows 100% machine-human match.
    """)

    print("="*80)
    print("READY TO BEGIN SYSTEMATIC REVIEW")
    print("="*80)

if __name__ == "__main__":
    main()
