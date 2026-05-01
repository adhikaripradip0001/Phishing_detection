"""
Generate additional dataset visualization charts for dissertation presentation.
Creates charts for data sources, URL analysis, class balance, and quality metrics.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)

# Paths
data_path = Path('backend/data')
raw_path = data_path / 'raw'
external_path = data_path / 'external'
reports_path = Path('backend/reports/figures')
reports_path.mkdir(parents=True, exist_ok=True)

print("📊 Generating dataset visualization charts...\n")

# ============================================================================
# 1. DATA SOURCE DISTRIBUTION
# ============================================================================
print("1. Creating data source distribution chart...")

source_counts = {
    'OpenPhish': 0,
    'PhishTank': 0,
    'Tranco (Legitimate)': 0,
    'Custom Sources': 0
}

csv_files = list(external_path.glob('*.csv'))
for csv_file in csv_files:
    if 'openphish' in csv_file.name.lower():
        source_counts['OpenPhish'] += len(pd.read_csv(csv_file))
    elif 'phishtank' in csv_file.name.lower():
        source_counts['PhishTank'] += len(pd.read_csv(csv_file))
    elif 'tranco' in csv_file.name.lower():
        source_counts['Tranco (Legitimate)'] += len(pd.read_csv(csv_file))
    elif 'legitimate' in csv_file.name.lower():
        source_counts['Tranco (Legitimate)'] += len(pd.read_csv(csv_file))
    else:
        source_counts['Custom Sources'] += len(pd.read_csv(csv_file))

fig, ax = plt.subplots(figsize=(10, 6))
sources = list(source_counts.keys())
counts = list(source_counts.values())
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

bars = ax.barh(sources, counts, color=colors)
ax.set_xlabel('Number of Records', fontsize=12, fontweight='bold')
ax.set_title('Dataset Source Distribution', fontsize=14, fontweight='bold')

for i, (bar, count) in enumerate(zip(bars, counts)):
    ax.text(count + 100, i, f'{count:,}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(reports_path / 'data_source_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: data_source_distribution.png")

# ============================================================================
# 2. URL LENGTH DISTRIBUTION
# ============================================================================
print("2. Creating URL length distribution chart...")

# Load sample data
phishing_df = pd.read_csv(external_path / 'phishing_source_5000.csv')
legitimate_df = pd.read_csv(external_path / 'tranco_legitimate_sample.csv')

phishing_df['url_length'] = phishing_df['url'].astype(str).str.len()
legitimate_df['url_length'] = legitimate_df['url'].astype(str).str.len()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Phishing URLs
axes[0].hist(phishing_df['url_length'], bins=50, color='#FF6B6B', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('URL Length (characters)', fontsize=11, fontweight='bold')
axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
axes[0].set_title('Phishing URLs - Length Distribution', fontsize=12, fontweight='bold')
axes[0].axvline(phishing_df['url_length'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {phishing_df["url_length"].mean():.1f}')
axes[0].legend()

# Legitimate URLs
axes[1].hist(legitimate_df['url_length'], bins=50, color='#45B7D1', edgecolor='black', alpha=0.7)
axes[1].set_xlabel('URL Length (characters)', fontsize=11, fontweight='bold')
axes[1].set_ylabel('Frequency', fontsize=11, fontweight='bold')
axes[1].set_title('Legitimate URLs - Length Distribution', fontsize=12, fontweight='bold')
axes[1].axvline(legitimate_df['url_length'].mean(), color='blue', linestyle='--', linewidth=2, label=f'Mean: {legitimate_df["url_length"].mean():.1f}')
axes[1].legend()

plt.tight_layout()
plt.savefig(reports_path / 'url_length_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: url_length_distribution.png")

# ============================================================================
# 3. CLASS BALANCE COMPARISON
# ============================================================================
print("3. Creating class balance comparison chart...")

# Load cleaned dataset
cleaned_df = pd.read_csv(data_path / 'processed/cleaned_dataset.csv')

class_counts = cleaned_df['label'].value_counts()
class_labels = ['Phishing', 'Legitimate']
class_values = [class_counts.get(1, 0), class_counts.get(0, 0)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
colors_pie = ['#FF6B6B', '#45B7D1']
wedges, texts, autotexts = ax1.pie(
    class_values, 
    labels=class_labels, 
    autopct='%1.1f%%',
    colors=colors_pie,
    startangle=90,
    textprops={'fontsize': 11, 'fontweight': 'bold'}
)
ax1.set_title('Class Balance in Cleaned Dataset', fontsize=12, fontweight='bold')

# Bar chart
bars = ax2.bar(class_labels, class_values, color=colors_pie, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Number of Samples', fontsize=11, fontweight='bold')
ax2.set_title('Class Distribution (Absolute Count)', fontsize=12, fontweight='bold')
ax2.set_ylim(0, max(class_values) * 1.1)

for bar, val in zip(bars, class_values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(val):,}',
            ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig(reports_path / 'class_balance_cleaned.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: class_balance_cleaned.png")

# ============================================================================
# 4. DATA QUALITY METRICS
# ============================================================================
print("4. Creating data quality metrics chart...")

# Raw vs Cleaned comparison
raw_combined = pd.read_csv(data_path / 'raw/combined_raw.csv')

metrics = {
    'Total Records': [len(raw_combined), len(cleaned_df)],
    'Duplicate Records': [len(raw_combined) - len(raw_combined.drop_duplicates()), 
                          0],  # Already removed
    'Missing Values': [raw_combined.isnull().sum().sum(), 
                       cleaned_df.isnull().sum().sum()],
    'Valid Records': [len(raw_combined.drop_duplicates()), len(cleaned_df)]
}

x = np.arange(len(metrics))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))

raw_values = [metrics[key][0] for key in metrics.keys()]
cleaned_values = [metrics[key][1] for key in metrics.keys()]

bars1 = ax.bar(x - width/2, raw_values, width, label='Raw Data', color='#FFA07A', edgecolor='black')
bars2 = ax.bar(x + width/2, cleaned_values, width, label='Cleaned Data', color='#90EE90', edgecolor='black')

ax.set_xlabel('Metrics', fontsize=11, fontweight='bold')
ax.set_ylabel('Count', fontsize=11, fontweight='bold')
ax.set_title('Data Quality: Raw vs Cleaned Dataset', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(metrics.keys(), fontsize=10)
ax.legend(fontsize=11)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(reports_path / 'data_quality_metrics.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: data_quality_metrics.png")

# ============================================================================
# 5. FEATURE STATISTICS BY CLASS
# ============================================================================
print("5. Creating feature statistics by class chart...")

# Load featured dataset
featured_df = pd.read_csv(data_path / 'processed/featured_dataset.csv')

# Select a few key features for visualization
feature_cols = [col for col in featured_df.columns if col not in ['label', 'url']][:6]

# Calculate mean features by class
phishing_features = featured_df[featured_df['label'] == 1][feature_cols].mean()
legitimate_features = featured_df[featured_df['label'] == 0][feature_cols].mean()

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(phishing_features))
width = 0.35

bars1 = ax.bar(x - width/2, phishing_features.values, width, label='Phishing', 
              color='#FF6B6B', edgecolor='black')
bars2 = ax.bar(x + width/2, legitimate_features.values, width, label='Legitimate', 
              color='#45B7D1', edgecolor='black')

ax.set_xlabel('Features', fontsize=11, fontweight='bold')
ax.set_ylabel('Mean Value', fontsize=11, fontweight='bold')
ax.set_title('Feature Statistics: Phishing vs Legitimate URLs', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([col[:20] for col in phishing_features.index], rotation=45, ha='right', fontsize=9)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig(reports_path / 'feature_statistics_by_class.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: feature_statistics_by_class.png")

# ============================================================================
# 6. DATASET PIPELINE STAGES
# ============================================================================
print("6. Creating dataset pipeline stages chart...")

stages = ['Raw Data', 'After Cleaning', 'After Feature\nEngineering', 'After Feature\nSelection']
record_counts = [
    len(raw_combined),
    len(cleaned_df),
    len(featured_df) if 'featured_df' in dir() else len(cleaned_df),
    len(pd.read_csv(data_path / 'processed/selected_features_dataset.csv')) if (data_path / 'processed/selected_features_dataset.csv').exists() else len(cleaned_df)
]

fig, ax = plt.subplots(figsize=(12, 6))

colors_gradient = ['#FFB6C1', '#FFB6C1', '#87CEEB', '#87CEEB']
bars = ax.bar(stages, record_counts, color=colors_gradient, edgecolor='black', linewidth=2)

ax.set_ylabel('Number of Records', fontsize=11, fontweight='bold')
ax.set_title('Dataset Evolution Through Processing Pipeline', fontsize=12, fontweight='bold')
ax.set_ylim(0, max(record_counts) * 1.15)

for bar, val in zip(bars, record_counts):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
           f'{int(val):,}',
           ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig(reports_path / 'dataset_pipeline_stages.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: dataset_pipeline_stages.png")

print("\n✅ All dataset visualization charts generated successfully!")
print(f"📁 Charts saved to: {reports_path}")
