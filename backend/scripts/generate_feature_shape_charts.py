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
# choose top 8 for individual plots, top 6 for pairplot, top 20 for heatmap
top8 = top_features[:8]
top6 = top_features[:6]
top20 = top_features[:20]

# Ensure features exist in featured dataset
top8 = [f for f in top8 if f in featured.columns]
top6 = [f for f in top6 if f in featured.columns]
top20 = [f for f in top20 if f in featured.columns]

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

print('Saved plots for features:', top8)
print('Pairplot saved and heatmap saved')
