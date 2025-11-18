#!/usr/bin/env python3
"""
Extract human verification results (a) and (b) from analyzed pages
"""
import pandas as pd

def get_voting_results():
    """
    Extract (a) and (b) values from the 14 analyzed pages
    Based on manual review of page images
    """

    results = [
        {
            "page": 2,
            "voting_location": "관외투표",
            "type": "Out-of-district voting",
            "C1_a": 1227, "C1_b": 13,
            "C2_a": 375, "C2_b": 0,
            "C4_a": 209, "C4_b": 39,
            "C5_a": 44, "C5_b": 1,
            "C8_a": 1, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 0  # Not visible in image
        },
        {
            "page": 3,
            "voting_location": "관내사전",
            "type": "In-district advance voting",
            "C1_a": 19900, "C1_b": 452,
            "C2_a": 7679, "C2_b": 280,
            "C4_a": 4520, "C4_b": 128,
            "C5_a": 354, "C5_b": 9,
            "C8_a": 37, "C8_b": 5,
            "invalid_a": 0, "invalid_b": 308  # 무효투표수
        },
        {
            "page": 4,
            "voting_location": "투표함 1",
            "type": "Ballot box 1 (1투표함)",
            "C1_a": 1862, "C1_b": 49,
            "C2_a": 624, "C2_b": 14,
            "C4_a": 362, "C4_b": 14,
            "C5_a": 25, "C5_b": 1,
            "C8_a": 4, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 27
        },
        {
            "page": 5,
            "voting_location": "투표함 2",
            "type": "Ballot box 2 (2투표함)",
            "C1_a": 1865, "C1_b": 56,
            "C2_a": 616, "C2_b": 28,
            "C4_a": 370, "C4_b": 14,
            "C5_a": 29, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 21
        },
        {
            "page": 6,
            "voting_location": "투표함 3",
            "type": "Ballot box 3 (3투표함)",
            "C1_a": 1873, "C1_b": 25,
            "C2_a": 610, "C2_b": 14,
            "C4_a": 402, "C4_b": 12,
            "C5_a": 28, "C5_b": 0,
            "C8_a": 4, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 32
        },
        {
            "page": 10,
            "voting_location": "투표함 7",
            "type": "Ballot box 7 (7투표함)",
            "C1_a": 1649, "C1_b": 43,
            "C2_a": 787, "C2_b": 29,
            "C4_a": 428, "C4_b": 11,
            "C5_a": 22, "C5_b": 0,
            "C8_a": 3, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 28
        },
        {
            "page": 20,
            "voting_location": "관내",
            "type": "In-district (관내)",
            "C1_a": 1167, "C1_b": 24,
            "C2_a": 586, "C2_b": 22,
            "C4_a": 186, "C4_b": 1,
            "C5_a": 14, "C5_b": 0,
            "C8_a": 2, "C8_b": 1,
            "invalid_a": 0, "invalid_b": 20
        },
        {
            "page": 30,
            "voting_location": "교촌동",
            "type": "Gyochon-dong (교촌동)",
            "C1_a": 4286, "C1_b": 49,
            "C2_a": 980, "C2_b": 13,
            "C4_a": 387, "C4_b": 6,
            "C5_a": 56, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 24
        },
        {
            "page": 40,
            "voting_location": "초전동/관내1투",
            "type": "Chojeon-dong box 1 (선거일)",
            "C1_a": 359, "C1_b": 8,
            "C2_a": 621, "C2_b": 14,
            "C4_a": 66, "C4_b": 3,
            "C5_a": 4, "C5_b": 1,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 10
        },
        {
            "page": 60,
            "voting_location": "장군면/제1투",
            "type": "Janggun-myeon box 1 (선거일)",
            "C1_a": 283, "C1_b": 10,
            "C2_a": 490, "C2_b": 32,
            "C4_a": 69, "C4_b": 2,
            "C5_a": 6, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 9
        },
        {
            "page": 70,
            "voting_location": "장동면/제1투",
            "type": "Jangdong-myeon box 1 (선거일)",
            "C1_a": 147, "C1_b": 6,
            "C2_a": 303, "C2_b": 13,
            "C4_a": 26, "C4_b": 1,
            "C5_a": 1, "C5_b": 0,
            "C8_a": 0, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 4
        },
        {
            "page": 90,
            "voting_location": "종촌동/제4투",
            "type": "Jongchon-dong box 4 (선거일)",
            "C1_a": 671, "C1_b": 9,
            "C2_a": 596, "C2_b": 13,
            "C4_a": 124, "C4_b": 3,
            "C5_a": 19, "C5_b": 1,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 5
        },
        {
            "page": 110,
            "voting_location": "소담동/제4투",
            "type": "Sodam-dong box 4 (선거일)",
            "C1_a": 634, "C1_b": 3,
            "C2_a": 667, "C2_b": 8,
            "C4_a": 144, "C4_b": 1,
            "C5_a": 21, "C5_b": 0,
            "C8_a": 1, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 12
        },
        {
            "page": 120,
            "voting_location": "반곡동/제3투",
            "type": "Bangok-dong box 3 (선거일)",
            "C1_a": 1257, "C1_b": 9,
            "C2_a": 755, "C2_b": 8,
            "C4_a": 252, "C4_b": 5,
            "C5_a": 24, "C5_b": 1,
            "C8_a": 2, "C8_b": 0,
            "invalid_a": 0, "invalid_b": 13
        },
    ]

    return results

def create_summary_table(results):
    """Create summary table for each page"""

    data = []
    for r in results:
        page_data = {
            "페이지": r["page"],
            "투표소": r["voting_location"],
            "이재명(a)": r["C1_a"],
            "이재명(b)": r["C1_b"],
            "이재명 계": r["C1_a"] + r["C1_b"],
            "김문수(a)": r["C2_a"],
            "김문수(b)": r["C2_b"],
            "김문수 계": r["C2_a"] + r["C2_b"],
            "이준석(a)": r["C4_a"],
            "이준석(b)": r["C4_b"],
            "이준석 계": r["C4_a"] + r["C4_b"],
            "권영국(a)": r["C5_a"],
            "권영국(b)": r["C5_b"],
            "권영국 계": r["C5_a"] + r["C5_b"],
            "송진호(a)": r["C8_a"],
            "송진호(b)": r["C8_b"],
            "송진호 계": r["C8_a"] + r["C8_b"],
            "무효(a)": r["invalid_a"],
            "무효(b)": r["invalid_b"],
            "무효 계": r["invalid_a"] + r["invalid_b"],
        }
        data.append(page_data)

    df = pd.DataFrame(data)
    return df

def create_candidate_summary(results):
    """Create summary by candidate"""

    totals = {
        "C1_a": 0, "C1_b": 0,
        "C2_a": 0, "C2_b": 0,
        "C4_a": 0, "C4_b": 0,
        "C5_a": 0, "C5_b": 0,
        "C8_a": 0, "C8_b": 0,
        "invalid_a": 0, "invalid_b": 0,
    }

    for r in results:
        for key in totals.keys():
            totals[key] += r[key]

    summary = [
        ["이재명", totals["C1_a"], totals["C1_b"], totals["C1_a"] + totals["C1_b"]],
        ["김문수", totals["C2_a"], totals["C2_b"], totals["C2_a"] + totals["C2_b"]],
        ["이준석", totals["C4_a"], totals["C4_b"], totals["C4_a"] + totals["C4_b"]],
        ["권영국", totals["C5_a"], totals["C5_b"], totals["C5_a"] + totals["C5_b"]],
        ["송진호", totals["C8_a"], totals["C8_b"], totals["C8_a"] + totals["C8_b"]],
        ["무효표", totals["invalid_a"], totals["invalid_b"], totals["invalid_a"] + totals["invalid_b"]],
    ]

    # Calculate total
    total_a = sum([row[1] for row in summary])
    total_b = sum([row[2] for row in summary])
    total_sum = total_a + total_b
    summary.append(["총계", total_a, total_b, total_sum])

    df = pd.DataFrame(summary, columns=["후보자", "분류된 투표지 확인결과(a)", "재확인대상 투표지 확인결과(b)", "계(a+b)"])
    return df

if __name__ == "__main__":
    results = get_voting_results()

    print("="*100)
    print("후보자별 집계 (14개 샘플 페이지 합계)")
    print("="*100)

    candidate_summary = create_candidate_summary(results)
    print(candidate_summary.to_string(index=False))

    print("\n" + "="*100)
    print("투표소별 상세 결과")
    print("="*100)

    detailed = create_summary_table(results)
    print(detailed.to_string(index=False))

    # Save to CSV
    candidate_summary.to_csv("candidate_summary.csv", index=False, encoding='utf-8-sig')
    detailed.to_csv("voting_location_details.csv", index=False, encoding='utf-8-sig')

    print("\n" + "="*100)
    print("파일 저장 완료:")
    print("  - candidate_summary.csv: 후보자별 집계표")
    print("  - voting_location_details.csv: 투표소별 상세표")
    print("="*100)
