"""
Regenerate just the data_analysis.png with the corrected hourly plot
(hourly pattern computed on raw 8-second data, not daily-resampled).
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
RESULTS_DIR = os.path.join(BASE, "results")
HOUSE_ID = 2
RESAMPLE_INTERVAL = "1D"
SMOOTH_WINDOW = 7

print("Loading raw House_2.csv ...")
fpath = os.path.join(DATA_DIR, "House_2.csv")
raw_df = pd.read_csv(fpath, parse_dates=['Time'], index_col='Time')
if 'Unix' in raw_df.columns:
    raw_df = raw_df.drop(columns=['Unix'])
agg_col = 'Aggregate'
print(f"Raw shape: {raw_df.shape}")

# Preprocess to daily
series = raw_df[[agg_col]].copy()
series.columns = ['Power']
series = series[series['Power'] >= 0]
upper = series['Power'].quantile(0.99)
series = series[series['Power'] <= upper]
series_daily = series.resample(RESAMPLE_INTERVAL).mean().ffill().bfill()
series_daily['Power'] = series_daily['Power'].rolling(window=SMOOTH_WINDOW, center=True).mean()
series_daily = series_daily.dropna()
print(f"Daily smoothed shape: {series_daily.shape}")

# Hourly pattern from raw data
raw_hourly = series.resample('1h').mean()
hourly = raw_hourly.groupby(raw_hourly.index.hour)['Power'].mean()
print(f"Hourly pattern range: hour 0 = {hourly.iloc[0]:.1f} W, max hour {hourly.idxmax()} = {hourly.max():.1f} W")

# Day of week pattern (on daily)
daily_dow = series_daily.copy()
daily_dow['dow'] = daily_dow.index.dayofweek
dow = daily_dow.groupby('dow')['Power'].mean()

# Make figure
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# 1. Daily time series
axes[0, 0].plot(series_daily.index, series_daily['Power'], linewidth=0.8, color='steelblue')
axes[0, 0].set_title(f'Household Energy Consumption, Daily Average (House {HOUSE_ID})', fontsize=12)
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Power (W)')

# 2. Hourly pattern from raw
axes[0, 1].bar(hourly.index, hourly.values, color='coral', edgecolor='white')
axes[0, 1].set_title('Average Power Consumption by Hour of Day (Raw Data)', fontsize=12)
axes[0, 1].set_xlabel('Hour of Day')
axes[0, 1].set_ylabel('Average Power (W)')
axes[0, 1].set_xticks(range(0, 24, 2))

# 3. Day of week
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
axes[1, 0].bar(range(7), dow.values, color='seagreen', edgecolor='white', tick_label=days)
axes[1, 0].set_title('Average Power Consumption by Day of Week', fontsize=12)
axes[1, 0].set_ylabel('Average Power (W)')

# 4. Distribution
axes[1, 1].hist(series_daily['Power'], bins=50, color='mediumpurple', edgecolor='white')
axes[1, 1].set_title('Daily Power Consumption Distribution', fontsize=12)
axes[1, 1].set_xlabel('Power (W)')
axes[1, 1].set_ylabel('Frequency')

plt.suptitle(f'REFIT Dataset, House {HOUSE_ID} Energy Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
out = os.path.join(RESULTS_DIR, 'data_analysis.png')
plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0.3)
plt.close()
print(f"Saved: {out}")
