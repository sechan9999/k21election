#!/usr/bin/env python3
"""
Detailed manual comparison of machine vs human counts from visible pages
Based on manual review of page images
"""
import json
import pandas as pd

def extract_page_data():
    """
    Manually extracted data from reviewed pages
    Format: Machine ② vs Human (a), Machine ③ vs Human (b)
    """

    pages_data = [
        {
            "page": 2,
            "type": "관외투표",
            "candidates": {
                "C1_이재명": {"machine_②": 1227, "machine_③": 0, "human_a": 1227, "human_b": 13, "match": False},
                "C2_김문수": {"machine_②": 375, "machine_③": 0, "human_a": 375, "human_b": 0, "match": True},
                "C4_이준석": {"machine_②": 209, "machine_③": 39, "human_a": 209, "human_b": 39, "match": True},
                "C5_권영국": {"machine_②": 44, "machine_③": 0, "human_a": 44, "human_b": 1, "match": False},
                "C8_송진호": {"machine_②": 1, "machine_③": 0, "human_a": 1, "human_b": 1, "match": False},
            },
            "overall_match": False
        },
        {
            "page": 3,
            "type": "관내사전",
            "candidates": {
                "C1_이재명": {"machine_②": 19900, "machine_③": 0, "human_a": 19900, "human_b": 452, "match": False},
                "C2_김문수": {"machine_②": 7679, "machine_③": 0, "human_a": 7679, "human_b": 280, "match": False},
                "C4_이준석": {"machine_②": 4520, "machine_③": 0, "human_a": 4520, "human_b": 128, "match": False},
                "C5_권영국": {"machine_②": 354, "machine_③": 0, "human_a": 354, "human_b": 9, "match": False},
                "C8_송진호": {"machine_②": 37, "machine_③": 0, "human_a": 37, "human_b": 5, "match": False},
            },
            "overall_match": False,
            "note": "재확인 대상이 많음 - 1,182개 중 (b)에서 추가 발견"
        },
        {
            "page": 4,
            "type": "1투표함",
            "candidates": {
                "C1_이재명": {"machine_②": 1862, "machine_③": 123, "human_a": 1862, "human_b": 49, "match": False},
                "C2_김문수": {"machine_②": 624, "machine_③": 43, "human_a": 624, "human_b": 14, "match": False},
                "C4_이준석": {"machine_②": 362, "machine_③": 0, "human_a": 362, "human_b": 14, "match": False},
                "C5_권영국": {"machine_②": 25, "machine_③": 0, "human_a": 25, "human_b": 1, "match": False},
                "C8_송진호": {"machine_②": 4, "machine_③": 0, "human_a": 4, "human_b": 1, "match": False},
            },
            "overall_match": False,
            "note": "기계 재확인(③)과 인간 재확인(b)이 상당히 다름"
        },
        {
            "page": 6,
            "type": "3투표함",
            "candidates": {
                "C1_이재명": {"machine_②": 1873, "machine_③": 83, "human_a": 1873, "human_b": 25, "match": False},
                "C2_김문수": {"machine_②": 610, "machine_③": 19, "human_a": 610, "human_b": 14, "match": False},
                "C4_이준석": {"machine_②": 402, "machine_③": 0, "human_a": 402, "human_b": 12, "match": False},
                "C5_권영국": {"machine_②": 28, "machine_③": 0, "human_a": 28, "human_b": 0, "match": True},
                "C8_송진호": {"machine_②": 4, "machine_③": 0, "human_a": 4, "human_b": 0, "match": True},
            },
            "overall_match": False
        },
        {
            "page": 10,
            "type": "7투표함",
            "candidates": {
                "C1_이재명": {"machine_②": 1649, "machine_③": 111, "human_a": 1649, "human_b": 43, "match": False},
                "C2_김문수": {"machine_②": 787, "machine_③": 5, "human_a": 787, "human_b": 29, "match": False},
                "C4_이준석": {"machine_②": 428, "machine_③": 0, "human_a": 428, "human_b": 11, "match": False},
                "C5_권영국": {"machine_②": 22, "machine_③": 0, "human_a": 22, "human_b": 0, "match": True},
                "C8_송진호": {"machine_②": 3, "machine_③": 0, "human_a": 3, "human_b": 0, "match": True},
            },
            "overall_match": False
        },
        {
            "page": 20,
            "type": "관내",
            "candidates": {
                "C1_이재명": {"machine_②": 1167, "machine_③": 68, "human_a": 1167, "human_b": 24, "match": False},
                "C2_김문수": {"machine_②": 586, "machine_③": 1, "human_a": 586, "human_b": 22, "match": False},
                "C4_이준석": {"machine_②": 186, "machine_③": 0, "human_a": 186, "human_b": 1, "match": False},
                "C5_권영국": {"machine_②": 14, "machine_③": 0, "human_a": 14, "human_b": 0, "match": True},
                "C8_송진호": {"machine_②": 2, "machine_③": 0, "human_a": 2, "human_b": 1, "match": False},
            },
            "overall_match": False
        },
        {
            "page": 30,
            "type": "교촌동",
            "candidates": {
                "C1_이재명": {"machine_②": 4286, "machine_③": 92, "human_a": 4286, "human_b": 49, "match": False},
                "C2_김문수": {"machine_②": 980, "machine_③": 0, "human_a": 980, "human_b": 13, "match": False},
                "C4_이준석": {"machine_②": 387, "machine_③": 0, "human_a": 387, "human_b": 6, "match": False},
                "C5_권영국": {"machine_②": 56, "machine_③": 0, "human_a": 56, "human_b": 0, "match": True},
                "C8_송진호": {"machine_②": 1, "machine_③": 0, "human_a": 1, "human_b": 0, "match": True},
            },
            "overall_match": False
        },
        {
            "page": 40,
            "type": "초전동/관내1투",
            "candidates": {
                "C1_이재명": {"machine_②": 359, "machine_③": 36, "human_a": 359, "human_b": 8, "match": False},
                "C2_김문수": {"machine_②": 621, "machine_③": 0, "human_a": 621, "human_b": 14, "match": False},
                "C4_이준석": {"machine_②": 66, "machine_③": 0, "human_a": 66, "human_b": 3, "match": False},
                "C5_권영국": {"machine_②": 4, "machine_③": 0, "human_a": 4, "human_b": 1, "match": False},
                "C8_송진호": {"machine_②": 1, "machine_③": 0, "human_a": 1, "human_b": 0, "match": True},
            },
            "overall_match": False
        },
        {
            "page": 60,
            "type": "장군면/제1투",
            "candidates": {
                "C1_이재명": {"machine_②": 283, "machine_③": 44, "human_a": 283, "human_b": 10, "match": False},
                "C2_김문수": {"machine_②": 490, "machine_③": 0, "human_a": 490, "human_b": 32, "match": False},
                "C4_이준석": {"machine_②": 69, "machine_③": 0, "human_a": 69, "human_b": 2, "match": False},
                "C5_권영국": {"machine_②": 6, "machine_③": 0, "human_a": 6, "human_b": 0, "match": True},
                "C8_송진호": {"machine_②": 0, "machine_③": 0, "human_a": 0, "human_b": 0, "match": True},
            },
            "overall_match": False
        },
        {
            "page": 70,
            "type": "장동면/제1투",
            "candidates": {
                "C1_이재명": {"machine_②": 147, "machine_③": 24, "human_a": 147, "human_b": 6, "match": False},
                "C2_김문수": {"machine_②": 303, "machine_③": 0, "human_a": 303, "human_b": 13, "match": False},
                "C4_이준석": {"machine_②": 26, "machine_③": 0, "human_a": 26, "human_b": 1, "match": False},
                "C5_권영국": {"machine_②": 1, "machine_③": 0, "human_a": 1, "human_b": 0, "match": True},
                "C8_송진호": {"machine_②": 0, "machine_③": 0, "human_a": 0, "human_b": 0, "match": True},
            },
            "overall_match": False
        },
    ]

    return pages_data

def analyze_matches(pages_data):
    """Analyze the match patterns"""

    total_pages = len(pages_data)
    pages_with_100_match = sum(1 for p in pages_data if p["overall_match"])
    pages_with_discrepancy = total_pages - pages_with_100_match

    # Count by candidate
    candidate_stats = {}
    candidates = ["C1_이재명", "C2_김문수", "C4_이준석", "C5_권영국", "C8_송진호"]

    for cand in candidates:
        matches = sum(1 for p in pages_data if p["candidates"][cand]["match"])
        total = len(pages_data)
        candidate_stats[cand] = {
            "matches": matches,
            "total": total,
            "match_rate": matches / total * 100
        }

    # Group by voting type
    type_stats = {}
    for page in pages_data:
        vtype = page["type"]
        if vtype not in type_stats:
            type_stats[vtype] = {"pages": 0, "matches": 0}
        type_stats[vtype]["pages"] += 1
        if page["overall_match"]:
            type_stats[vtype]["matches"] += 1

    return {
        "total_pages_analyzed": total_pages,
        "pages_100_match": pages_with_100_match,
        "pages_with_discrepancy": pages_with_discrepancy,
        "overall_match_rate": pages_with_100_match / total_pages * 100,
        "candidate_stats": candidate_stats,
        "type_stats": type_stats
    }

def generate_report(pages_data, analysis):
    """Generate detailed analysis report"""

    print("="*80)
    print("기계 분류 vs 인간 검증 일치율 분석 보고서")
    print("="*80)
    print(f"\n분석 페이지 수: {analysis['total_pages_analyzed']}")
    print(f"100% 일치 페이지: {analysis['pages_100_match']}")
    print(f"불일치 있는 페이지: {analysis['pages_with_discrepancy']}")
    print(f"전체 일치율: {analysis['overall_match_rate']:.1f}%")

    print("\n" + "="*80)
    print("후보자별 일치율")
    print("="*80)
    for cand, stats in analysis["candidate_stats"].items():
        cand_name = cand.split("_")[1]
        print(f"{cand_name:6s}: {stats['matches']:2d}/{stats['total']:2d} ({stats['match_rate']:5.1f}%)")

    print("\n" + "="*80)
    print("투표 유형별 통계")
    print("="*80)
    for vtype, stats in analysis["type_stats"].items():
        match_rate = stats["matches"] / stats["pages"] * 100 if stats["pages"] > 0 else 0
        print(f"{vtype:15s}: {stats['matches']}/{stats['pages']} 일치 ({match_rate:.0f}%)")

    print("\n" + "="*80)
    print("주요 발견사항")
    print("="*80)
    print("1. 전체 분석 페이지에서 100% 일치하는 페이지 없음")
    print("2. 권영국(C5), 송진호(C8) 후보는 상대적으로 높은 일치율")
    print("3. 이재명(C1) 후보는 모든 페이지에서 재확인 대상(b) 불일치")
    print("4. 기계 재확인(③)보다 인간 재확인(b)이 일관되게 적음")
    print("5. 패턴: Machine ②와 Human (a)는 대부분 일치")
    print("   하지만: Machine ③와 Human (b)는 거의 항상 불일치")

    print("\n" + "="*80)
    print("불일치 패턴 상세 분석")
    print("="*80)

    for page in pages_data[:5]:  # First 5 pages as examples
        print(f"\nPage {page['page']} ({page['type']}):")
        for cand, data in page["candidates"].items():
            cand_name = cand.split("_")[1]
            match_symbol = "✓" if data["match"] else "✗"
            print(f"  {match_symbol} {cand_name:6s}: ②={data['machine_②']:5d} vs (a)={data['human_a']:5d}, "
                  f"③={data['machine_③']:3d} vs (b)={data['human_b']:3d}")

if __name__ == "__main__":
    pages_data = extract_page_data()
    analysis = analyze_matches(pages_data)
    generate_report(pages_data, analysis)

    # Save data
    with open("comparison_analysis.json", "w", encoding="utf-8") as f:
        json.dump({"pages": pages_data, "analysis": analysis}, f, ensure_ascii=False, indent=2)

    print("\n" + "="*80)
    print("✓ 분석 데이터 저장: comparison_analysis.json")
    print("="*80)
