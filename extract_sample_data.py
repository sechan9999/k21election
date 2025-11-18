#!/usr/bin/env python3
"""
Extract data from a representative sample of pages to analyze match patterns
"""

def create_sample_plan():
    """
    Create a plan to sample pages from each voting type
    """

    sample_pages = [
        # Early voting
        {"page": 2, "type": "관외투표", "description": "Out-of-district voting"},
        {"page": 3, "type": "관내사전", "description": "In-district advance voting - 1"},

        # Ballot boxes (투표함)
        {"page": 4, "type": "투표함 1", "description": "Ballot box 1"},
        {"page": 5, "type": "투표함 2", "description": "Ballot box 2"},
        {"page": 6, "type": "투표함 3", "description": "Ballot box 3"},
        {"page": 10, "type": "투표함", "description": "Later ballot box"},

        # District voting (선거일 - 동별)
        {"page": 20, "type": "관내", "description": "In-district"},
        {"page": 30, "type": "아름동", "description": "Areum-dong"},
        {"page": 40, "type": "나성동", "description": "Naseong-dong"},
        {"page": 50, "type": "초전동/제11투", "description": "Chojeon-dong box 11"},
        {"page": 60, "type": "도담동", "description": "Dodam-dong"},
        {"page": 70, "type": "도담동", "description": "Dodam-dong (continued)"},
        {"page": 80, "type": "도담동/제3투", "description": "Dodam-dong box 3"},
        {"page": 90, "type": "보람동", "description": "Boram-dong"},
        {"page": 100, "type": "보람동/제3투", "description": "Boram-dong box 3"},
        {"page": 110, "type": "새롬동", "description": "Saerom-dong"},
        {"page": 120, "type": "종촌동", "description": "Jongchon-dong"},
        {"page": 125, "type": "한솔동", "description": "Hansol-dong"},
    ]

    return sample_pages

if __name__ == "__main__":
    samples = create_sample_plan()

    print("="*80)
    print("REPRESENTATIVE SAMPLE PLAN")
    print("="*80)
    print(f"\nTotal sample pages: {len(samples)}")

    print("\n\nPages to review:")
    for i, sample in enumerate(samples, 1):
        print(f"{i:2d}. Page {sample['page']:3d}: {sample['type']:20s} - {sample['description']}")

    print("\n" + "="*80)
    print("These pages represent:")
    print("  - Early voting types (관외투표, 관내사전)")
    print("  - Ballot box voting (투표함 1-3, etc.)")
    print("  - Election day voting by district (동별)")
    print("  - Various locations across Sejong City")
    print("="*80)
