"""
Generate the comprehensive Final Project Report (DOCX) and convert to PDF.

Clean style:
 - Calibri throughout
 - 1.3 line spacing
 - No em-dash, no superscript R-squared, no et al., no subscript digits
 - "and others" instead of "et al."

Rich content:
 - Cover page
 - Abstract
 - Section structure: Intro -> Data -> Methodology -> Results -> Discussion -> Conclusion
 - All 6 EDA/result figures + 4 custom diagrams
 - Results tables
 - References
"""
import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, "results")
OUTPUT_DOCX = os.path.join(BASE, "EBT629E_Final_Project_Report.docx")
OUTPUT_PDF = os.path.join(BASE, "EBT629E_Final_Project_Report.pdf")

doc = Document()

# Page setup
for section in doc.sections:
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.4)
    section.right_margin = Cm(2.4)

# Default style
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.3
style.paragraph_format.space_after = Pt(5)

NAVY = RGBColor(0, 51, 102)
GREY = RGBColor(80, 80, 80)


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def add_heading(text, level=1, color=NAVY):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = color
        run.font.name = 'Calibri'
    return h


def add_para(text, lead_bold=None, justify=True):
    p = doc.add_paragraph()
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if lead_bold:
        r = p.add_run(lead_bold)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(11)
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(11)
    return p


def add_figure(filename, caption, width=Inches(6.0)):
    path = os.path.join(RESULTS, filename)
    if not os.path.exists(path):
        doc.add_paragraph(f"[Figure missing: {filename}]")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run()
    run.add_picture(path, width=width)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(10)
    r = cap.add_run(caption)
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = 'Calibri'


def add_bullet(text):
    p = doc.add_paragraph(text, style='List Bullet')
    for r in p.runs:
        r.font.name = 'Calibri'
        r.font.size = Pt(11)


def add_table_caption(text):
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(2)
    r = cap.add_run(text)
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = 'Calibri'


# ============================================================
# COVER PAGE
# ============================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Istanbul Technical University")
r.font.size = Pt(14)
r.font.name = 'Calibri'
r.font.color.rgb = GREY

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("EBT 629E, Artificial Intelligence")
r.font.size = Pt(14)
r.font.name = 'Calibri'
r.font.color.rgb = GREY

doc.add_paragraph()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Final Project Report")
r.font.size = Pt(22)
r.bold = True
r.font.name = 'Calibri'
r.font.color.rgb = NAVY

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Household Energy Consumption Forecasting\nUsing Time Series Models")
r.font.size = Pt(16)
r.bold = True
r.font.name = 'Calibri'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("A Comparative Study of ARIMA, LSTM, and FB-Prophet on the REFIT Dataset")
r.font.size = Pt(12)
r.italic = True
r.font.name = 'Calibri'
r.font.color.rgb = GREY

for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Group Members")
r.font.size = Pt(12)
r.bold = True
r.font.name = 'Calibri'

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(
    "Nurullah Yıldırım (301252004)\n"
    "Kadir Göksel Gündüz (301241077)\n"
    "Furkan Çınar (301212001)"
)
r.font.size = Pt(12)
r.font.name = 'Calibri'

for _ in range(3):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("May 2026")
r.font.size = Pt(12)
r.font.name = 'Calibri'
r.font.color.rgb = GREY

doc.add_page_break()

# ============================================================
# ABSTRACT
# ============================================================
add_heading("Abstract", level=1)
add_para(
    "This report presents a comparative study of three time series forecasting models, ARIMA, "
    "Long Short-Term Memory (LSTM), and FB-Prophet, applied to household energy consumption data "
    "from the REFIT Smart Home dataset. We use 22 months of 8-second resolution measurements from "
    "House 2, aggregate them to daily mean power and apply a 7-day rolling smoother, then split "
    "the series temporally into 80 percent training and 20 percent testing. The ARIMA model is "
    "tuned through an ADF-based stationarity test and a grid search over (p, d, q) on the AIC "
    "criterion, then deployed under a rolling one-step-ahead protocol. The LSTM model uses a "
    "three-layer stacked recurrent architecture with dropout and is trained for up to 100 epochs "
    "with early stopping. Prophet is configured with weekly and yearly seasonality and runs in "
    "single multi-step mode. ARIMA reaches the best accuracy (R2 = 0.876, RMSE = 48.7 W), "
    "followed by LSTM (R2 = 0.193) and Prophet (R2 = 0.015). The wide gap between ARIMA and the "
    "other two models is attributable in part to the forecasting protocol: ARIMA and LSTM benefit "
    "from teacher forcing while Prophet must commit to a 122-day forecast at once. The results "
    "echo the conclusions of recent literature that classical statistical models stay competitive "
    "for short-horizon residential forecasting, while deep learning gains are conditional on data "
    "scale and matching evaluation protocols. The full code base, with fixed random seed and "
    "reproducible pipeline, is provided alongside this report."
)

doc.add_page_break()

# ============================================================
# 1. INTRODUCTION
# ============================================================
add_heading("1. Introduction", level=1)

add_heading("1.1 Background and Motivation", level=2)
add_para(
    "Household electricity consumption sits at the centre of several modern energy challenges. "
    "On the supply side, accurate short-term forecasts are needed for grid operators to balance "
    "renewable generation, plan reserve capacity, and reduce curtailment. On the demand side, "
    "they enable consumers to participate in demand-response programmes, schedule appliances "
    "intelligently, and optimise integration with rooftop photovoltaic and battery storage "
    "systems. The widespread roll-out of smart meters across Europe and the increasing maturity "
    "of machine learning frameworks have made it feasible to study this problem at the level of "
    "individual households rather than at the substation level."
)
add_para(
    "Forecasting residential consumption is, however, structurally harder than forecasting "
    "aggregated demand. A single household exhibits abrupt switching events (kettles, ovens, "
    "washing machines), idiosyncratic schedules driven by occupant behaviour, and seasonality "
    "that interacts with weather and holidays. Smoothing across many households averages much "
    "of this noise away, which is one reason that grid-level forecasts often report low MAPE "
    "while household-level forecasts can fail outright."
)

add_heading("1.2 Project Objectives", level=2)
add_para(
    "The present project asks a focused, practical question: among three widely used time series "
    "models, ARIMA, LSTM, and FB-Prophet, which is best suited to forecasting the daily energy "
    "consumption of a single household, and why? Concretely, the project pursues four objectives."
)
add_bullet("Build a reproducible pipeline from raw 8-second REFIT readings to model outputs.")
add_bullet("Compare ARIMA, LSTM, and FB-Prophet on a single test bed under the same data split.")
add_bullet("Quantify the gap between models using MSE, RMSE, MAE, and R2 metrics.")
add_bullet("Investigate where each model wins or loses, and document the iterations that led to "
           "the final design.")

add_heading("1.3 Report Structure", level=2)
add_para(
    "Section 2 introduces the REFIT dataset and the chosen household. Section 3 details the "
    "preprocessing pipeline and the three modelling approaches, including the rolling forecast "
    "protocol that distinguishes our setup from many of the multi-step benchmarks reported in "
    "the literature. Section 4 presents the exploratory data analysis. Section 5 reports the "
    "quantitative results and visual comparisons. Section 6 discusses the findings, the "
    "limitations of the study, and threats to validity. Section 7 closes with conclusions and "
    "directions for further work."
)

# ============================================================
# 2. DATASET
# ============================================================
add_heading("2. Dataset: REFIT Smart Home Electrical Load Measurements", level=1)

add_heading("2.1 Overview", level=2)
add_para(
    "REFIT (Personalised Retrofit Decision Support Tools for UK Homes) is a longitudinal dataset "
    "collected between October 2013 and June 2015 in the Loughborough area of the United Kingdom. "
    "The data was produced by a consortium of the Universities of Strathclyde, Loughborough, and "
    "East Anglia under EPSRC funding and is released under a Creative Commons Attribution 4.0 "
    "International licence. Twenty households were instrumented (numbered House 1 to House 21, "
    "skipping House 14) with one current clamp on the whole-house feed and nine Individual "
    "Appliance Monitors per home. Active power was sampled in Watts at roughly one reading every "
    "six to eight seconds, which produced a corpus of about 1.19 billion observations across all "
    "houses (Murray, Stankovic, and Stankovic, 2017)."
)

add_heading("2.2 Selected Household: House 2", level=2)
add_para(
    "We use House 2 as the test bed for this project. The CSV file is 299 MB on disk and contains "
    "5,733,526 timestamped readings spanning 22 months. The monitored appliances are Fridge-"
    "Freezer, Washing Machine, Dishwasher, Television, Microwave, Toaster, Hi-Fi, Kettle, and "
    "Oven Extractor Fan. House 2 was selected because it has no documented signature changes, no "
    "rooftop PV interference, and represents a typical UK household appliance mix."
)

# Correlation heatmap
add_figure("correlation_heatmap.png",
           "Figure 1. Pearson correlation among the aggregate power channel and the nine "
           "individual appliance monitors in House 2.",
           width=Inches(5.5))

add_heading("2.3 Data Quality and Cleaning", level=2)
add_para(
    "The REFIT release applies forward-filling for short gaps and zeros out gaps longer than "
    "two minutes. Readings above 4000 W on appliance channels (above sensor range) have already "
    "been removed by the original maintainers. Our additional cleaning steps remove negative "
    "aggregate readings (caused by clamp polarity glitches) and trim the upper one percent of "
    "values as outliers. After these steps, the aggregate series is continuous and ready for "
    "resampling."
)

doc.add_page_break()

# ============================================================
# 3. METHODOLOGY
# ============================================================
add_heading("3. Methodology", level=1)

add_figure("pipeline_diagram.png",
           "Figure 2. End-to-end machine learning pipeline. Raw 8-second REFIT data flows "
           "through outlier removal, daily resampling, and 7-day smoothing, then feeds three "
           "competing models whose forecasts are evaluated against the held-out test set.",
           width=Inches(6.3))

add_heading("3.1 Data Preprocessing", level=2)
add_para(
    "Five preprocessing steps prepare the raw signal for modelling. First, the timestamp column "
    "is parsed into a pandas DatetimeIndex. Second, the Unix epoch column is dropped to save "
    "memory. Third, outlier filtering removes negative values and entries above the 99th "
    "percentile. Fourth, the cleaned series is resampled to daily means, reducing 5.7 million "
    "rows to roughly 630 daily observations and removing most of the appliance-level switching "
    "noise. Fifth, a centred 7-day rolling mean is applied to suppress residual day-of-week "
    "variability while keeping the weekly and seasonal cycles intact."
)
add_para(
    "Missing days, where the rolling mean would otherwise produce a NaN, are forward and backward "
    "filled before the dataset is split temporally. The split keeps the first 80 percent of days "
    "for training and the last 20 percent for testing, which is the standard protocol for time "
    "series with non-stationary trends."
)

add_heading("3.2 ARIMA Model", level=2)
add_para(
    "ARIMA(p, d, q) is the workhorse of statistical time series forecasting. We follow the Box-"
    "Jenkins procedure. The Augmented Dickey-Fuller test on the training set returned a p-value "
    "of 0.94, indicating non-stationarity, so a single differencing order (d = 1) was applied. "
    "A grid search over p in [0, 2] and q in [0, 2] then selected the configuration with the "
    "lowest AIC, which was ARIMA(2, 1, 2) at AIC = 4547.63."
)
add_para(
    "The final ARIMA model is deployed under a rolling one-step-ahead protocol: at each test "
    "day, the model is re-fitted on all data observed up to that point and asked to forecast the "
    "next day only. This matches how a real operator would use such a model in production, where "
    "yesterday's actual reading is always available before today's forecast must be made.",
    lead_bold="Rolling forecast protocol. "
)

add_heading("3.3 LSTM Model", level=2)
add_para(
    "The LSTM model is a three-layer stacked recurrent network with 128, 64, and 32 units, "
    "interleaved with dropout layers at rate 0.2 and topped with a 16-unit ReLU dense layer "
    "before the linear output. Inputs are 14-day sliding windows of Min-Max scaled power values. "
    "Training uses the Adam optimiser with mean squared error loss, batch size 16, and up to 100 "
    "epochs with early stopping triggered after 5 stagnant validation epochs. A fixed random "
    "seed (42) is used to make the run reproducible across machines."
)

add_figure("lstm_architecture.png",
           "Figure 3. LSTM network architecture, hyperparameters, and training configuration "
           "used in this project.",
           width=Inches(5.5))

add_heading("3.4 FB-Prophet Model", level=2)
add_para(
    "FB-Prophet decomposes a series into trend, seasonality, and holiday effects, fitting each "
    "component as an additive (or multiplicative) signal. We enable weekly and yearly "
    "seasonality, disable daily seasonality (irrelevant after daily resampling), and use the "
    "multiplicative mode, which is appropriate when the amplitude of seasonal swings scales with "
    "the overall level. The changepoint prior scale is left at 0.05, the package default for "
    "moderately flexible trends."
)
add_para(
    "Crucially, Prophet is run in single multi-step mode, that is, it forecasts the entire "
    "122-day test horizon in one shot, without access to test-set actuals. This is the canonical "
    "way Prophet is deployed in practice, but it puts it at a structural disadvantage relative "
    "to the rolling protocols used for ARIMA and LSTM. We return to this point in the discussion.",
    lead_bold="Multi-step protocol. "
)

add_figure("rolling_forecast.png",
           "Figure 4. Comparison of the two forecasting protocols. ARIMA and LSTM see the "
           "previous day's actual value before producing each forecast, while Prophet must "
           "commit to the entire test horizon based on training data only.",
           width=Inches(6.3))

add_heading("3.5 Evaluation Metrics", level=2)
add_para(
    "Predictive accuracy is measured with four complementary metrics. Mean Squared Error (MSE) "
    "and Root Mean Squared Error (RMSE) penalise large errors heavily and report in the original "
    "Watt units (RMSE only). Mean Absolute Error (MAE) is more robust to outliers and is also "
    "expressed in Watts. The coefficient of determination (R2) gives a unit-free measure of how "
    "much of the variance is explained, ranging from 1 (perfect) to negative values for models "
    "that perform worse than the mean baseline."
)

doc.add_page_break()

# ============================================================
# 4. EXPLORATORY DATA ANALYSIS
# ============================================================
add_heading("4. Exploratory Data Analysis", level=1)

add_para(
    "Before modelling, we inspected the cleaned aggregate signal to characterise its temporal "
    "structure. The four panels in Figure 5 summarise the analysis."
)

add_figure("data_analysis.png",
           "Figure 5. Exploratory analysis of House 2. Top-left: daily mean power across "
           "22 months. Top-right: hourly profile computed on the raw 8-second data (consumption "
           "peaks around 16:00 to 20:00 corresponding to cooking and lighting). Bottom-left: "
           "average daily power by weekday (weekends are higher). Bottom-right: distribution of "
           "daily power.",
           width=Inches(6.2))

add_para(
    "Three findings emerged. First, the daily series shows a clear seasonal cycle, with winter "
    "consumption substantially higher than summer, consistent with electric heating use. Second, "
    "the hourly profile, computed on raw data so the pattern is not collapsed by daily "
    "aggregation, has the classic two-peak shape of UK households, a smaller morning peak and a "
    "pronounced evening peak between 16:00 and 20:00. Third, the day-of-week breakdown reveals "
    "weekend consumption is about 15 percent higher than midweek, reflecting longer occupancy "
    "hours."
)

# ============================================================
# 5. RESULTS
# ============================================================
add_heading("5. Results", level=1)

add_heading("5.1 Final Performance Comparison", level=2)
add_para(
    "Table 1 reports the test-set metrics for all three models. ARIMA is the clear winner across "
    "all four metrics, with an R2 of 0.876, roughly four times that of LSTM and sixty times that "
    "of Prophet. The RMSE gap is even more striking: ARIMA at 48.7 W versus 124.2 W for LSTM and "
    "137.3 W for Prophet."
)

add_table_caption("Table 1. Test set performance of the three models on House 2 daily forecasts.")

table = doc.add_table(rows=4, cols=5, style='Light Grid Accent 1')
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['Model', 'MSE', 'RMSE (W)', 'MAE (W)', 'R2']
data = [
    ['ARIMA(2,1,2)', '2,370.01', '48.68', '32.75', '0.876'],
    ['LSTM (3-layer)', '15,436.04', '124.24', '93.59', '0.193'],
    ['FB-Prophet',    '18,851.52', '137.30', '111.70', '0.015'],
]
for i, h in enumerate(headers):
    c = table.rows[0].cells[i]
    c.text = h
    for p in c.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(10)
            r.font.name = 'Calibri'
for r_idx, row in enumerate(data):
    for c_idx, v in enumerate(row):
        c = table.rows[r_idx + 1].cells[c_idx]
        c.text = v
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(10)
                r.font.name = 'Calibri'

doc.add_paragraph()

add_figure("metrics_comparison.png",
           "Figure 6. Side-by-side comparison of the four evaluation metrics across the three "
           "models. Lower is better for MSE, RMSE, and MAE; higher is better for R2.",
           width=Inches(6.3))

add_heading("5.2 Predicted versus Actual Series", level=2)
add_para(
    "Figure 7 plots each model's predictions against the held-out test values. The ARIMA panel "
    "tracks the actual series closely because rolling re-fitting keeps the predictor anchored to "
    "the most recent observed value. The LSTM panel captures the broad direction of the trend "
    "but oversmooths the peaks and troughs. The Prophet panel essentially produces a piecewise "
    "linear baseline plus seasonality, which is reasonable as an average but fails to follow the "
    "sharper movements present in the actual data."
)

add_figure("model_comparison.png",
           "Figure 7. Actual versus predicted daily mean power for ARIMA, LSTM, and FB-Prophet "
           "across the 122-day test window.",
           width=Inches(6.3))

add_heading("5.3 Training Diagnostics", level=2)
add_para(
    "The LSTM training loss curve in Figure 8 shows fast initial convergence and a plateau "
    "after roughly 12 epochs, at which point early stopping was triggered. The validation loss "
    "tracks the training loss closely, suggesting that overfitting is not the dominant issue, "
    "but rather that the model has reached the limit of what it can extract from the smoothed "
    "daily signal."
)

add_figure("lstm_training_history.png",
           "Figure 8. LSTM training and validation MSE loss across epochs.",
           width=Inches(5.0))

add_para(
    "Prophet's decomposition (Figure 9) highlights a clear yearly trend (consumption highest in "
    "winter, lowest in summer) and a moderate weekly cycle. These components are sensible and "
    "match the EDA, but the overall fit is dominated by the long-horizon trend rather than "
    "short-horizon dynamics."
)

add_figure("prophet_components.png",
           "Figure 9. FB-Prophet decomposition showing the underlying trend, weekly seasonality, "
           "and yearly seasonality fitted on the training portion of House 2.",
           width=Inches(5.5))

add_heading("5.4 Development Iterations", level=2)
add_para(
    "The final results in Table 1 were not achieved on the first attempt. We documented the "
    "design decisions that moved the R2 of the best model from negative territory to 0.876. "
    "Figure 10 summarises the three iterations."
)

add_figure("iteration_timeline.png",
           "Figure 10. Three iterations of the design and their effect on test R2. The change "
           "that mattered most was the move from a single multi-step ARIMA forecast to a "
           "rolling one-step-ahead protocol.",
           width=Inches(6.3))

doc.add_page_break()

# ============================================================
# 6. DISCUSSION
# ============================================================
add_heading("6. Discussion", level=1)

add_heading("6.1 Why ARIMA Wins", level=2)
add_para(
    "ARIMA's strong showing is driven by two factors. The first is data character: residential "
    "energy at the daily level has strong autocorrelation at lag 1, so the previous day is by "
    "far the most informative single feature for the current day. ARIMA(2, 1, 2) makes direct "
    "use of this through its autoregressive and moving average terms. The second is the "
    "forecasting protocol: every step is informed by the latest actual value, which keeps "
    "ARIMA's predictions anchored even if its underlying parameters drift slightly over the "
    "test window."
)

add_heading("6.2 Why LSTM Underperforms", level=2)
add_para(
    "LSTM's modest score is not a verdict on deep learning, it is a comment on the data scale. "
    "The training set contains 490 daily observations, which means only 476 input sequences "
    "after the 14-day lookback. Deep learning architectures with around 129,000 parameters "
    "typically need orders of magnitude more samples to reach their full potential. The "
    "training and validation curves in Figure 8 confirm that the model has converged but has "
    "not generalised well. Recent work (Gasparin and others, 2024) reports a similar pattern: "
    "below six months of training data, simple baselines beat deep models, and only with nine "
    "or more months do the deep architectures start to pull ahead."
)

add_heading("6.3 Why Prophet Looks the Worst", level=2)
add_para(
    "Prophet's near-zero R2 deserves careful interpretation. Two factors are at play. First, "
    "Prophet produces a single multi-step forecast for the entire 122-day horizon, with no "
    "access to test actuals, which puts it at a structural disadvantage against the rolling "
    "ARIMA and LSTM setups. Second, Prophet's strength lies in capturing slow seasonal trends "
    "and calendar effects, both of which are present but neither is the dominant driver of "
    "House 2 daily consumption. The residual day-to-day variation, which represents most of the "
    "test-set variance, is precisely the component Prophet does not try to model."
)
add_para(
    "The takeaway is not that Prophet is a weak model, but that the comparison rules favour "
    "models that can use teacher forcing. A fair comparison on this dataset would also run "
    "Prophet in a rolling refit mode, which we leave for future work because it requires roughly "
    "two orders of magnitude more compute."
)

add_heading("6.4 Limitations and Threats to Validity", level=2)
add_para(
    "Three limitations qualify our conclusions."
)
add_bullet("Single household. House 2 may not be representative of the other 19 REFIT homes, "
           "and the rankings could shift on a different occupancy or appliance mix.")
add_bullet("Univariate setup. None of the models receive weather, calendar, or appliance-level "
           "exogenous data. Adding these would likely close the gap, particularly for LSTM.")
add_bullet("Heavy smoothing. The 7-day rolling mean removes much of the high-frequency content. "
           "An operational forecaster who needs daily ramping information would have to revisit "
           "this choice.")

add_heading("6.5 Comparison with Reference Literature", level=2)
add_para(
    "The ordering ARIMA greater than LSTM greater than Prophet, observed here, matches the "
    "findings of Bülüç, Sevli, and Yünlü (2025), who reported R2 = 0.97 for ARIMA on Istanbul "
    "solar production data using a similar rolling protocol. It differs from Demirtop and Sevli "
    "(2024), where LSTM beat ARIMA on wind speed; the difference is most likely the longer time "
    "series available in that study and the use of multi-year hourly data. Hybrid models such as "
    "CNN-LSTM-Transformer (Limouni and others, 2023) and STL-Prophet-LSTM (Xie and others, 2022) "
    "consistently outperform their components and represent the natural next step beyond the "
    "single-model baselines compared here."
)

# ============================================================
# 7. CONCLUSION
# ============================================================
add_heading("7. Conclusion and Future Work", level=1)

add_para(
    "We built a reproducible pipeline that forecasts the daily mean power consumption of a "
    "single UK household using three time series methods. Under a rolling one-step-ahead "
    "protocol and a fixed random seed, ARIMA(2, 1, 2) reached R2 = 0.876 on 122 unseen days, "
    "outperforming a three-layer LSTM (R2 = 0.193) and FB-Prophet (R2 = 0.015). The lessons we "
    "carry forward are that the forecasting protocol can dominate model choice for short series, "
    "that residential daily energy has strong lag-one autocorrelation that classical models "
    "exploit naturally, and that deep architectures require substantially more data than was "
    "available here."
)

add_para(
    "Four directions stand out for further work."
)
add_bullet("Extending the rolling protocol to Prophet for a fair multi-model comparison.")
add_bullet("Adding weather (temperature, irradiance) and calendar features through SARIMAX and "
           "multivariate LSTM.")
add_bullet("Cross-household transfer learning across all 20 REFIT homes to amortise the deep "
           "learning training cost.")
add_bullet("Hybrid models such as STL-Prophet-LSTM and CNN-LSTM-Transformer that combine the "
           "strengths of decomposition and neural sequence learning.")

add_heading("Reproducibility Note", level=2)
add_para(
    "All experiments use a fixed random seed (42) for NumPy, Python's random module, and "
    "TensorFlow. The dataset is downloaded from the public Kaggle mirror of REFIT, and the "
    "preprocessing, training, and evaluation are encoded in a single Python script "
    "(energy_forecasting.py). Results in this report were obtained on Python 3.13, TensorFlow "
    "2.x, statsmodels 0.14, and Prophet 1.3."
)

# ============================================================
# REFERENCES
# ============================================================
add_heading("References", level=1)

refs = [
    "Atalay, B. A., and Zor, K. (2025). XGBoost ile hidroelektrik enerji tahmini. "
    "Çukurova Üniversitesi Mühendislik Fakültesi Dergisi, 40(1), 205-218.",

    "Berus, Y., and Yakut, Y. B. (2024). Derin öğrenme (1D-CNN, RNN, LSTM, BiLSTM) ile enerji "
    "tüketim tahmini: Diyarbakır AVM örneği. Dicle University Journal of Engineering, 15(2), "
    "311-322.",

    "Bülüç, M., Sevli, O., and Yünlü, L. (2025). Time Series Analysis of Solar Energy Production "
    "Based on Weather Conditions. GU J Sci, Part A, 12(4), 1060-1077.",

    "Çolak, M. B., and Özhan, E. (2025). Renewable energy forecasting in Turkey: Analytical "
    "approaches. Journal of Intelligent Systems: Theory and Applications, 8(1), 25-34.",

    "Demirtop, A., and Sevli, O. (2024). Wind speed prediction using LSTM and ARIMA time series "
    "analysis models: A case study of Gelibolu. Turkish Journal of Engineering, 8(3), 524-536.",

    "Gasparin, A., Lukovic, S., and Alippi, C. (2024). Load Forecasting for Households and "
    "Energy Communities: Are Deep Learning Models Worth the Effort? arXiv:2501.05000.",

    "Limouni, T., Yaagoubi, R., Bouziane, K., Guissi, K., and Baali, E. H. (2023). Solar Energy "
    "Production Forecasting Based on a Hybrid CNN-LSTM-Transformer Model. Mathematics, 11(3), 676.",

    "Murray, D., Stankovic, L., and Stankovic, V. (2017). An electrical load measurements "
    "dataset of United Kingdom households from a two-year longitudinal study. Scientific Data, "
    "4, 160122.",

    "Rahman, M. R., and others (2025). Time-series and deep learning approaches for renewable "
    "energy forecasting in Dhaka: a comparative study of ARIMA, SARIMA, and LSTM models. "
    "Discover Sustainability, 6, 01733.",

    "Sakib, N., and others (2024). Deep learning-driven hybrid model for short-term load "
    "forecasting and smart grid information management. Scientific Reports, 14, 63262.",

    "Tamay, M., and Türker, G. F. (2024). Machine learning based energy forecasting for "
    "photovoltaic solar plants. Yekarum, 9(2), 128-146.",

    "Triebe, O., Hewamalage, H., Pilyugina, P., Laptev, N., Bergmeir, C., and Rajagopal, R. "
    "(2021). NeuralProphet: Explainable Forecasting at Scale. arXiv:2111.15397.",

    "Vargas-Forero, V. M., Manotas-Duque, D. F., and Trujillo, L. (2025). Comparative study of "
    "forecasting methods to predict the energy demand for the market of Colombia. International "
    "Journal of Energy Economics and Policy, 15(1), 65-76.",

    "Xie, J., Li, Z., Zhou, Z., and Liu, S. (2022). A hybrid forecasting model using LSTM and "
    "Prophet for energy consumption with decomposition of time series data. PeerJ Computer "
    "Science, 8, e1001.",
]

for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(f"[{i}] {ref}")
    r.font.size = Pt(9.5)
    r.font.name = 'Calibri'


# ============================================================
# SAVE DOCX
# ============================================================
doc.save(OUTPUT_DOCX)
print(f"DOCX saved: {OUTPUT_DOCX}")
print(f"DOCX size: {os.path.getsize(OUTPUT_DOCX)/1024:.0f} KB")

# ============================================================
# CONVERT TO PDF
# ============================================================
print("\nConverting to PDF...")
try:
    from docx2pdf import convert
    convert(OUTPUT_DOCX, OUTPUT_PDF)
    print(f"PDF saved: {OUTPUT_PDF}")
    print(f"PDF size: {os.path.getsize(OUTPUT_PDF)/1024:.0f} KB")
except Exception as e:
    print(f"docx2pdf failed: {e}")
    print("Will try alternative PDF conversion methods.")
