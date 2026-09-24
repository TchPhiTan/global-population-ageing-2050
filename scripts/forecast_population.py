from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, mean_absolute_error, mean_squared_error, precision_score, r2_score, recall_score
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]
WIDE_INPUT = ROOT / "data" / "processed" / "population_fact_wide.csv"
OUTPUT_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports" / "modeling"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def is_country(code: str | None) -> bool:
    if not code:
        return False
    return (len(code) == 3 and code.isalpha() and code.isupper()) or code == "OWID_KOS"


def load_wide_data() -> list[dict[str, str]]:
    with WIDE_INPUT.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    sns.set_theme(style="whitegrid")
    rows = load_wide_data()
    country_rows = [r for r in rows if is_country(r.get("Code"))]

    countries = sorted(list(set(r["Entity"] for r in country_rows)))
    code_map = {r["Entity"]: r["Code"] for r in country_rows}

    # Group data by country
    country_pop_hist: dict[str, dict[int, float]] = defaultdict(dict)
    country_growth: dict[str, dict[int, float]] = defaultdict(dict)
    country_tfr: dict[str, dict[int, float]] = defaultdict(dict)

    for r in country_rows:
        entity = r["Entity"]
        year = int(r["Year"])
        if r.get("Population"):
            country_pop_hist[entity][year] = float(r["Population"])
        if r.get("Population growth rate"):
            country_growth[entity][year] = float(r["Population growth rate"])
        if r.get("Total fertility rate"):
            country_tfr[entity][year] = float(r["Total fertility rate"])

    print(f"Bắt đầu huấn luyện mô hình cho {len(countries)} quốc gia/vùng lãnh thổ...")

    # -------------------------------------------------------------
    # 1. LINEAR REGRESSION FOR POPULATION FORECAST (TO 2050)
    # -------------------------------------------------------------
    # Train-test split evaluation (Train: <= 2015, Test: 2016-2023)
    test_actuals = []
    test_preds = []

    for entity in countries:
        years = sorted([y for y in country_pop_hist[entity] if y <= 2023])
        train_years = [y for y in years if y <= 2015]
        test_years = [y for y in years if 2016 <= y <= 2023]

        if len(train_years) >= 10 and test_years:
            X_tr = np.array(train_years).reshape(-1, 1)
            y_tr = np.array([country_pop_hist[entity][y] for y in train_years])
            model_eval = LinearRegression()
            model_eval.fit(X_tr, y_tr)

            X_te = np.array(test_years).reshape(-1, 1)
            preds = model_eval.predict(X_te)

            test_actuals.extend([country_pop_hist[entity][y] for y in test_years])
            test_preds.extend(preds)

    r2_eval = r2_score(test_actuals, test_preds)
    rmse_eval = math.sqrt(mean_squared_error(test_actuals, test_preds))
    mae_eval = mean_absolute_error(test_actuals, test_preds)

    print(f"Đánh giá Linear Regression trên Test Set (2016-2023): R2 = {r2_eval:.4f}, MAE = {mae_eval:,.0f} người")

    # Fit on all available historical data (1950 - 2026) and generate forecast 2027 - 2050
    forecast_rows = []
    forecast_2050_map = {}

    for entity in countries:
        code = code_map[entity]
        all_known_years = sorted(country_pop_hist[entity].keys())

        # Include historical + current data up to 2026
        for y in all_known_years:
            if y <= 2026:
                status = "estimate" if y <= 2023 else "projected"
                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": y,
                    "Population": country_pop_hist[entity][y],
                    "DataStatus": status,
                    "Model": "actual_or_un_wpp",
                })

        # Fit linear regression model using past 30 years (1996 - 2026) for stable local trend
        reg_years = [y for y in all_known_years if 1996 <= y <= 2026]
        if len(reg_years) >= 10:
            X = np.array(reg_years).reshape(-1, 1)
            y_vals = np.array([country_pop_hist[entity][yr] for yr in reg_years])
            reg = LinearRegression()
            reg.fit(X, y_vals)

            future_years = list(range(2027, 2051))
            future_preds = reg.predict(np.array(future_years).reshape(-1, 1))

            for yr, p in zip(future_years, future_preds):
                pop_pred = max(p, 500.0)  # non-negative population floor
                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population": round(pop_pred),
                    "DataStatus": "forecast",
                    "Model": "linear_regression",
                })
                if yr == 2050:
                    forecast_2050_map[entity] = pop_pred
        else:
            # Fallback if sparse
            last_val = country_pop_hist[entity].get(2026, 0)
            forecast_2050_map[entity] = last_val
            for yr in range(2027, 2051):
                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population": round(last_val),
                    "DataStatus": "forecast",
                    "Model": "constant_fallback",
                })

    # Save population_forecast_2050.csv
    forecast_path = OUTPUT_DIR / "population_forecast_2050.csv"
    with forecast_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Entity", "Code", "Year", "Population", "DataStatus", "Model"])
        writer.writeheader()
        writer.writerows(forecast_rows)
    print(f"Đã lưu bảng dự báo dân số đến 2050 tại: {forecast_path} ({len(forecast_rows):,} dòng)")

    # -------------------------------------------------------------
    # 2. LOGISTIC REGRESSION FOR DEPOPULATION RISK CLASSIFICATION
    # -------------------------------------------------------------
    # Target: 1 if population in 2050 < population in 2026 OR growth rate in 2026 < 0
    # Features: growth_rate_2026, tfr_2023, log10_pop_2026, growth_delta_5yr (2026 - 2020)
    X_list = []
    y_list = []
    feature_entities = []

    for entity in countries:
        pop_2026 = country_pop_hist[entity].get(2026)
        pop_2050 = forecast_2050_map.get(entity)
        growth_2026 = country_growth[entity].get(2026)
        growth_2020 = country_growth[entity].get(2020, growth_2026)
        tfr_2023 = country_tfr[entity].get(2023, 1.8)

        if pop_2026 and pop_2050 and growth_2026 is not None:
            is_depopulating = 1 if (pop_2050 < pop_2026 or growth_2026 < 0) else 0
            growth_delta = growth_2026 - growth_2020
            log_pop = math.log10(max(pop_2026, 1000.0))

            X_list.append([growth_2026, tfr_2023, log_pop, growth_delta])
            y_list.append(is_depopulating)
            feature_entities.append(entity)

    X_mat = np.array(X_list)
    y_vec = np.array(y_list)

    X_train, X_test, y_train, y_test, ent_train, ent_test = train_test_split(
        X_mat, y_vec, feature_entities, test_size=0.25, random_state=42, stratify=y_vec
    )

    clf = LogisticRegression(random_state=42, max_iter=500)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Đánh giá Logistic Regression: Accuracy = {acc:.2%}, F1-score = {f1:.2%}")

    # Predict risk probabilities for all countries
    probs_all = clf.predict_proba(X_mat)[:, 1]
    risk_summary = []
    for ent, prob, actual_label in zip(feature_entities, probs_all, y_vec):
        risk_summary.append({
            "Entity": ent,
            "Code": code_map[ent],
            "Depopulation_Risk_Score": prob,
            "Risk_Category": "High Risk" if prob >= 0.6 else ("Moderate Risk" if prob >= 0.3 else "Low Risk"),
            "Actual_Flag": actual_label,
        })

    # Save evaluation plot
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Tăng trưởng (0)", "Suy giảm (1)"],
                yticklabels=["Tăng trưởng (0)", "Suy giảm (1)"])
    plt.title("Confusion Matrix - Logistic Regression Phân loại Nguy cơ Suy giảm", fontsize=11, fontweight="bold")
    plt.xlabel("Dự báo của Mô hình")
    plt.ylabel("Thực tế Phân loại")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "confusion_matrix.png", dpi=180)
    plt.close()

    # Forecast trajectory plot for prominent countries
    sample_entities = ["India", "China", "United States", "Nigeria", "Vietnam", "Japan"]
    plt.figure(figsize=(10.5, 6))
    for ent in sample_entities:
        ent_rows = [r for r in forecast_rows if r["Entity"] == ent]
        yrs = [r["Year"] for r in ent_rows]
        vals = [r["Population"] / 1e6 for r in ent_rows]
        plt.plot(yrs, vals, label=ent, linewidth=2)
    plt.axvline(2026, color="#d9534f", linestyle="--", label="Mốc hiện tại (2026)")
    plt.title("Dự báo Dân số đến năm 2050 cho các Quốc gia Tiêu biểu (Linear Regression)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Năm")
    plt.ylabel("Dân số (triệu người)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "forecast_trends_2050.png", dpi=180)
    plt.close()

    # -------------------------------------------------------------
    # 3. WRITE MODEL REPORT
    # -------------------------------------------------------------
    high_risk_sample = sorted([r for r in risk_summary if r["Risk_Category"] == "High Risk"], key=lambda x: x["Depopulation_Risk_Score"], reverse=True)[:10]

    report = [
        "# Báo cáo Mô hình Hóa Dự báo Dân số và Nguy cơ Suy giảm (Phase 3)",
        "",
        "## 1. Mục tiêu và Kiến trúc Mô hình",
        "- **Mô hình 1 (Hồi quy Tuyến tính - Linear Regression)**: Dự báo giá trị quy mô dân số liên tục từ năm 2027 đến năm 2050 cho 237 quốc gia/vùng lãnh thổ.",
        "- **Mô hình 2 (Hồi quy Logistic - Logistic Regression)**: Phân loại nhị phân nguy cơ một quốc gia bước vào chu kỳ suy giảm dân số kéo dài trước năm 2050 (`Depopulation_Risk`), không dùng để dự báo trực tiếp quy mô dân số (tuân thủ đặc tả đồ án).",
        "",
        "## 2. Kết quả Đánh giá Mô hình Dự báo Dân số (Linear Regression)",
        "Kiểm định mô hình theo phương pháp phân chia thời gian (Time-based train/test split):",
        "- **Tập huấn luyện (Train set)**: Giai đoạn 1950 - 2015.",
        "- **Tập kiểm định (Test set)**: Giai đoạn 2016 - 2023.",
        "",
        "| Chỉ số Đánh giá | Giá trị Đạt được | Ý nghĩa |",
        "| :--- | :---: | :--- |",
        f"| **Hệ số xác định ($R^2$)** | **{r2_eval:.4f}** | Mô hình giải thích được hơn {r2_eval*100:.1f}% phương sai biến động dân số trên tập kiểm định |",
        f"| **Sai số tuyệt đối trung bình (MAE)** | **{mae_eval:,.0f} người** | Độ lệch trung bình trên quy mô quốc gia |",
        f"| **Căn bậc hai sai số toàn phương (RMSE)** | **{rmse_eval:,.0f} người** | Mức độ tin cậy cao trên chu kỳ trung hạn |",
        "",
        "- **Dữ liệu đầu ra**: Toàn bộ chuỗi 1950 - 2050 đã được xuất ra file [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv).",
        "",
        "## 3. Kết quả Phân loại Nguy cơ Suy giảm Dân số (Logistic Regression)",
        "Mô hình phân loại nhị phân đánh giá xác suất quốc gia có nguy cơ suy giảm dân số đến năm 2050 dựa trên 4 đặc trưng: Tốc độ tăng trưởng 2026, Mức sinh TFR 2023, Quy mô dân số log10 và Độ suy giảm tăng trưởng 5 năm gần nhất.",
        "",
        "| Chỉ số Phân loại | Giá trị Kiểm định (Test Set) |",
        "| :--- | :---: |",
        f"| **Độ chính xác (Accuracy)** | **{acc:.2%}** |",
        f"| **Độ chuẩn xác (Precision)** | **{prec:.2%}** |",
        f"| **Độ thu hồi (Recall)** | **{rec:.2%}** |",
        f"| **Điểm F1-Score** | **{f1:.2%}** |",
        "",
        "### Ma trận nhầm lẫn (Confusion Matrix):",
        f"- True Negatives (Dự báo tăng trưởng - Thực tế tăng trưởng): {cm[0][0]}",
        f"- False Positives (Dự báo suy giảm - Thực tế tăng trưởng): {cm[0][1]}",
        f"- False Negatives (Dự báo tăng trưởng - Thực tế suy giảm): {cm[1][0]}",
        f"- True Positives (Dự báo suy giảm - Thực tế suy giảm): {cm[1][1]}",
        "",
        "## 4. Top 10 Quốc gia có Nguy cơ Suy giảm Dân số Cao nhất (High Depopulation Risk)",
        "| Thứ hạng | Quốc gia | Mã ISO | Điểm Nguy cơ (Risk Probability) | Phân loại |",
        "| :---: | :--- | :---: | :---: | :---: |",
    ]

    for idx, r in enumerate(high_risk_sample, 1):
        report.append(f"| {idx} | {r['Entity']} | {r['Code']} | {r['Depopulation_Risk_Score']:.2%} | {r['Risk_Category']} |")

    report.extend([
        "",
        "## 5. Hướng dẫn Tích hợp vào Dashboard Tableau (Phase 4)",
        "1. Nạp file [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv) vào Tableau.",
        "2. Tạo bộ lọc theo cột `DataStatus` (`estimate`, `projected`, `forecast`) để người xem có thể quan sát từng giai đoạn lịch sử - hiện tại - tương lai.",
        "3. Sử dụng trường `Model` để phân biệt dữ liệu điều tra thực tế với giá trị dự báo toán học.",
    ])

    report_path = REPORTS_DIR / "model_report.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Đã xuất báo cáo mô hình hóa tại: {report_path}")


if __name__ == "__main__":
    main()
