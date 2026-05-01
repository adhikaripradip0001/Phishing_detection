"""
Generate feature shape and distribution charts for presentation.
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

# Determine top features by importance
if 'random_forest_importance' in fr.columns:
    fr['importance'] = fr['random_forest_importance']
else:
    fr['importance'] = fr['abs_correlation']

top_features = fr.sort_values('importance', ascending=False)['feature'].tolist()

# Use the strongest features for the detailed plots
top8 = [f for f in top_features[:8] if f in featured.columns]
top6 = [f for f in top_features[:6] if f in featured.columns]
top20 = [f for f in top_features[:20] if f in featured.columns]

# 1. Histograms + KDE for top8
for feat in top8:
    plt.figure(figsize=(8,5))
    sns.histplot(data=featured, x=feat, hue='label', kde=True, element='step', stat='density', common_norm=False, palette=['#45B7D1','#FF6B6B'])
    plt.title(f'Distribution of {feat} (by class)')
    plt.tight_layout()
    plt.savefig(reports_path / f'{feat}_distribution_by_class.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. Boxplots for top8
for feat in top8:
    plt.figure(figsize=(6,5))
    sns.boxplot(data=featured, x='label', y=feat, palette=['#45B7D1','#FF6B6B'])
    plt.xticks([0,1], ['Legitimate','Phishing'])
    plt.title(f'Boxplot of {feat} by class')
    plt.tight_layout()
    plt.savefig(reports_path / f'{feat}_boxplot_by_class.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. Violin plots for top8
for feat in top8:
    plt.figure(figsize=(6,5))
    sns.violinplot(data=featured, x='label', y=feat, palette=['#45B7D1','#FF6B6B'], cut=0)
    plt.xticks([0,1], ['Legitimate','Phishing'])
    plt.title(f'Violin plot of {feat} by class')
    plt.tight_layout()
    plt.savefig(reports_path / f'{feat}_violin_by_class.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. Cumulative distribution (ECDF) for top6
for feat in top6:
    plt.figure(figsize=(8,5))
    sns.ecdfplot(data=featured, x=feat, hue='label', palette=['#45B7D1','#FF6B6B'])
    plt.title(f'ECDF of {feat} by class')
    plt.tight_layout()
    plt.savefig(reports_path / f'{feat}_ecdf_by_class.png', dpi=300, bbox_inches='tight')
    plt.close()

# 5. Pairplot for top6 (sample if large)
sample_df = featured[top6 + ['label']].sample(n=min(2000, len(featured)), random_state=42)
pp = sns.pairplot(sample_df, hue='label', palette={0:'#45B7D1',1:'#FF6B6B'}, diag_kind='kde', corner=True)
pp.fig.suptitle('Pairplot of Top 6 Features (sampled)', y=1.02)
pp.savefig(reports_path / 'features_pairplot_top6.png', dpi=200, bbox_inches='tight')
plt.close()

# 6. Correlation heatmap for top20
corr_df = featured[top20].corr()
plt.figure(figsize=(12,10))
sns.heatmap(corr_df, annot=False, cmap='coolwarm', center=0)
plt.title('Feature Correlation Heatmap (Top 20)')
plt.tight_layout()
plt.savefig(reports_path / 'features_correlation_heatmap_top20.png', dpi=300, bbox_inches='tight')
plt.close()


# 7. Project-aligned feature shape overview using only features that vary in the processed dataset
candidate_shape_features = [
    'url_length',
    'domain_length',
    'path_length',
    'num_digits',
    'num_special_chars',
    'suspicious_keyword_count',
    'has_login_keyword',
    'brand_similarity_score',
]

shape_features = []
for feat in candidate_shape_features:
    if feat in featured.columns and featured[feat].nunique(dropna=True) > 1:
        shape_features.append(feat)

# Keep the figure concise and presentation-friendly
shape_features = shape_features[:6]

if shape_features:
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()
    for ax, feat in zip(axes, shape_features):
        for lab, color, label in [(0, '#45B7D1', 'Legitimate'), (1, '#FF6B6B', 'Phishing')]:
            subset = featured[featured['label'] == lab][feat].dropna()
            if subset.nunique(dropna=True) > 1:
                sns.kdeplot(subset, ax=ax, fill=True, alpha=0.30, linewidth=2, color=color, label=label, warn_singular=False)
            else:
                ax.axvline(subset.iloc[0] if len(subset) else 0, color=color, linewidth=2, label=label)
        ax.set_title(feat.replace('_', ' ').title(), fontweight='bold')
        ax.set_xlabel(feat.replace('_', ' ').title())
        ax.set_ylabel('Density')
        ax.legend()
    for ax in axes[len(shape_features):]:
        ax.axis('off')
    fig.suptitle('Feature Shape Overview Across Variable Lexical and Brand Features', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_path = reports_path / 'feature_shape_overview_project_aligned.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print('Saved project-aligned shape overview:', out_path)
    print('Shape features used:', shape_features)

print('Saved plots for features:', top8)
print('Pairplot saved and heatmap saved')
