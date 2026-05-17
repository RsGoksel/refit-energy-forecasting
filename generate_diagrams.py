"""
Generate custom diagrams for the Final Project Report.
Outputs:
 - results/pipeline_diagram.png      ML pipeline flowchart
 - results/lstm_architecture.png     LSTM model architecture
 - results/rolling_forecast.png      Rolling vs multi-step forecast illustration
 - results/iteration_timeline.png    Development iteration timeline
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

plt.style.use('seaborn-v0_8-whitegrid')

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, "results")

# ============================================================
# 1. PIPELINE DIAGRAM
# ============================================================
def make_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    stages = [
        # (x, y, w, h, label, color)
        (0.5, 7.0, 2.4, 1.0, "Raw REFIT Data\n(8-second sampling,\n5.7M rows)", "#4A90E2"),
        (3.5, 7.0, 2.4, 1.0, "Outlier Removal\n(0 < P < P99)", "#7BA7D9"),
        (6.5, 7.0, 2.4, 1.0, "Daily Resample\n(mean)", "#7BA7D9"),
        (9.5, 7.0, 2.4, 1.0, "7-day Rolling\nMean Smoothing", "#7BA7D9"),

        (0.5, 5.0, 5.4, 1.0, "Train/Test Split\n80% (490 days) / 20% (122 days)", "#F5A623"),

        (0.5, 2.5, 4.0, 1.5, "ARIMA\nGrid Search (p,d,q)\nRolling Forecast", "#E94B3C"),
        (5.0, 2.5, 4.0, 1.5, "LSTM\n3-layer (128/64/32)\nTeacher Forcing", "#9B59B6"),
        (9.5, 2.5, 4.0, 1.5, "FB-Prophet\nWeekly + Yearly\nMulti-step Forecast", "#2ECC71"),

        (3.5, 0.2, 7.0, 1.0, "Evaluation: MSE, RMSE, MAE, R2", "#34495E"),
    ]

    for x, y, w, h, label, color in stages:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                             linewidth=1.5, edgecolor='white', facecolor=color)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

    # Arrows: top row
    for x1 in [2.9, 5.9, 8.9]:
        ax.annotate('', xy=(x1+0.6, 7.5), xytext=(x1, 7.5),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#555'))

    # From top row to Train/Test
    ax.annotate('', xy=(3.2, 6.0), xytext=(3.2, 6.9),
                arrowprops=dict(arrowstyle='->', lw=2, color='#555'))

    # From Train/Test to three models
    ax.annotate('', xy=(2.5, 4.0), xytext=(2.5, 4.9),
                arrowprops=dict(arrowstyle='->', lw=2, color='#555'))
    ax.annotate('', xy=(7.0, 4.0), xytext=(4.0, 4.9),
                arrowprops=dict(arrowstyle='->', lw=2, color='#555'))
    ax.annotate('', xy=(11.5, 4.0), xytext=(5.0, 4.9),
                arrowprops=dict(arrowstyle='->', lw=2, color='#555'))

    # From models to evaluation
    for x1 in [2.5, 7.0, 11.5]:
        ax.annotate('', xy=(7.0, 1.2), xytext=(x1, 2.4),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#555'))

    ax.set_title("End-to-End ML Pipeline for REFIT Household Load Forecasting",
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    out = os.path.join(RESULTS, 'pipeline_diagram.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0.3, facecolor='white')
    plt.close()
    print(f"Saved: {out}")


# ============================================================
# 2. LSTM ARCHITECTURE DIAGRAM
# ============================================================
def make_lstm_diagram():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    layers = [
        (3, 10.5, 4, 0.8, "Input: 14-day window (sequence length=14, features=1)", "#34495E"),
        (3, 9.0,  4, 0.8, "LSTM Layer 1: 128 units, return_sequences=True", "#9B59B6"),
        (3, 8.0,  4, 0.6, "Dropout (0.2)", "#BDC3C7"),
        (3, 6.5,  4, 0.8, "LSTM Layer 2: 64 units, return_sequences=True", "#8E44AD"),
        (3, 5.5,  4, 0.6, "Dropout (0.2)", "#BDC3C7"),
        (3, 4.0,  4, 0.8, "LSTM Layer 3: 32 units", "#7D3C98"),
        (3, 3.0,  4, 0.6, "Dropout (0.2)", "#BDC3C7"),
        (3, 1.8,  4, 0.7, "Dense (16, ReLU)", "#3498DB"),
        (3, 0.8,  4, 0.7, "Dense (1) -> Predicted Power (W)", "#27AE60"),
    ]

    for x, y, w, h, label, color in layers:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                             linewidth=1.5, edgecolor='white', facecolor=color)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

    # Arrows connecting layers
    arrow_y = [
        (10.5, 9.8),
        (9.0, 8.6),
        (8.0, 7.3),
        (6.5, 6.1),
        (5.5, 4.8),
        (4.0, 3.6),
        (3.0, 2.5),
        (1.8, 1.5),
    ]
    for y_top, y_bottom in arrow_y:
        ax.annotate('', xy=(5, y_bottom), xytext=(5, y_top),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='#555'))

    # Side info
    ax.text(8, 10.0, "Total Trainable\nParams: 128,929",
            ha='left', va='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='#FFF9E6', edgecolor='#F5A623'))
    ax.text(8, 5.5, "Optimizer: Adam\nLoss: MSE\nEpochs: 100\nBatch: 16\nEarly Stop: 5",
            ha='left', va='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='#E8F5E9', edgecolor='#2ECC71'))

    ax.set_title("LSTM Architecture for Daily Household Load Forecasting",
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    out = os.path.join(RESULTS, 'lstm_architecture.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0.3, facecolor='white')
    plt.close()
    print(f"Saved: {out}")


# ============================================================
# 3. ROLLING vs MULTI-STEP FORECAST ILLUSTRATION
# ============================================================
def make_rolling_diagram():
    fig, axes = plt.subplots(2, 1, figsize=(12, 7))

    # Rolling (ARIMA, LSTM)
    ax = axes[0]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.set_title("Rolling One-step-ahead Forecast (ARIMA, LSTM)",
                 fontsize=12, fontweight='bold')
    ax.axis('off')

    # Training data
    train_rect = Rectangle((0.5, 1.5), 5, 1, facecolor='#4A90E2', edgecolor='white')
    ax.add_patch(train_rect)
    ax.text(3.0, 2.0, "Training Data", ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')

    # Test points
    for i, x_pos in enumerate([6.0, 7.2, 8.4, 9.6, 10.8, 12.0]):
        c = '#E94B3C' if i == 0 else '#F5A623'
        ax.add_patch(Rectangle((x_pos, 1.5), 1.0, 1, facecolor=c, edgecolor='white'))
        ax.text(x_pos + 0.5, 2.0, f"t+{i+1}", ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')

    # Annotation
    ax.annotate('Predict t+1\nUsing all prior history', xy=(6.5, 2.5), xytext=(6.5, 3.5),
                ha='center', fontsize=9, color='#E94B3C',
                arrowprops=dict(arrowstyle='->', color='#E94B3C'))
    ax.text(8.0, 0.8, "Then add t+1 actual to history and predict t+2, and so on",
            ha='center', fontsize=10, style='italic')

    # Multi-step (Prophet)
    ax = axes[1]
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.set_title("Multi-step Forecast (FB-Prophet)",
                 fontsize=12, fontweight='bold')
    ax.axis('off')

    train_rect = Rectangle((0.5, 1.5), 5, 1, facecolor='#4A90E2', edgecolor='white')
    ax.add_patch(train_rect)
    ax.text(3.0, 2.0, "Training Data", ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')

    # All test predictions at once
    for i, x_pos in enumerate([6.0, 7.2, 8.4, 9.6, 10.8, 12.0]):
        ax.add_patch(Rectangle((x_pos, 1.5), 1.0, 1, facecolor='#2ECC71', edgecolor='white'))
        ax.text(x_pos + 0.5, 2.0, f"t+{i+1}", ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')

    ax.annotate('Predict t+1..t+N\nin a single forecast', xy=(9.0, 2.5), xytext=(9.0, 3.5),
                ha='center', fontsize=9, color='#2ECC71',
                arrowprops=dict(arrowstyle='->', color='#2ECC71'))
    ax.text(8.0, 0.8, "No access to test actuals, so error accumulates over horizon",
            ha='center', fontsize=10, style='italic')

    plt.suptitle("Forecasting Protocols Compared",
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    out = os.path.join(RESULTS, 'rolling_forecast.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0.3, facecolor='white')
    plt.close()
    print(f"Saved: {out}")


# ============================================================
# 4. DEVELOPMENT ITERATION TIMELINE
# ============================================================
def make_iteration_timeline():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')

    iterations = [
        (1, 5.0, "Iteration 1", "Hourly resample,\n3-month subset",
         "ARIMA: -0.13   LSTM: 0.09   Prophet: -0.17", "#E94B3C"),
        (4.5, 5.0, "Iteration 2", "Daily resample,\nfull data, single-shot ARIMA",
         "ARIMA: 0.08   LSTM: -0.03   Prophet: 0.03", "#F5A623"),
        (8.5, 5.0, "Iteration 3 (Final)", "Daily + 7-day smoothing,\nrolling ARIMA",
         "ARIMA: 0.876   LSTM: 0.193   Prophet: 0.015", "#27AE60"),
    ]

    for x, y, title, desc, result, color in iterations:
        box = FancyBboxPatch((x - 1.5, y - 2.0), 3.0, 2.5, boxstyle="round,pad=0.1",
                             linewidth=2, edgecolor=color, facecolor='white')
        ax.add_patch(box)
        ax.text(x, y + 0.1, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color=color)
        ax.text(x, y - 0.5, desc, ha='center', va='center',
                fontsize=9, color='#333')
        ax.text(x, y - 1.5, "R2 results:", ha='center', va='center',
                fontsize=8, fontweight='bold', color='#333')
        ax.text(x, y - 1.8, result, ha='center', va='center',
                fontsize=8, color=color, fontweight='bold')

    # Arrows
    ax.annotate('', xy=(3.0, 5.0), xytext=(2.5, 5.0),
                arrowprops=dict(arrowstyle='->', lw=3, color='#666'))
    ax.annotate('', xy=(7.0, 5.0), xytext=(6.0, 5.0),
                arrowprops=dict(arrowstyle='->', lw=3, color='#666'))

    # Bottom takeaway
    ax.text(6.0, 1.5,
            "Key Insight: Daily aggregation removes intra-day noise,\n"
            "7-day smoothing preserves weekly cycles,\n"
            "rolling forecast leverages strong autocorrelation in residential data",
            ha='center', va='center', fontsize=10, style='italic',
            bbox=dict(boxstyle='round', facecolor='#FFF9E6', edgecolor='#F5A623'))

    ax.set_title("Development Iterations: From -0.13 to 0.876 R2",
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    out = os.path.join(RESULTS, 'iteration_timeline.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', pad_inches=0.3, facecolor='white')
    plt.close()
    print(f"Saved: {out}")


if __name__ == "__main__":
    make_pipeline_diagram()
    make_lstm_diagram()
    make_rolling_diagram()
    make_iteration_timeline()
    print("\nAll diagrams generated.")
