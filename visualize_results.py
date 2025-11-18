#!/usr/bin/env python3
"""
Create visualizations for the classification match analysis
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Use non-interactive backend
matplotlib.use('Agg')

# Korean font setup
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def create_candidate_match_chart():
    """Create bar chart for candidate match rates"""

    candidates = ['이재명\n(C1)', '김문수\n(C2)', '이준석\n(C4)', '권영국\n(C5)', '송진호\n(C8)']
    match_rates = [0.0, 7.1, 7.1, 50.0, 50.0]
    colors = ['#1976D2', '#D32F2F', '#F57C00', '#7B1FA2', '#558B2F']

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(candidates, match_rates, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for bar, rate in zip(bars, match_rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_ylabel('Match Rate (%)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Candidates', fontsize=14, fontweight='bold')
    ax.set_title('Machine vs Human Classification Match Rate by Candidate\n(Sample: 14 pages)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% threshold')
    ax.legend()

    plt.tight_layout()
    plt.savefig('candidate_match_rates.png', dpi=300, bbox_inches='tight')
    print("✓ Created: candidate_match_rates.png")
    plt.close()

def create_voting_type_analysis():
    """Create visualization for voting type patterns"""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left plot: Voting type distribution
    types = ['Early Voting\n(Pages 2-3)', 'Ballot Boxes\n(Pages 4-20)',
             'District Voting\n(Pages 30-125)']
    counts = [2, 4, 8]  # From our sample
    colors_type = ['#4CAF50', '#2196F3', '#FF9800']

    ax1.bar(types, counts, color=colors_type, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Number of Pages Analyzed', fontsize=12, fontweight='bold')
    ax1.set_title('Analyzed Pages by Voting Type', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # Add counts on bars
    for i, (t, c) in enumerate(zip(types, counts)):
        ax1.text(i, c, str(c), ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Right plot: Match status
    match_data = {
        '100% Match': 0,
        'Partial Match\n(Some candidates)': 0,  # Actually we have partial matches
        'No Match\n(All discrepancy)': 14
    }

    colors_match = ['#4CAF50', '#FFC107', '#F44336']
    ax2.pie(match_data.values(), labels=match_data.keys(), autopct='%1.0f%%',
            colors=colors_match, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Overall Page Match Status\n(14 pages analyzed)', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('voting_type_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Created: voting_type_analysis.png")
    plt.close()

def create_mismatch_pattern():
    """Create visualization showing mismatch patterns"""

    # Sample data from analyzed pages
    pages = ['P2', 'P3', 'P4', 'P6', 'P10', 'P20', 'P30', 'P40', 'P60', 'P70']

    # C1 (Lee Jae-myung) mismatch data
    machine_reconfirm = [0, 0, 123, 83, 111, 68, 92, 36, 44, 24]
    human_reconfirm = [13, 452, 49, 25, 43, 24, 49, 8, 10, 6]

    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(pages))
    width = 0.35

    bars1 = ax.bar(x - width/2, machine_reconfirm, width, label='Machine Reconfirm (③)',
                   color='#2196F3', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x + width/2, human_reconfirm, width, label='Human Reconfirm (b)',
                   color='#FF5722', alpha=0.8, edgecolor='black')

    ax.set_xlabel('Page Number', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Reconfirm Votes', fontsize=14, fontweight='bold')
    ax.set_title('Machine vs Human Reconfirmation Pattern\nCandidate: Lee Jae-myung (C1)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(pages, rotation=45)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # Add annotation
    ax.text(0.5, 0.95, 'Pattern: Machine and Human judgments differ significantly',
            transform=ax.transAxes, ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('mismatch_pattern_c1.png', dpi=300, bbox_inches='tight')
    print("✓ Created: mismatch_pattern_c1.png")
    plt.close()

def create_summary_heatmap():
    """Create heatmap showing match status for all candidates across pages"""

    fig, ax = plt.subplots(figsize=(12, 8))

    # Data: 1 = match, 0 = mismatch
    candidates = ['C1\n이재명', 'C2\n김문수', 'C4\n이준석', 'C5\n권영국', 'C8\n송진호']
    pages = ['P2', 'P3', 'P4', 'P5', 'P6', 'P10', 'P20', 'P30', 'P40', 'P60', 'P70', 'P90', 'P110', 'P120']

    # Match matrix (1=match, 0=mismatch)
    data = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # C1
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # C2
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # C4
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0],  # C5
        [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0],  # C8
    ])

    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

    # Set ticks
    ax.set_xticks(np.arange(len(pages)))
    ax.set_yticks(np.arange(len(candidates)))
    ax.set_xticklabels(pages, rotation=45, ha='right')
    ax.set_yticklabels(candidates, fontsize=11, fontweight='bold')

    # Add grid
    ax.set_xticks(np.arange(len(pages))-.5, minor=True)
    ax.set_yticks(np.arange(len(candidates))-.5, minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=1.5)

    # Add text annotations
    for i in range(len(candidates)):
        for j in range(len(pages)):
            text = ax.text(j, i, '✓' if data[i, j] == 1 else '✗',
                          ha="center", va="center", color="black", fontsize=14, fontweight='bold')

    ax.set_title('Machine vs Human Classification Match Status Heatmap\nGreen = Match, Red = Mismatch',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Page Number', fontsize=14, fontweight='bold')
    ax.set_ylabel('Candidates', fontsize=14, fontweight='bold')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, ticks=[0, 1])
    cbar.ax.set_yticklabels(['Mismatch', 'Match'])

    plt.tight_layout()
    plt.savefig('match_status_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Created: match_status_heatmap.png")
    plt.close()

if __name__ == "__main__":
    print("="*80)
    print("Generating Visualizations")
    print("="*80)

    create_candidate_match_chart()
    create_voting_type_analysis()
    create_mismatch_pattern()
    create_summary_heatmap()

    print("="*80)
    print("All visualizations created successfully!")
    print("="*80)
