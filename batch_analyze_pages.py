#!/usr/bin/env python3
"""
Batch analyze all 126 pages to extract machine vs human comparison data
This will help identify which pages have 100% match vs discrepancies
"""
import os
import csv
from pathlib import Path

def analyze_page_structure():
    """
    Based on manual review, document the page structure patterns
    """

    page_types = {
        "Page 1": "Summary page - Early voting (거소·선상투표)",
        "Page 2": "Individual ballot box - 관외투표",
        "Page 3": "Individual ballot box - 관외사전",
        "Pages 4-125": "Individual ballot boxes - Various voting types",
        "Page 126": "Summary page - Wrong district voting (잘못 투입·구분된 투표지)"
    }

    voting_types_found = [
        "거소·선상투표 (Absentee/Ship voting)",
        "관외투표 (Out-of-district voting)",
        "관내사전 (In-district advance voting)",
        "투표함 (Ballot boxes numbered 1, 2, 3, etc.)",
        "선거일 (Election day voting by district)",
    ]

    return page_types, voting_types_found

def get_page_list():
    """Get list of all page images"""
    pages_dir = "pdf_pages_all"
    pages = sorted([f for f in os.listdir(pages_dir) if f.endswith('.png')])
    return pages, pages_dir

def create_analysis_plan():
    """
    Create a systematic plan to extract data from all pages
    """

    pages, pages_dir = get_page_list()

    analysis_plan = {
        "total_pages": len(pages),
        "pages_to_analyze": [
            {
                "range": "Page 1",
                "type": "Summary (skip - no comparison needed)",
                "action": "Skip"
            },
            {
                "range": "Pages 2-125",
                "type": "Individual ballot box results",
                "action": "Extract machine (②,③) vs human (a,b) for each candidate"
            },
            {
                "range": "Page 126",
                "type": "Summary (skip - no comparison needed)",
                "action": "Skip"
            }
        ],
        "data_points_per_page": {
            "candidates": 5,
            "invalid_votes": 1,
            "total_comparisons": 6,
            "fields_per_candidate": "machine_② vs human_a, machine_③ vs human_b"
        },
        "expected_data_rows": 124  # Pages 2-125
    }

    return analysis_plan

if __name__ == "__main__":
    print("="*80)
    print("BATCH ANALYSIS PLAN FOR 126 PAGES")
    print("="*80)

    page_types, voting_types = analyze_page_structure()

    print("\nPage Structure:")
    for page, desc in page_types.items():
        print(f"  {page}: {desc}")

    print("\nVoting Types Found:")
    for vtype in voting_types:
        print(f"  - {vtype}")

    plan = create_analysis_plan()

    print(f"\n\nAnalysis Plan:")
    print(f"  Total pages: {plan['total_pages']}")
    print(f"  Pages to analyze: {plan['expected_data_rows']}")
    print(f"  Comparisons per page: {plan['data_points_per_page']['total_comparisons']}")
    print(f"  Total comparisons: {plan['expected_data_rows'] * plan['data_points_per_page']['total_comparisons']}")

    pages, pages_dir = get_page_list()

    print(f"\n\nPages available in {pages_dir}:")
    print(f"  First page: {pages[0]}")
    print(f"  Last page: {pages[-1]}")
    print(f"  Total: {len(pages)} pages")

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Manually review pages 2-125 (124 pages)")
    print("2. For each page, extract:")
    print("   - Machine classification: ② (분류된 투표지수)")
    print("   - Machine reconfirm: ③ (재확인대상 투표지수)")
    print("   - Human verification: (a) (확인결과 - 분류된)")
    print("   - Human reconfirm: (b) (확인결과 - 재확인대상)")
    print("3. Compare: ② = (a) AND ③ = (b) for each candidate")
    print("4. Record if 100% match or discrepancy")
    print("="*80)
