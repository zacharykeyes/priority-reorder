import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_priority_diagram():
    """Create a simple bar diagram showing priority and normal sections"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis('off')
    
    # Main bar
    bar_width = 8
    bar_height = 1
    bar_x = 1
    bar_y = 0.5
    
    # Priority section (40% of bar)
    priority_width = bar_width * 0.4
    priority_rect = patches.Rectangle((bar_x, bar_y), priority_width, bar_height, 
                                    facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax.add_patch(priority_rect)
    ax.text(bar_x + priority_width/2, bar_y + bar_height/2, 'PRIORITY', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    
    # Normal section (60% of bar)
    normal_x = bar_x + priority_width
    normal_width = bar_width * 0.6
    normal_rect = patches.Rectangle((normal_x, bar_y), normal_width, bar_height, 
                                  facecolor='#7ED321', edgecolor='black', linewidth=2)
    ax.add_patch(normal_rect)
    ax.text(normal_x + normal_width/2, bar_y + bar_height/2, 'NORMAL', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    
    # Divider line
    ax.plot([normal_x, normal_x], [bar_y, bar_y + bar_height], 'k-', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('priority_diagram.svg', bbox_inches='tight', 
                facecolor='none', edgecolor='none')
    plt.close()
    print("Generated: diagrams/priority_diagram.svg")

def create_sequential_priorities_diagram():
    """Create diagram showing multiple priorities in sequential mode"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 2)
    ax.axis('off')
    
    # Main bar
    bar_width = 10
    bar_height = 1.5
    bar_x = 1
    bar_y = 0.25
    
    # Priority 1 section (30% of bar)
    p1_width = bar_width * 0.3
    p1_rect = patches.Rectangle((bar_x, bar_y), p1_width, bar_height, 
                               facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax.add_patch(p1_rect)
    ax.text(bar_x + p1_width/2, bar_y + bar_height/2, 'PRIORITY 1\n(added:3)', 
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Priority 2 section (20% of bar)
    p2_x = bar_x + p1_width
    p2_width = bar_width * 0.2
    p2_rect = patches.Rectangle((p2_x, bar_y), p2_width, bar_height, 
                               facecolor='#2E86AB', edgecolor='black', linewidth=2)
    ax.add_patch(p2_rect)
    ax.text(p2_x + p2_width/2, bar_y + bar_height/2, 'PRIORITY 2\n(added:7)', 
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Normal section (50% of bar)
    normal_x = p2_x + p2_width
    normal_width = bar_width * 0.5
    normal_rect = patches.Rectangle((normal_x, bar_y), normal_width, bar_height, 
                                  facecolor='#7ED321', edgecolor='black', linewidth=2)
    ax.add_patch(normal_rect)
    ax.text(normal_x + normal_width/2, bar_y + bar_height/2, 'NORMAL\n(-added:7)', 
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Divider lines
    ax.plot([p2_x, p2_x], [bar_y, bar_y + bar_height], 'k-', linewidth=2)
    ax.plot([normal_x, normal_x], [bar_y, bar_y + bar_height], 'k-', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('sequential_priorities_diagram.svg', bbox_inches='tight', 
                facecolor='none', edgecolor='none')
    plt.close()
    print("Generated: diagrams/sequential_priorities_diagram.svg")


def create_cutoff_prioritization_diagram():
    """Create diagram showing cutoff and prioritization rules"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 2))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 2)
    ax.axis('off')
    
    # Main bar
    bar_width = 12
    bar_height = 1.5
    bar_x = 1
    bar_y = 0.25
    
    # Priority section (40% of bar)
    priority_width = bar_width * 0.4
    priority_rect = patches.Rectangle((bar_x, bar_y), priority_width, bar_height, 
                                    facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax.add_patch(priority_rect)
    ax.text(bar_x + priority_width/2, bar_y + bar_height/2, 'PRIORITY\n(added:4)\nFreq > 10000 →', 
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Normal section (60% of bar)
    normal_x = bar_x + priority_width
    normal_width = bar_width * 0.6
    normal_rect = patches.Rectangle((normal_x, bar_y), normal_width, bar_height, 
                                  facecolor='#7ED321', edgecolor='black', linewidth=2)
    ax.add_patch(normal_rect)
    ax.text(normal_x + normal_width/2, bar_y + bar_height/2, 'NORMAL\n(-added:4)\n← Freq < 1000', 
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Divider line
    ax.plot([normal_x, normal_x], [bar_y, bar_y + bar_height], 'k-', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('cutoff_prioritization_diagram.svg', bbox_inches='tight', 
                facecolor='none', edgecolor='none')
    plt.close()
    print("Generated: diagrams/cutoff_prioritization_diagram.svg")

def create_priority_limit_diagram():
    """Create diagram showing priority limit functionality"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 2))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 2)
    ax.axis('off')
    
    # Main bar
    bar_width = 12
    bar_height = 1.5
    bar_x = 1
    bar_y = 0.25
    
    # Priority section (limited to 50 cards)
    priority_width = bar_width * 0.3
    priority_rect = patches.Rectangle((bar_x, bar_y), priority_width, bar_height, 
                                    facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax.add_patch(priority_rect)
    ax.text(bar_x + priority_width/2, bar_y + bar_height/2, 'PRIORITY\n(added:4)\nLimit: 50 Excess →', 
            ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Normal section (includes overflow)
    normal_x = bar_x + priority_width
    normal_width = bar_width * 0.7
    normal_rect = patches.Rectangle((normal_x, bar_y), normal_width, bar_height, 
                                  facecolor='#7ED321', edgecolor='black', linewidth=2)
    ax.add_patch(normal_rect)
    ax.text(normal_x + normal_width/2, bar_y + bar_height/2, 'NORMAL\n(-added:4 + overflow)', 
            ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Divider line
    ax.plot([normal_x, normal_x], [bar_y, bar_y + bar_height], 'k-', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('priority_limit_diagram.svg', bbox_inches='tight', 
                facecolor='none', edgecolor='none')
    plt.close()
    print("Generated: diagrams/priority_limit_diagram.svg")

def create_occurrence_search_diagram():
    """Create diagram showing occurrence-based search with mixed normal queue"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 2))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 2)
    ax.axis('off')
    
    # Main bar
    bar_width = 12
    bar_height = 1.5
    bar_x = 1
    bar_y = 0.25
    
    # Priority section (40% of bar) - high occurrence cards
    priority_width = bar_width * 0.4
    priority_rect = patches.Rectangle((bar_x, bar_y), priority_width, bar_height, 
                                    facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax.add_patch(priority_rect)
    ax.text(bar_x + priority_width/2, bar_y + bar_height/2, 'PRIORITY\n(occurrences >= 50)', 
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Normal section (60% of bar)
    normal_x = bar_x + priority_width
    normal_width = bar_width * 0.6
    normal_rect = patches.Rectangle((normal_x, bar_y), normal_width, bar_height, 
                                  facecolor='#7ED321', edgecolor='black', linewidth=2)
    ax.add_patch(normal_rect)
    ax.text(normal_x + normal_width/2, bar_y + bar_height/2, 'NORMAL\n(occurrences < 50)', 
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Divider line
    ax.plot([normal_x, normal_x], [bar_y, bar_y + bar_height], 'k-', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('occurrence_search_diagram.svg', bbox_inches='tight', 
                facecolor='none', edgecolor='none')
    plt.close()
    print("Generated: diagrams/occurrence_search_diagram.svg")


def main():
    """Generate all diagrams"""
    print("Generating Priority Reorder Addon diagrams...")
    print("=" * 50)
    
    create_priority_diagram()
    create_sequential_priorities_diagram()
    create_cutoff_prioritization_diagram()
    create_priority_limit_diagram()
    create_occurrence_search_diagram()
    
    print("\nAll diagrams generated successfully!")
    print("Check the 'diagrams' folder for the SVG files.")

if __name__ == "__main__":
    main()
