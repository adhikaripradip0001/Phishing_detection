"""
Generate feature distribution overview (histograms) for presentation.
This is a simplified script focused on the distribution overview figure.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style('whitegrid')
reports_path = Path('backend/reports/figures')
reports_path.mkdir(parents=True, exist_ok=True)

# Load data
featured = pd.read_csv('backend/data/processed/featured_dataset.csv')
fr = pd.read_csv('backend/data/processed/feature_rankings.csv')

# Features that have variance in the dataset
shape_features = [
    'url_length',
    'domain_length',
    'path_length',
    'num_digits',
    'num_special_chars',
    'suspicious_keyword_count',
]

# Filter to only features that exist and have variance
final_features = []
for feat in shape_features:
    if feat in featured.columns and featured[feat].std() > 0:
        final_features.append(feat)

# Create distribution overview (histograms)
if final_features:
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()
    
    for ax, feat in zip(axes, final_features):
        # Create histogram with separate bins for each class
        legitimate = featured[featured['label'] == 0][feat].dropna()
        phishing = featured[featured['label'] == 1][feat].dropna()
        
        ax.hist(legitimate, bins=30, alpha=0.6, color='#45B7D1', label='Legitimate', 
                density=True, edgecolor='black', linewidth=0.5)
        ax.hist(phishing, bins=30, alpha=0.6, color='#FF6B6B', label='Phishing', 
                density=True, edgecolor='black', linewidth=0.5)
        
        ax.set_title(feat.replace('_', ' ').title(), fontweight='bold', fontsize=11)
        ax.set_xlabel(feat.replace('_', ' ').title(), fontsize=10)
        ax.set_ylabel('Density', fontsize=10)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
    
    # Hide unused subplots
    for ax in axes[len(final_features):]:
        ax.axis('off')
    
    fig.suptitle('Feature Distribution Overview Across Variable Lexical and Brand Features', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_path = reports_path / 'feature_distribution_overview_project_aligned.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print('Saved distribution overview:', out_path)
    print('Features used:', final_features)
else:
    print('No features with variance found!')
