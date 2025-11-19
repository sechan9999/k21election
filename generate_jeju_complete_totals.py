#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
제주시 선거 데이터 집계 스크립트
Generate complete totals and analysis from Jeju election data

작성일: 2025-11-19
입력: complete_jeju_voting_location_details.csv
출력: complete_jeju_candidate_summary.csv
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 경로 설정
DATA_DIR = Path("/home/user/k21election/jeju_data")
INPUT_CSV = DATA_DIR / "complete_jeju_voting_location_details.csv"
OUTPUT_SUMMARY = DATA_DIR / "complete_jeju_candidate_summary.csv"
OUTPUT_JSON = DATA_DIR / "jeju_analysis_report.json"

# 후보자 정의
CANDIDATES = {
    1: {"name": "이재명", "party": "더불어민주당"},
    2: {"name": "김문수", "party": "국민의힘"},
    4: {"name": "이준석", "party": "개혁신당"},
    5: {"name": "권영국", "party": "민주노동당"},
    8: {"name": "송진호", "party": "무소속"}
}


def load_voting_data(input_path: Path) -> List[Dict]:
    """투표소별 데이터 로드"""
    data = []
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictWriter(f)
        for row in reader:
            data.append(row)
    return data


def calculate_candidate_totals(input_path: Path) -> Dict:
    """후보자별 총득표 계산"""

    summary = {}
    for cand_num in CANDIDATES:
        summary[cand_num] = {
            "candidate_number": cand_num,
            "name": CANDIDATES[cand_num]["name"],
            "party": CANDIDATES[cand_num]["party"],
            "total_votes": 0,
            "vote_percentage": 0.0
        }

    # 데이터 읽기 및 집계
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            summary[1]["total_votes"] += int(row.get("이재명_득표", 0))
            summary[2]["total_votes"] += int(row.get("김문수_득표", 0))
            summary[4]["total_votes"] += int(row.get("이준석_득표", 0))
            summary[5]["total_votes"] += int(row.get("권영국_득표", 0))
            summary[8]["total_votes"] += int(row.get("송진호_득표", 0))

    # 총 득표 계산
    total_votes = sum(s["total_votes"] for s in summary.values())

    # 득표율 계산
    if total_votes > 0:
        for cand_num in summary:
            summary[cand_num]["vote_percentage"] = round(
                summary[cand_num]["total_votes"] / total_votes * 100, 2
            )

    return summary, total_votes


def calculate_statistics(input_path: Path) -> Dict:
    """전체 통계 계산"""

    stats = {
        "total_pages": 0,
        "total_eligible_voters": 0,
        "total_ballots": 0,
        "total_valid_votes": 0,
        "total_invalid_votes": 0,
        "turnout_rate": 0.0,
        "valid_vote_rate": 0.0,
        "vote_types": {}
    }

    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stats["total_pages"] += 1
            stats["total_eligible_voters"] += int(row.get("eligible_voters", 0))
            stats["total_ballots"] += int(row.get("total_ballots", 0))
            stats["total_valid_votes"] += int(row.get("valid_votes", 0))
            stats["total_invalid_votes"] += int(row.get("invalid_votes", 0))

            # 투표 유형별 집계
            vote_type = row.get("vote_type", "선거일투표")
            if vote_type not in stats["vote_types"]:
                stats["vote_types"][vote_type] = {
                    "count": 0,
                    "total_votes": 0
                }
            stats["vote_types"][vote_type]["count"] += 1
            stats["vote_types"][vote_type]["total_votes"] += int(row.get("valid_votes", 0))

    # 비율 계산
    if stats["total_eligible_voters"] > 0:
        stats["turnout_rate"] = round(
            stats["total_ballots"] / stats["total_eligible_voters"] * 100, 2
        )

    if stats["total_ballots"] > 0:
        stats["valid_vote_rate"] = round(
            stats["total_valid_votes"] / stats["total_ballots"] * 100, 2
        )

    return stats


def save_candidate_summary(summary: Dict, total_votes: int, output_path: Path):
    """후보자별 집계 CSV 저장"""

    fieldnames = ["candidate_number", "name", "party", "total_votes", "vote_percentage"]

    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        # 득표순으로 정렬
        sorted_summary = sorted(summary.values(), key=lambda x: x["total_votes"], reverse=True)

        for row in sorted_summary:
            writer.writerow(row)

    print(f"✓ 후보자별 집계 저장: {output_path}")

    # 콘솔 출력
    print(f"\n{'=' * 70}")
    print(f"후보자별 득표 집계")
    print(f"{'=' * 70}")
    for row in sorted_summary:
        print(f"{row['candidate_number']}. {row['name']:8s} ({row['party']:12s}): {row['total_votes']:8,}표 ({row['vote_percentage']:6.2f}%)")
    print(f"{'=' * 70}")
    print(f"총 유효표: {total_votes:,}표")
    print(f"{'=' * 70}\n")


def save_json_report(summary: Dict, stats: Dict, total_votes: int, output_path: Path):
    """JSON 형식 보고서 저장"""

    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source_file": str(INPUT_CSV),
            "analysis_version": "1.0"
        },
        "summary_statistics": {
            **stats,
            "total_candidate_votes": total_votes
        },
        "candidate_results": sorted(
            summary.values(),
            key=lambda x: x["total_votes"],
            reverse=True
        )
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"✓ JSON 보고서 저장: {output_path}")


def print_statistics(stats: Dict):
    """통계 정보 출력"""

    print(f"\n{'=' * 70}")
    print(f"전체 통계")
    print(f"{'=' * 70}")
    print(f"처리된 페이지: {stats['total_pages']} 페이지")
    print(f"총 선거인 수: {stats['total_eligible_voters']:,}명")
    print(f"총 투표자 수: {stats['total_ballots']:,}명")
    print(f"투표율: {stats['turnout_rate']:.2f}%")
    print(f"총 유효표: {stats['total_valid_votes']:,}표")
    print(f"총 무효표: {stats['total_invalid_votes']:,}표")
    print(f"유효표율: {stats['valid_vote_rate']:.2f}%")

    if stats["vote_types"]:
        print(f"\n투표 유형별 집계:")
        for vote_type, data in stats["vote_types"].items():
            print(f"  - {vote_type}: {data['count']:,}개 투표함, {data['total_votes']:,}표")

    print(f"{'=' * 70}\n")


def main():
    """메인 실행 함수"""

    print(f"\n{'=' * 70}")
    print(f"제주시 선거 데이터 집계 스크립트")
    print(f"{'=' * 70}")
    print(f"입력 파일: {INPUT_CSV}")
    print(f"출력 파일:")
    print(f"  - {OUTPUT_SUMMARY}")
    print(f"  - {OUTPUT_JSON}")
    print(f"{'=' * 70}\n")

    # 입력 파일 확인
    if not INPUT_CSV.exists():
        print(f"✗ 오류: 입력 파일을 찾을 수 없습니다: {INPUT_CSV}")
        return 1

    # 후보자별 집계
    print("후보자별 득표 집계 중...")
    summary, total_votes = calculate_candidate_totals(INPUT_CSV)

    # 전체 통계 계산
    print("전체 통계 계산 중...")
    stats = calculate_statistics(INPUT_CSV)

    # 결과 저장
    print("\n결과 저장 중...")
    save_candidate_summary(summary, total_votes, OUTPUT_SUMMARY)
    save_json_report(summary, stats, total_votes, OUTPUT_JSON)

    # 통계 출력
    print_statistics(stats)

    print(f"\n✅ 모든 집계 완료!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
