#!/usr/bin/env python3
"""
Manual data extraction helper for comparing machine vs human counts
This script will display each page and collect the comparison data
"""
import os
import json

# Template for data extraction
def create_template():
    """Create CSV template for manual data entry"""

    template = {
        "page_number": 0,
        "voting_type": "",  # e.g., "관외사전", "관내", "선거일투표"
        "ballot_box": "",   # e.g., "투표함 1", "2투표함"
        "machine_classification": {
            "candidate_1_lee_jae_myung": {"machine_classified": 0, "machine_reconfirm": 0},
            "candidate_2_kim_moon_soo": {"machine_classified": 0, "machine_reconfirm": 0},
            "candidate_4_lee_jun_seok": {"machine_classified": 0, "machine_reconfirm": 0},
            "candidate_5_kwon_young_kook": {"machine_classified": 0, "machine_reconfirm": 0},
            "candidate_8_song_jin_ho": {"machine_classified": 0, "machine_reconfirm": 0},
            "invalid_votes": {"machine_classified": 0, "machine_reconfirm": 0},
        },
        "human_verification": {
            "candidate_1_lee_jae_myung": {"verified_a": 0, "verified_b": 0},
            "candidate_2_kim_moon_soo": {"verified_a": 0, "verified_b": 0},
            "candidate_4_lee_jun_seok": {"verified_a": 0, "verified_b": 0},
            "candidate_5_kwon_young_kook": {"verified_a": 0, "verified_b": 0},
            "candidate_8_song_jin_ho": {"verified_a": 0, "verified_b": 0},
            "invalid_votes": {"verified_a": 0, "verified_b": 0},
        },
        "match_status": {
            "candidate_1": False,
            "candidate_2": False,
            "candidate_4": False,
            "candidate_5": False,
            "candidate_8": False,
            "invalid": False,
            "overall_match": False
        }
    }

    return template

def save_csv_header():
    """Generate CSV header for manual data entry"""

    header = [
        "Page",
        "VotingType",
        "BallotBox",
        # Machine Classification (②, ③)
        "M_C1_②", "M_C1_③",
        "M_C2_②", "M_C2_③",
        "M_C4_②", "M_C4_③",
        "M_C5_②", "M_C5_③",
        "M_C8_②", "M_C8_③",
        "M_Invalid_②", "M_Invalid_③",
        # Human Verification (a, b)
        "H_C1_a", "H_C1_b",
        "H_C2_a", "H_C2_b",
        "H_C4_a", "H_C4_b",
        "H_C5_a", "H_C5_b",
        "H_C8_a", "H_C8_b",
        "H_Invalid_a", "H_Invalid_b",
        # Match status
        "Match_C1", "Match_C2", "Match_C4", "Match_C5", "Match_C8", "Match_Invalid",
        "Overall_Match"
    ]

    return ",".join(header)

if __name__ == "__main__":
    # Save template
    with open("data_extraction_template.json", "w", encoding="utf-8") as f:
        json.dump(create_template(), f, ensure_ascii=False, indent=2)

    # Save CSV header
    with open("manual_extraction.csv", "w", encoding="utf-8") as f:
        f.write(save_csv_header() + "\n")

    print("✓ Created data_extraction_template.json")
    print("✓ Created manual_extraction.csv with headers")
    print("\nTo compare machine vs human counts:")
    print("1. For each page, check if ② = (a) AND ③ = (b)")
    print("2. If both match for ALL candidates → 100% match")
    print("3. Record any discrepancies")
