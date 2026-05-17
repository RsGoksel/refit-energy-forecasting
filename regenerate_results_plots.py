"""
Regenerate metrics_comparison.png (4 models including Persistence) and
cross_house_comparison.png from the saved CSVs. Quick way to refresh
visuals without re-running the whole pipeline.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, "results")

# ---------- Single-house metrics (House 2) ----------
df = pd.read_csv(os.path.join(RESULTS, "metrics_table.csv"))
df = df.set_index("Model")
print("House 2 metrics:")
print(df.round(3))

colors = ['#888888', '#e74c3c', '#9b59b6', '#2ecc71']
fig, axes = plt.subplots(1, 4, figsize=(18, 5))
for i, metric in enumerate(['MSE', 'RMSE', 'MAE', 'R²']):
    bars = axes[i].bar(df.index, df[metric], color=colors[:len(df)], edgecolor='white')
    axes[i].set_title(metric, fontsize=14, fontweight='bold')
    axes[i].set_ylabel(metric)
    for bar in bars:
        height = bar.get_height()
        axes[i].text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.2f}', ha='center', va='bottom', fontsize=9)
    axes[i].tick_params(axis='x', labelrotation=20)
plt.suptitle('Performance Metrics, House 2 (Persistence baseline included)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
out = os.path.join(RESULTS, 'metrics_comparison.png')
plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0.3)
plt.close()
print(f"Saved: {out}")

# ---------- DM test summary plot ----------
dm = pd.read_csv(os.path.join(RESULTS, "dm_test_results.csv"))
print("\nDM tests:")
print(dm)

# Plot DM with significance shading
fig, ax = plt.subplots(figsize=(11, 5))
labels = [f"{r['model_1']}\nvs\n{r['model_2']}" for _, r in dm.iterrows()]
dm_vals = dm['DM'].values
pvals = dm['p_value'].values

bar_colors = ['#2ecc71' if p < 0.05 else '#bdc3c7' for p in pvals]
bars = ax.bar(range(len(dm)), dm_vals, color=bar_colors, edgecolor='white')
ax.axhline(0, color='black', linewidth=0.6)
ax.axhline(1.96, color='red', linewidth=0.6, linestyle='--', label='+-1.96 (5% sig.)')
ax.axhline(-1.96, color='red', linewidth=0.6, linestyle='--')
ax.set_xticks(range(len(dm)))
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylabel('DM Statistic')
ax.set_title('Diebold-Mariano Test, House 2\n(green: significant at 5%, grey: not significant)',
             fontweight='bold')
ax.legend(loc='upper right')
# annotate p-values
for i, (b, p) in enumerate(zip(bars, pvals)):
    h = b.get_height()
    ax.text(b.get_x() + b.get_width()/2, h + (0.3 if h >= 0 else -0.6),
            f'p={p:.3f}', ha='center', fontsize=9)
plt.tight_layout()
out = os.path.join(RESULTS, 'dm_test_plot.png')
plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0.3)
plt.close()
print(f"Saved: {out}")

# ---------- Cross-house already saved by cross_house_validation.py ----------
ch = pd.read_csv(os.path.join(RESULTS, "cross_house_metrics.csv"))
print("\nCross-house metrics:")
print(ch.round(3))
