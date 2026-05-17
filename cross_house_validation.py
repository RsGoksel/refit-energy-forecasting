"""
Cross-house validation: run the same ARIMA / LSTM / FB-Prophet / Persistence
pipeline on multiple REFIT households and report whether the ranking holds.

This script imports the building blocks from energy_forecasting.py and runs
them in a loop. It writes:
  results/cross_house_metrics.csv      - all metrics for all houses + models
  results/cross_house_comparison.png   - per-house R2 bar chart
"""
import os
import sys
import importlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Force the imported pipeline to use the same RESULTS_DIR
import energy_forecasting as ef


HOUSES = [1, 2, 5]
RESULTS_DIR = ef.RESULTS_DIR


def run_for_house(house_id: int) -> dict:
    """Run all 4 models on one house and return a metrics dict."""
    print("\n" + "#" * 70)
    print(f"# HOUSE {house_id}")
    print("#" * 70)

    ef.HOUSE_ID = house_id  # patch module-level constant
    df, agg_col = ef.load_refit_data(house_id)
    series = ef.preprocess_data(df, agg_col)
    train, test = ef.train_test_split_ts(series)
    train_s, test_s = train['Power'], test['Power']

    out = {"house": house_id, "test_mean_W": float(test_s.mean()),
           "test_n_days": int(len(test_s))}

    # Persistence
    _, persistence_metrics = ef.run_persistence(train_s, test_s)
    out["persistence_rmse"] = persistence_metrics["RMSE"]
    out["persistence_r2"] = persistence_metrics["R²"]

    # ARIMA
    _, arima_metrics = ef.run_arima(train_s, test_s)
    out["arima_rmse"] = arima_metrics["RMSE"]
    out["arima_r2"] = arima_metrics["R²"]

    # LSTM
    _, lstm_metrics, _ = ef.run_lstm(train_s, test_s)
    out["lstm_rmse"] = lstm_metrics["RMSE"]
    out["lstm_r2"] = lstm_metrics["R²"]

    # Prophet
    _, prophet_metrics = ef.run_prophet(train_s, test_s)
    out["prophet_rmse"] = prophet_metrics["RMSE"]
    out["prophet_r2"] = prophet_metrics["R²"]

    return out


def main():
    rows = []
    for hid in HOUSES:
        try:
            rows.append(run_for_house(hid))
        except FileNotFoundError as exc:
            print(f"!! Skipping House {hid}: {exc}")
            continue

    df = pd.DataFrame(rows).set_index("house")
    out_csv = os.path.join(RESULTS_DIR, "cross_house_metrics.csv")
    df.to_csv(out_csv)
    print(f"\nSaved metrics to: {out_csv}")
    print(df.round(3).to_string())

    # Bar chart of R2 across houses
    fig, ax = plt.subplots(figsize=(12, 5))
    models = ["Persistence", "ARIMA", "LSTM", "Prophet"]
    cols = ["persistence_r2", "arima_r2", "lstm_r2", "prophet_r2"]
    palette = ["#888888", "#E94B3C", "#9B59B6", "#2ECC71"]
    x = np.arange(len(df))
    w = 0.2
    for i, (m, c, color) in enumerate(zip(models, cols, palette)):
        ax.bar(x + (i - 1.5) * w, df[c].values, width=w, label=m,
               color=color, edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels([f"House {h}" for h in df.index])
    ax.set_ylabel("R2 on test set")
    ax.set_title("Cross-House Validation: R2 by Model and Household", fontweight='bold')
    ax.axhline(0, color='black', linewidth=0.6)
    ax.legend(loc='lower right')
    plt.tight_layout()
    out_png = os.path.join(RESULTS_DIR, "cross_house_comparison.png")
    plt.savefig(out_png, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved figure to: {out_png}")


if __name__ == "__main__":
    main()
