"""
REFIT Household Energy Consumption Forecasting
================================================
Compares ARIMA, LSTM, and FB-Prophet models for predicting
household energy consumption using the REFIT Smart Home dataset.

Course: EBT 629E - Artificial Intelligence (ITU)
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')

# Reproducibility: seed all randomness sources we use
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
import random as _random
_random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# ============================================================
# 1. CONFIGURATION
# ============================================================
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Which house to analyze (1-20)
HOUSE_ID = 2
# Resample interval (raw data is 8sec, we resample for practical modeling)
RESAMPLE_INTERVAL = "1D"
# Train/test split ratio
TRAIN_RATIO = 0.8
# LSTM parameters
LSTM_EPOCHS = 100
LSTM_BATCH_SIZE = 16
LSTM_LOOKBACK = 14  # days of history to use for prediction
# Limit data to N months for faster processing (None = use all)
LIMIT_MONTHS = None  # Use all ~2 years
# Rolling mean window for smoothing noisy consumption data
SMOOTH_WINDOW = 7  # 7-day rolling mean for daily data


# ============================================================
# 2. DATA LOADING
# ============================================================
def load_refit_data(house_id: int) -> pd.DataFrame:
    """Load REFIT data for a specific house."""
    # Try different file naming conventions
    patterns = [
        f"House_{house_id}.csv",
        f"CLEAN_House{house_id}.csv",
        f"House{house_id}.csv",
        f"house_{house_id}.csv",
    ]

    filepath = None
    for pattern in patterns:
        candidate = os.path.join(DATA_DIR, pattern)
        if os.path.exists(candidate):
            filepath = candidate
            break

    if filepath is None:
        # Try to find any CSV file matching house id
        for f in os.listdir(DATA_DIR):
            if f.endswith('.csv') and str(house_id) in f:
                filepath = os.path.join(DATA_DIR, f)
                break

    if filepath is None:
        raise FileNotFoundError(
            f"No data file found for House {house_id} in {DATA_DIR}. "
            f"Please download the REFIT dataset and place CSV files in {DATA_DIR}/"
        )

    print(f"Loading data from: {filepath}")

    # Read CSV - use 'Time' column directly
    df = pd.read_csv(filepath, parse_dates=['Time'], index_col='Time')

    # Drop Unix timestamp column if present
    if 'Unix' in df.columns:
        df = df.drop(columns=['Unix'])

    # Rename appliance columns for readability (House 2 specific)
    appliance_names = {
        2: {
            'Appliance1': 'Fridge-Freezer', 'Appliance2': 'Washing Machine',
            'Appliance3': 'Dishwasher', 'Appliance4': 'Television',
            'Appliance5': 'Microwave', 'Appliance6': 'Toaster',
            'Appliance7': 'Hi-Fi', 'Appliance8': 'Kettle',
            'Appliance9': 'Oven Extractor Fan'
        }
    }
    if house_id in appliance_names:
        df = df.rename(columns=appliance_names[house_id])

    agg_col = 'Aggregate'

    # Limit to N months if configured
    if LIMIT_MONTHS is not None:
        end_date = df.index.min() + pd.DateOffset(months=LIMIT_MONTHS)
        df = df[df.index <= end_date]
        print(f"Limited to first {LIMIT_MONTHS} months")

    print(f"Dataset shape: {df.shape}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print(f"Columns: {list(df.columns)}")

    return df, agg_col


# ============================================================
# 3. DATA PREPROCESSING
# ============================================================
def preprocess_data(df: pd.DataFrame, agg_col: str) -> pd.DataFrame:
    """Resample, clean, and prepare data for modeling."""
    print(f"\n--- Preprocessing ---")
    print(f"Original shape: {df.shape}")

    # Use aggregate power consumption
    series = df[[agg_col]].copy()
    series.columns = ['Power']

    # Remove negative values and extreme outliers
    series = series[series['Power'] >= 0]
    upper_limit = series['Power'].quantile(0.99)
    series = series[series['Power'] <= upper_limit]

    # Resample to hourly
    series = series.resample(RESAMPLE_INTERVAL).mean()

    # Fill missing values with forward fill then backward fill
    series = series.ffill().bfill()

    # Apply rolling mean smoothing to reduce noise
    if SMOOTH_WINDOW and SMOOTH_WINDOW > 1:
        series['Power'] = series['Power'].rolling(window=SMOOTH_WINDOW, center=True).mean()
        print(f"Applied {SMOOTH_WINDOW}-period rolling mean smoothing")

    # Drop any remaining NaN
    series = series.dropna()

    print(f"After preprocessing: {series.shape}")
    print(f"Date range: {series.index.min()} to {series.index.max()}")
    print(f"\nBasic Statistics:")
    print(series.describe())

    return series


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add time-based features for analysis."""
    df = df.copy()
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['month'] = df.index.month
    df['is_weekend'] = (df.index.dayofweek >= 5).astype(int)
    return df


def train_test_split_ts(series: pd.DataFrame):
    """Split time series into train and test sets."""
    n = len(series)
    train_size = int(n * TRAIN_RATIO)
    train = series.iloc[:train_size]
    test = series.iloc[train_size:]
    print(f"\nTrain size: {len(train)} | Test size: {len(test)}")
    return train, test


# ============================================================
# 4. EVALUATION METRICS
# ============================================================
def evaluate_model(y_true, y_pred, model_name: str) -> dict:
    """Calculate MSE, RMSE, MAE, R² metrics."""
    y_true = np.array(y_true).flatten()
    y_pred = np.array(y_pred).flatten()

    # Align lengths
    min_len = min(len(y_true), len(y_pred))
    y_true = y_true[:min_len]
    y_pred = y_pred[:min_len]

    mse = mean_squared_error(y_true, y_pred)
    rmse = sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    metrics = {'Model': model_name, 'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'R²': r2}
    print(f"\n{model_name} Performance:")
    print(f"  MSE:  {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE:  {mae:.4f}")
    print(f"  R²:   {r2:.4f}")
    return metrics


# ============================================================
# 4b. PERSISTENCE BASELINE (naive forecast: y_hat[t] = y_actual[t-1])
# ============================================================
def run_persistence(train: pd.Series, test: pd.Series) -> tuple:
    """Naive baseline: predict today equals yesterday's actual.

    This is the canonical sanity-check baseline for time-series forecasting.
    If a more complex model cannot beat this, it has learned nothing useful.
    """
    print("\n" + "=" * 60)
    print("PERSISTENCE BASELINE (predict y[t] = y[t-1])")
    print("=" * 60)

    # First test prediction uses last training value, then each test
    # prediction uses the previous actual test value.
    history_last = train.values[-1]
    predictions = np.empty(len(test))
    predictions[0] = history_last
    predictions[1:] = test.values[:-1]

    metrics = evaluate_model(test.values, predictions, "Persistence")
    return predictions, metrics


# ============================================================
# 4c. DIEBOLD-MARIANO TEST (forecast accuracy significance)
# ============================================================
def diebold_mariano_test(actual, pred1, pred2, h: int = 1) -> dict:
    """Diebold-Mariano test for equal predictive accuracy.

    H0: forecasts from model 1 and model 2 have equal squared-error loss.
    Negative DM statistic favours model 1 (lower errors); positive favours model 2.

    Returns the test statistic and a two-sided p-value.
    Implementation follows Diebold and Mariano (1995) with the
    Harvey, Leybourne, Newbold (1997) small-sample correction.
    """
    from scipy.stats import t as t_dist

    actual = np.asarray(actual, dtype=float).flatten()
    pred1 = np.asarray(pred1, dtype=float).flatten()
    pred2 = np.asarray(pred2, dtype=float).flatten()

    n = min(len(actual), len(pred1), len(pred2))
    actual, pred1, pred2 = actual[:n], pred1[:n], pred2[:n]

    e1 = actual - pred1
    e2 = actual - pred2
    d = e1 ** 2 - e2 ** 2  # squared-error loss differential

    mean_d = float(np.mean(d))
    # Newey-West style HAC variance with lag = h - 1 (h=1 means use sample variance)
    gamma0 = float(np.var(d, ddof=0))
    var_d = gamma0
    for k in range(1, h):
        gamma_k = float(np.mean((d[k:] - mean_d) * (d[:-k] - mean_d)))
        var_d += 2 * (1 - k / h) * gamma_k

    if var_d <= 0 or n < 3:
        return {"DM": float("nan"), "p_value": float("nan"), "n": n}

    dm_stat = mean_d / np.sqrt(var_d / n)
    # Harvey, Leybourne, Newbold (1997) small-sample correction
    correction = np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    dm_stat_hln = dm_stat * correction

    # Two-sided p-value using Student t with n-1 dof
    p_value = 2 * (1 - t_dist.cdf(abs(dm_stat_hln), df=n - 1))

    return {"DM": float(dm_stat_hln), "p_value": float(p_value), "n": n}


# ============================================================
# 5. ARIMA MODEL
# ============================================================
def run_arima(train: pd.Series, test: pd.Series) -> tuple:
    """Train and evaluate ARIMA model."""
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller

    print("\n" + "=" * 60)
    print("ARIMA MODEL")
    print("=" * 60)

    # ADF test for stationarity
    adf_result = adfuller(train.values)
    print(f"ADF Statistic: {adf_result[0]:.4f}")
    print(f"p-value: {adf_result[1]:.6f}")

    d = 0 if adf_result[1] < 0.05 else 1
    print(f"Differencing order (d): {d}")

    # Grid search for best (p, d, q)
    best_aic = float('inf')
    best_order = (1, d, 1)

    print("Searching for optimal ARIMA parameters...")
    for p in range(0, 3):
        for q in range(0, 3):
            try:
                model = ARIMA(train.values, order=(p, d, q))
                fitted = model.fit()
                if fitted.aic < best_aic:
                    best_aic = fitted.aic
                    best_order = (p, d, q)
            except Exception:
                continue

    print(f"Best ARIMA order: {best_order} (AIC: {best_aic:.2f})")

    # Rolling forecast for better accuracy
    print("Running rolling forecast...")
    history = list(train.values)
    predictions = []
    for i in range(len(test)):
        model = ARIMA(history, order=best_order)
        fitted = model.fit()
        yhat = fitted.forecast(steps=1)[0]
        predictions.append(yhat)
        history.append(test.values[i])
        if (i + 1) % 30 == 0:
            print(f"  Step {i+1}/{len(test)}")

    predictions = np.array(predictions)
    metrics = evaluate_model(test.values, predictions, "ARIMA")
    return predictions, metrics


# ============================================================
# 6. LSTM MODEL
# ============================================================
def create_lstm_sequences(data, lookback):
    """Create sequences for LSTM input."""
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i - lookback:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)


def run_lstm(train: pd.Series, test: pd.Series) -> tuple:
    """Train and evaluate LSTM model."""
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping

    # Seed TensorFlow for reproducibility
    tf.random.set_seed(RANDOM_SEED)
    tf.keras.utils.set_random_seed(RANDOM_SEED)

    print("\n" + "=" * 60)
    print("LSTM MODEL")
    print("=" * 60)

    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_scaled = scaler.fit_transform(train.values.reshape(-1, 1))
    test_scaled = scaler.transform(test.values.reshape(-1, 1))

    # Combine for sequence creation
    full_scaled = np.concatenate([train_scaled, test_scaled])

    # Create sequences
    X_train, y_train = create_lstm_sequences(train_scaled, LSTM_LOOKBACK)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

    # For test, we need lookback from end of training data
    test_input = full_scaled[len(train_scaled) - LSTM_LOOKBACK:]
    X_test, y_test = create_lstm_sequences(test_input, LSTM_LOOKBACK)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")

    # Build model
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(LSTM_LOOKBACK, 1)),
        Dropout(0.2),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    model.summary()

    # Train
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    history = model.fit(
        X_train, y_train,
        epochs=LSTM_EPOCHS,
        batch_size=LSTM_BATCH_SIZE,
        validation_split=0.1,
        callbacks=[early_stop],
        verbose=1
    )

    # Predict
    predictions_scaled = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions_scaled).flatten()

    # Align test values
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

    metrics = evaluate_model(y_test_actual, predictions, "LSTM")

    # Save training history plot
    plt.figure(figsize=(10, 4))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('LSTM Training History')
    plt.xlabel('Epoch')
    plt.ylabel('Loss (MSE)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'lstm_training_history.png'), dpi=150)
    plt.close()

    return predictions, metrics, y_test_actual


# ============================================================
# 7. FB-PROPHET MODEL
# ============================================================
def run_prophet(train: pd.Series, test: pd.Series) -> tuple:
    """Train and evaluate FB-Prophet model."""
    from prophet import Prophet

    print("\n" + "=" * 60)
    print("FB-PROPHET MODEL")
    print("=" * 60)

    # Prophet requires 'ds' and 'y' columns
    train_df = pd.DataFrame({
        'ds': train.index,
        'y': train.values
    })

    # Build and fit model
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05,
        seasonality_mode='multiplicative',
    )
    model.fit(train_df)

    # Create future dataframe
    future = model.make_future_dataframe(periods=len(test), freq=RESAMPLE_INTERVAL)
    forecast = model.predict(future)

    # Extract predictions for test period
    predictions = forecast['yhat'].iloc[-len(test):].values

    metrics = evaluate_model(test.values, predictions, "FB-Prophet")

    # Save Prophet components plot
    fig = model.plot_components(forecast)
    fig.savefig(os.path.join(RESULTS_DIR, 'prophet_components.png'), dpi=150)
    plt.close(fig)

    return predictions, metrics


# ============================================================
# 8. VISUALIZATION
# ============================================================
def plot_data_analysis(series: pd.DataFrame, raw_df: pd.DataFrame, agg_col: str):
    """Create exploratory data analysis plots.

    The processed 'series' is daily-resampled and used for the time series, day-of-week,
    monthly, and distribution plots. The 'raw_df' (8-second sampling) is used for the
    hourly pattern so that the hourly bar chart is meaningful (otherwise daily resampling
    collapses every timestamp to hour 00:00 and the chart becomes trivial).
    """
    df_feat = create_features(series)

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # 1. Time series plot (daily aggregated)
    axes[0, 0].plot(series.index, series['Power'], linewidth=0.8, color='steelblue')
    axes[0, 0].set_title(f'Household Energy Consumption, Daily Average (House {HOUSE_ID})',
                         fontsize=12)
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Power (W)')

    # 2. Hourly pattern, computed on the RAW 8-second data (then averaged over hours)
    raw_power = raw_df[[agg_col]].copy()
    raw_power.columns = ['Power']
    raw_power = raw_power[raw_power['Power'] >= 0]
    raw_power = raw_power[raw_power['Power'] <= raw_power['Power'].quantile(0.99)]
    raw_hourly = raw_power.resample('1h').mean()
    hourly = raw_hourly.groupby(raw_hourly.index.hour)['Power'].mean()
    axes[0, 1].bar(hourly.index, hourly.values, color='coral', edgecolor='white')
    axes[0, 1].set_title('Average Power Consumption by Hour of Day (Raw Data)', fontsize=12)
    axes[0, 1].set_xlabel('Hour of Day')
    axes[0, 1].set_ylabel('Average Power (W)')
    axes[0, 1].set_xticks(range(0, 24, 2))

    # 3. Day of week pattern (on daily aggregates, still valid)
    daily = df_feat.groupby('dayofweek')['Power'].mean()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    axes[1, 0].bar(range(7), daily.values, color='seagreen', edgecolor='white',
                   tick_label=days)
    axes[1, 0].set_title('Average Power Consumption by Day of Week', fontsize=12)
    axes[1, 0].set_ylabel('Average Power (W)')

    # 4. Distribution
    axes[1, 1].hist(series['Power'], bins=50, color='mediumpurple', edgecolor='white')
    axes[1, 1].set_title('Daily Power Consumption Distribution', fontsize=12)
    axes[1, 1].set_xlabel('Power (W)')
    axes[1, 1].set_ylabel('Frequency')

    plt.suptitle(f'REFIT Dataset, House {HOUSE_ID} Energy Analysis',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'data_analysis.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Data analysis plot saved.")


def plot_correlation_heatmap(df: pd.DataFrame):
    """Plot correlation heatmap of appliance data."""
    # Select numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 2:
        corr = df[numeric_cols].corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr, annot=True, cmap='RdYlBu_r', center=0,
                    fmt='.2f', square=True, linewidths=0.5)
        plt.title(f'Correlation Heatmap - House {HOUSE_ID} Appliances', fontsize=14)
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, 'correlation_heatmap.png'), dpi=150)
        plt.close()
        print("Correlation heatmap saved.")


def plot_model_comparison(test_index, test_values, arima_pred, lstm_pred, lstm_actual,
                          prophet_pred):
    """Plot actual vs predicted for all models."""
    fig, axes = plt.subplots(3, 1, figsize=(16, 14))

    # ARIMA
    axes[0].plot(test_index, test_values, label='Actual', color='steelblue', linewidth=1)
    axes[0].plot(test_index, arima_pred, label='ARIMA Predicted',
                 color='orangered', linewidth=1, linestyle='--')
    axes[0].set_title('ARIMA Model: Actual vs Predicted', fontsize=12)
    axes[0].set_ylabel('Power (W)')
    axes[0].legend()

    # LSTM (uses aligned test values)
    lstm_index = test_index[:len(lstm_pred)]
    axes[1].plot(lstm_index, lstm_actual[:len(lstm_pred)], label='Actual',
                 color='steelblue', linewidth=1)
    axes[1].plot(lstm_index, lstm_pred, label='LSTM Predicted',
                 color='orangered', linewidth=1, linestyle='--')
    axes[1].set_title('LSTM Model: Actual vs Predicted', fontsize=12)
    axes[1].set_ylabel('Power (W)')
    axes[1].legend()

    # Prophet
    axes[2].plot(test_index, test_values, label='Actual', color='steelblue', linewidth=1)
    axes[2].plot(test_index, prophet_pred, label='FB-Prophet Predicted',
                 color='orangered', linewidth=1, linestyle='--')
    axes[2].set_title('FB-Prophet Model: Actual vs Predicted', fontsize=12)
    axes[2].set_xlabel('Date')
    axes[2].set_ylabel('Power (W)')
    axes[2].legend()

    plt.suptitle(f'Model Comparison - House {HOUSE_ID} Energy Forecasting',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'model_comparison.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Model comparison plot saved.")


def plot_metrics_comparison(all_metrics: list):
    """Bar chart comparing model performance metrics."""
    metrics_df = pd.DataFrame(all_metrics)
    metrics_df = metrics_df.set_index('Model')

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    colors = ['#888888', '#e74c3c', '#9b59b6', '#2ecc71']

    for i, metric in enumerate(['MSE', 'RMSE', 'MAE', 'R²']):
        bars = axes[i].bar(metrics_df.index, metrics_df[metric], color=colors, edgecolor='white')
        axes[i].set_title(metric, fontsize=14, fontweight='bold')
        axes[i].set_ylabel(metric)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width() / 2., height,
                         f'{height:.2f}', ha='center', va='bottom', fontsize=10)

    plt.suptitle('Performance Metrics Comparison', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'metrics_comparison.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Metrics comparison plot saved.")

    # Save metrics table
    metrics_df.to_csv(os.path.join(RESULTS_DIR, 'metrics_table.csv'))
    print("\nFinal Metrics Table:")
    print(metrics_df.to_string())


# ============================================================
# 9. MAIN PIPELINE
# ============================================================
def main():
    print("=" * 60)
    print("REFIT Household Energy Consumption Forecasting")
    print("ARIMA vs LSTM vs FB-Prophet Comparison")
    print("=" * 60)

    # Step 1: Load data
    print("\n[1/8] Loading data...")
    df, agg_col = load_refit_data(HOUSE_ID)

    # Step 2: Correlation analysis on raw data
    print("\n[2/8] Correlation analysis...")
    plot_correlation_heatmap(df)

    # Step 3: Preprocess
    print("\n[3/8] Preprocessing...")
    series = preprocess_data(df, agg_col)

    # Step 4: EDA
    print("\n[4/8] Exploratory Data Analysis...")
    plot_data_analysis(series, df, agg_col)

    # Step 5: Train/Test split
    print("\n[5/8] Train/Test split...")
    train, test = train_test_split_ts(series)
    train_series = train['Power']
    test_series = test['Power']

    # Step 6: Run models
    print("\n[6/8] Training models...")
    all_metrics = []

    # Persistence baseline
    persistence_pred, persistence_metrics = run_persistence(train_series, test_series)
    all_metrics.append(persistence_metrics)

    # ARIMA
    arima_pred, arima_metrics = run_arima(train_series, test_series)
    all_metrics.append(arima_metrics)

    # LSTM
    lstm_pred, lstm_metrics, lstm_actual = run_lstm(train_series, test_series)
    all_metrics.append(lstm_metrics)

    # Prophet
    prophet_pred, prophet_metrics = run_prophet(train_series, test_series)
    all_metrics.append(prophet_metrics)

    # Step 6b: Diebold-Mariano significance tests
    print("\n[6b/8] Diebold-Mariano tests (squared-error loss, two-sided)...")
    test_arr = test_series.values
    n_test = len(test_arr)
    dm_results = []
    pairs = [
        ("ARIMA", arima_pred, "Persistence", persistence_pred),
        ("LSTM", lstm_pred[:n_test], "Persistence", persistence_pred[-len(lstm_pred):][:n_test]
         if len(lstm_pred) < n_test else persistence_pred),
        ("Prophet", prophet_pred, "Persistence", persistence_pred),
        ("ARIMA", arima_pred, "LSTM", lstm_pred[:n_test] if len(lstm_pred) >= n_test else None),
        ("ARIMA", arima_pred, "Prophet", prophet_pred),
    ]
    for name1, p1, name2, p2 in pairs:
        if p2 is None or len(p1) != len(p2):
            min_n = min(len(p1), len(p2)) if p2 is not None else 0
            if min_n < 3:
                print(f"  Skipped {name1} vs {name2}: length mismatch")
                continue
            actual_use = test_arr[:min_n]
            p1, p2 = p1[:min_n], p2[:min_n]
        else:
            actual_use = test_arr[:len(p1)]
        result = diebold_mariano_test(actual_use, p1, p2)
        result["model_1"] = name1
        result["model_2"] = name2
        dm_results.append(result)
        sig = "***" if result["p_value"] < 0.01 else ("**" if result["p_value"] < 0.05
              else ("*" if result["p_value"] < 0.10 else "n.s."))
        better = name1 if result["DM"] < 0 else name2
        print(f"  {name1:>11} vs {name2:<11}: DM = {result['DM']:>7.3f}, "
              f"p = {result['p_value']:.4f} {sig:>4}  -> {better} has lower error")
    # Save DM table
    pd.DataFrame(dm_results).to_csv(os.path.join(RESULTS_DIR, "dm_test_results.csv"), index=False)

    # Step 7: Visualize comparison
    print("\n[7/8] Generating comparison plots...")
    plot_model_comparison(
        test.index, test_series.values,
        arima_pred, lstm_pred, lstm_actual, prophet_pred
    )

    # Step 8: Metrics summary
    print("\n[8/8] Metrics summary...")
    plot_metrics_comparison(all_metrics)

    # Practical interpretation (cost / accuracy in domain units)
    mean_consumption = float(test_series.mean())
    arima_rmse = arima_metrics["RMSE"]
    rmse_pct = 100 * arima_rmse / mean_consumption if mean_consumption > 0 else float("nan")
    daily_kwh_error = arima_rmse * 24 / 1000  # 1 day of avg-power error -> kWh
    print(f"\nPractical interpretation (ARIMA, House {HOUSE_ID}):")
    print(f"  Mean daily test consumption: {mean_consumption:.1f} W")
    print(f"  ARIMA RMSE: {arima_rmse:.2f} W  ({rmse_pct:.1f}% of mean)")
    print(f"  Equivalent daily energy error: ~{daily_kwh_error:.2f} kWh/day")

    print("\n" + "=" * 60)
    print("DONE! All results saved to:", RESULTS_DIR)
    print("=" * 60)

    return all_metrics, dm_results, mean_consumption


if __name__ == "__main__":
    main()
