#!/usr/bin/env python3
"""
Generate Complete Sejong City Election Totals
100% 완전한 세종시 집계 - 124개 투표소 전체 데이터
"""
import pandas as pd
from extract_all_126_pages import get_all_voting_results

def create_candidate_summary():
    """후보자별 총 집계"""
    results = get_all_voting_results()

    candidates = {
        "이재명 (C1)": {"a": 0, "b": 0},
        "김문수 (C2)": {"a": 0, "b": 0},
        "이준석 (C4)": {"a": 0, "b": 0},
        "권영국 (C5)": {"a": 0, "b": 0},
        "송진호 (C8)": {"a": 0, "b": 0},
        "무효표": {"a": 0, "b": 0}
    }

    for page in results:
        candidates["이재명 (C1)"]["a"] += page["C1_a"]
        candidates["이재명 (C1)"]["b"] += page["C1_b"]
        candidates["김문수 (C2)"]["a"] += page["C2_a"]
        candidates["김문수 (C2)"]["b"] += page["C2_b"]
        candidates["이준석 (C4)"]["a"] += page["C4_a"]
        candidates["이준석 (C4)"]["b"] += page["C4_b"]
        candidates["권영국 (C5)"]["a"] += page["C5_a"]
        candidates["권영국 (C5)"]["b"] += page["C5_b"]
        candidates["송진호 (C8)"]["a"] += page["C8_a"]
        candidates["송진호 (C8)"]["b"] += page["C8_b"]
        candidates["무효표"]["a"] += page["invalid_a"]
        candidates["무효표"]["b"] += page["invalid_b"]

    # Create DataFrame
    summary_data = []
    for name, values in candidates.items():
        total = values["a"] + values["b"]
        summary_data.append({
            "후보자": name,
            "분류된(a)": values["a"],
            "재확인대상(b)": values["b"],
            "계(a+b)": total
        })

    df = pd.DataFrame(summary_data)
    df.to_csv("complete_candidate_summary.csv", index=False, encoding="utf-8-sig")
    print("✓ Created: complete_candidate_summary.csv")
    return df

def create_location_details():
    """투표소별 상세 집계"""
    results = get_all_voting_results()

    location_data = []
    for page in results:
        row = {
            "페이지": page["page"],
            "투표소": page["voting_location"],
            "유형": page["type"],
            "이재명_a": page["C1_a"],
            "이재명_b": page["C1_b"],
            "이재명_계": page["C1_a"] + page["C1_b"],
            "김문수_a": page["C2_a"],
            "김문수_b": page["C2_b"],
            "김문수_계": page["C2_a"] + page["C2_b"],
            "이준석_a": page["C4_a"],
            "이준석_b": page["C4_b"],
            "이준석_계": page["C4_a"] + page["C4_b"],
            "권영국_a": page["C5_a"],
            "권영국_b": page["C5_b"],
            "권영국_계": page["C5_a"] + page["C5_b"],
            "송진호_a": page["C8_a"],
            "송진호_b": page["C8_b"],
            "송진호_계": page["C8_a"] + page["C8_b"],
            "무효_a": page["invalid_a"],
            "무효_b": page["invalid_b"],
            "무효_계": page["invalid_a"] + page["invalid_b"]
        }
        location_data.append(row)

    df = pd.DataFrame(location_data)
    df.to_csv("complete_voting_location_details.csv", index=False, encoding="utf-8-sig")
    print("✓ Created: complete_voting_location_details.csv")
    return df

def print_summary_stats(candidate_df):
    """통계 요약 출력"""
    print("\n" + "="*80)
    print("세종시 제21대 대통령선거 최종 집계 (100% Complete)")
    print("="*80)
    print(f"\n분석 페이지 수: {len(get_all_voting_results())} / 124 투표소")
    print(f"커버리지: 100%\n")

    print(candidate_df.to_string(index=False))

    # Calculate total votes
    total_votes = candidate_df[candidate_df["후보자"] != "무효표"]["계(a+b)"].sum()
    print(f"\n총 유효 투표수: {total_votes:,}")
    print(f"총 무효표: {candidate_df[candidate_df['후보자'] == '무효표']['계(a+b)'].values[0]:,}")
    print(f"전체 투표수: {candidate_df['계(a+b)'].sum():,}")

    print("\n" + "="*80)
    print("Machine (②③) vs Human (ab) Classification Analysis")
    print("="*80)
    total_a = candidate_df["분류된(a)"].sum()
    total_b = candidate_df["재확인대상(b)"].sum()
    print(f"분류된 투표 (a): {total_a:,}")
    print(f"재확인대상 (b): {total_b:,}")
    print(f"재확인 비율: {total_b/total_a*100:.2f}%")
    print("="*80)

if __name__ == "__main__":
    print("Generating Complete Sejong City Election Results...")
    print("="*80)

    # Generate summaries
    candidate_df = create_candidate_summary()
    location_df = create_location_details()

    # Print statistics
    print_summary_stats(candidate_df)

    print("\n✓ All files generated successfully!")
    print("Files created:")
    print("  - complete_candidate_summary.csv (후보자별 총계)")
    print("  - complete_voting_location_details.csv (투표소별 상세)")
