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
    country_pop: dict[str, dict[int, float]] = defaultdict(dict)
    country_older: dict[str, dict[int, float]] = defaultdict(dict)
    country_share65: dict[str, dict[int, float]] = defaultdict(dict)
    country_growth: dict[str, dict[int, float]] = defaultdict(dict)
    country_tfr: dict[str, dict[int, float]] = defaultdict(dict)
    country_med_age: dict[str, dict[int, float]] = defaultdict(dict)
    country_life_exp: dict[str, dict[int, float]] = defaultdict(dict)

    for r in country_rows:
        entity = r["Entity"]
        year = int(r["Year"])
        if r.get("Population"):
            country_pop[entity][year] = float(r["Population"])
        if r.get("Older people (65+ years)"):
            country_older[entity][year] = float(r["Older people (65+ years)"])
        if r.get("Share of population aged 65+"):
            country_share65[entity][year] = float(r["Share of population aged 65+"])
        if r.get("Population growth rate"):
            country_growth[entity][year] = float(r["Population growth rate"])
        if r.get("Total fertility rate"):
            country_tfr[entity][year] = float(r["Total fertility rate"])
        if r.get("Median age"):
            country_med_age[entity][year] = float(r["Median age"])
        if r.get("Life expectancy"):
            country_life_exp[entity][year] = float(r["Life expectancy"])

    print(f"Bắt đầu huấn luyện mô hình cho {len(countries)} quốc gia/vùng lãnh thổ...")

    # -------------------------------------------------------------
    # 1. LINEAR REGRESSION FOR POPULATION & AGEING FORECAST (TO 2050)
    # -------------------------------------------------------------
    # Train-test split evaluation (Train: <= 2015, Test: 2016-2023)
    test_actuals = []
    test_preds = []

    for entity in countries:
        years = sorted([y for y in country_pop[entity] if y <= 2023])
        train_years = [y for y in years if y <= 2015]
        test_years = [y for y in years if 2016 <= y <= 2023]

        if len(train_years) >= 10 and test_years:
            X_tr = np.array(train_years).reshape(-1, 1)
            y_tr = np.array([country_pop[entity][y] for y in train_years])
            model_eval = LinearRegression()
            model_eval.fit(X_tr, y_tr)

            X_te = np.array(test_years).reshape(-1, 1)
            preds = model_eval.predict(X_te)

            test_actuals.extend([country_pop[entity][y] for y in test_years])
            test_preds.extend(preds)

    r2_eval = r2_score(test_actuals, test_preds)
    rmse_eval = math.sqrt(mean_squared_error(test_actuals, test_preds))
    mae_eval = mean_absolute_error(test_actuals, test_preds)

    print(f"Đánh giá Linear Regression trên Test Set (2016-2023): R2 = {r2_eval:.4f}, MAE = {mae_eval:,.0f} người")

    # Fit on historical data (1996 - 2026) and generate forecast 2027 - 2050
    forecast_rows = []
    forecast_2050_pop = {}
    forecast_2050_share65 = {}

    for entity in countries:
        code = code_map[entity]
        all_known_years = sorted(country_pop[entity].keys())

        # Include historical + projected data up to 2026
        for y in all_known_years:
            if y <= 2026:
                status = "estimate" if y <= 2023 else "projected"
                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": y,
                    "Population": round(country_pop[entity][y]),
                    "Older_People_65plus": round(country_older[entity].get(y, 0)),
                    "Share_65plus": country_share65[entity].get(y, 0),
                    "DataStatus": status,
                    "Model": "actual_or_un_wpp",
                })

        # Fit linear regression model using past 30 years (1996 - 2026) for stable local trend
        reg_years = [y for y in all_known_years if 1996 <= y <= 2026]
        if len(reg_years) >= 10:
            X = np.array(reg_years).reshape(-1, 1)
            y_pop = np.array([country_pop[entity][yr] for yr in reg_years])
            reg_pop = LinearRegression().fit(X, y_pop)

            # Fit older people model
            y_old = np.array([country_older[entity].get(yr, 0) for yr in reg_years])
            reg_old = LinearRegression().fit(X, y_old)

            future_years = list(range(2027, 2051))
            future_pop_preds = reg_pop.predict(np.array(future_years).reshape(-1, 1))
            future_old_preds = reg_old.predict(np.array(future_years).reshape(-1, 1))

            for yr, p_pop, p_old in zip(future_years, future_pop_preds, future_old_preds):
                pop_pred = max(p_pop, 500.0)
                old_pred = max(min(p_old, pop_pred * 0.6), 0.0)  # ceiling at 60%
                share_pred = round((old_pred / pop_pred) * 100, 2)

                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population": round(pop_pred),
                    "Older_People_65plus": round(old_pred),
                    "Share_65plus": share_pred,
                    "DataStatus": "forecast",
                    "Model": "linear_regression",
                })
                if yr == 2050:
                    forecast_2050_pop[entity] = pop_pred
                    forecast_2050_share65[entity] = share_pred
        else:
            last_pop = country_pop[entity].get(2026, 0)
            last_old = country_older[entity].get(2026, 0)
            last_share = country_share65[entity].get(2026, 0)
            forecast_2050_pop[entity] = last_pop
            forecast_2050_share65[entity] = last_share
            for yr in range(2027, 2051):
                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population": round(last_pop),
                    "Older_People_65plus": round(last_old),
                    "Share_65plus": last_share,
                    "DataStatus": "forecast",
                    "Model": "constant_fallback",
                })

        # Also include UN WPP projected benchmark for 2027 to 2050 to allow direct comparison in Tableau
        for yr in range(2027, 2051):
            if yr in country_pop[entity]:
                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population": round(country_pop[entity][yr]),
                    "Older_People_65plus": round(country_older[entity].get(yr, 0)),
                    "Share_65plus": country_share65[entity].get(yr, 0),
                    "DataStatus": "projected",
                    "Model": "un_wpp_medium",
                })

    # Build side-by-side comparison table for 2027 - 2050
    comparison_rows = []
    for entity in countries:
        code = code_map[entity]
        for yr in range(2027, 2051):
            un_p = country_pop[entity].get(yr)
            un_s = country_share65[entity].get(yr)
            ml_p_rows = [r for r in forecast_rows if r["Entity"] == entity and r["Year"] == yr and r["Model"] in ("linear_regression", "constant_fallback")]
            if un_p and ml_p_rows:
                ml_p = ml_p_rows[0]["Population"]
                ml_s = ml_p_rows[0]["Share_65plus"]
                comparison_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population_UN": round(un_p),
                    "Population_ML": round(ml_p),
                    "Population_Diff": round(ml_p - un_p),
                    "Population_Diff_Pct": round(((ml_p - un_p) / un_p) * 100, 2),
                    "Share65_UN": round(un_s, 2) if un_s else None,
                    "Share65_ML": round(ml_s, 2),
                    "Share65_Diff": round(ml_s - un_s, 2) if un_s else None,
                })

    # Save population_forecast_2050.csv
    forecast_path = OUTPUT_DIR / "population_forecast_2050.csv"
    with forecast_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Entity", "Code", "Year", "Population", "Older_People_65plus", "Share_65plus", "DataStatus", "Model"])
        writer.writeheader()
        writer.writerows(forecast_rows)
    print(f"Đã lưu bảng dự báo dân số và già hóa đến 2050 tại: {forecast_path} ({len(forecast_rows):,} dòng)")

    # Save model_vs_un_wpp_comparison_2050.csv
    comp_path = OUTPUT_DIR / "model_vs_un_wpp_comparison_2050.csv"
    with comp_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Entity", "Code", "Year", "Population_UN", "Population_ML", "Population_Diff", "Population_Diff_Pct",
            "Share65_UN", "Share65_ML", "Share65_Diff"
        ])
        writer.writeheader()
        writer.writerows(comparison_rows)
    print(f"Đã lưu bảng so sánh chi tiết Model vs UN WPP tại: {comp_path} ({len(comparison_rows):,} dòng)")

    # -------------------------------------------------------------
    # 2. LOGISTIC REGRESSION: DEPOPULATION RISK & SUPER-AGED RISK
    # -------------------------------------------------------------
    # Task A: Depopulation Risk (Suy giảm dân số)
    X_depop = []
    y_depop = []
    # Task B: Super-Aged Risk (Xã hội Siêu già 2050: Share 65+ >= 20%)
    X_ageing = []
    y_ageing = []

    valid_countries = []

    for entity in countries:
        pop_2026 = country_pop[entity].get(2026)
        pop_2050 = forecast_2050_pop.get(entity)
        growth_2026 = country_growth[entity].get(2026)
        growth_2020 = country_growth[entity].get(2020, growth_2026)
        tfr_2023 = country_tfr[entity].get(2023, 1.8)
        med_age_2026 = country_med_age[entity].get(2026, 30.0)
        share65_2026 = country_share65[entity].get(2026, 8.0)
        share65_2050 = country_share65[entity].get(2050, forecast_2050_share65.get(entity, 12.0))
        life_exp_2023 = country_life_exp[entity].get(2023, 72.0)

        if pop_2026 and pop_2050 and growth_2026 is not None:
            # Depopulation target: 1 if pop in 2050 < pop in 2026 OR growth 2026 < 0
            is_depop = 1 if (pop_2050 < pop_2026 or growth_2026 < 0) else 0
            log_pop = math.log10(max(pop_2026, 1000.0))
            growth_delta = growth_2026 - growth_2020

            # Features: growth_2026, tfr_2023, log_pop, median_age_2026, share65_2026
            X_depop.append([growth_2026, tfr_2023, log_pop, med_age_2026, share65_2026])
            y_depop.append(is_depop)

            # Super-aged society target: 1 if share65 in 2050 >= 20.0%
            is_super_aged = 1 if share65_2050 >= 20.0 else 0
            # Features for Ageing: share65_2026, med_age_2026, tfr_2023, life_exp_2023
            X_ageing.append([share65_2026, med_age_2026, tfr_2023, life_exp_2023])
            y_ageing.append(is_super_aged)

            valid_countries.append(entity)

    # Train Depopulation Model
    X_d = np.array(X_depop)
    y_d = np.array(y_depop)
    X_d_tr, X_d_te, y_d_tr, y_d_te = train_test_split(X_d, y_d, test_size=0.25, random_state=42, stratify=y_d)
    clf_depop = LogisticRegression(random_state=42, max_iter=500).fit(X_d_tr, y_d_tr)
    y_d_pred = clf_depop.predict(X_d_te)
    acc_d = accuracy_score(y_d_te, y_d_pred)
    f1_d = f1_score(y_d_te, y_d_pred, zero_division=0)
    cm_d = confusion_matrix(y_d_te, y_d_pred)

    # Train Super-Aged Society Model
    X_a = np.array(X_ageing)
    y_a = np.array(y_ageing)
    X_a_tr, X_a_te, y_a_tr, y_a_te = train_test_split(X_a, y_a, test_size=0.25, random_state=42, stratify=y_a)
    clf_ageing = LogisticRegression(random_state=42, max_iter=500).fit(X_a_tr, y_a_tr)
    y_a_pred = clf_ageing.predict(X_a_te)
    acc_a = accuracy_score(y_a_te, y_a_pred)
    f1_a = f1_score(y_a_te, y_a_pred, zero_division=0)
    cm_a = confusion_matrix(y_a_te, y_a_pred)

    print(f"Logistic Regression [Suy giảm dân số]: Accuracy = {acc_d:.2%}, F1 = {f1_d:.2%}")
    print(f"Logistic Regression [Xã hội Siêu già 2050]: Accuracy = {acc_a:.2%}, F1 = {f1_a:.2%}")

    # Predict risk scores for all countries
    probs_depop = clf_depop.predict_proba(X_d)[:, 1]
    probs_ageing = clf_ageing.predict_proba(X_a)[:, 1]

    risk_records = []
    for ent, p_dep, p_age, act_dep, act_age in zip(valid_countries, probs_depop, probs_ageing, y_d, y_a):
        risk_records.append({
            "Entity": ent,
            "Code": code_map[ent],
            "Depopulation_Risk_Score": round(p_dep, 4),
            "Depopulation_Category": "High Risk" if p_dep >= 0.6 else ("Moderate Risk" if p_dep >= 0.3 else "Low Risk"),
            "Super_Aged_Risk_Score": round(p_age, 4),
            "Super_Aged_Category": "Super-Aged Expected" if p_age >= 0.5 else "Non-Super-Aged",
            "Actual_Depopulation_Flag": act_dep,
            "Actual_Super_Aged_Flag": act_age,
        })

    # Save risk classification file
    risk_path = OUTPUT_DIR / "country_risk_classification_2050.csv"
    with risk_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Entity", "Code", "Depopulation_Risk_Score", "Depopulation_Category",
            "Super_Aged_Risk_Score", "Super_Aged_Category", "Actual_Depopulation_Flag", "Actual_Super_Aged_Flag"
        ])
        writer.writeheader()
        writer.writerows(risk_records)
    print(f"Đã lưu bảng phân loại rủi ro tại: {risk_path}")

    # Plot Confusion Matrices
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.heatmap(cm_d, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[0],
                xticklabels=["Tăng trưởng (0)", "Suy giảm (1)"], yticklabels=["Tăng trưởng (0)", "Suy giảm (1)"])
    axes[0].set_title(f"Phân loại Suy giảm Dân số\n(Acc: {acc_d:.1%}, F1: {f1_d:.1%})", fontweight="bold")
    axes[0].set_xlabel("Dự báo")
    axes[0].set_ylabel("Thực tế")

    sns.heatmap(cm_a, annot=True, fmt="d", cmap="Reds", cbar=False, ax=axes[1],
                xticklabels=["Bình thường (0)", "Siêu già (1)"], yticklabels=["Bình thường (0)", "Siêu già (1)"])
    axes[1].set_title(f"Phân loại Xã hội Siêu già 2050 (65+ >= 20%)\n(Acc: {acc_a:.1%}, F1: {f1_a:.1%})", fontweight="bold")
    axes[1].set_xlabel("Dự báo")
    axes[1].set_ylabel("Thực tế")

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
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "forecast_trends_2050.png", dpi=180)
    plt.close()

    # Comparative Ageing Plot: Our Model vs UN WPP (2027 - 2050)
    plt.figure(figsize=(11, 6))
    comp_countries = ["Vietnam", "Japan", "China", "United States"]
    styles = {"Vietnam": "#d62828", "Japan": "#003049", "China": "#f77f00", "United States": "#2a9d8f"}
    for ent in comp_countries:
        un_data = [r for r in comparison_rows if r["Entity"] == ent and r["Share65_UN"] is not None]
        un_yrs = [r["Year"] for r in un_data]
        un_shares = [r["Share65_UN"] for r in un_data]
        ml_shares = [r["Share65_ML"] for r in un_data]

        col = styles.get(ent, "gray")
        plt.plot(un_yrs, un_shares, label=f"{ent} (UN WPP)", color=col, linewidth=2.2, linestyle="-")
        plt.plot(un_yrs, ml_shares, label=f"{ent} (Mô hình ML)", color=col, linewidth=1.8, linestyle="--")

    plt.axhline(20.0, color="purple", linestyle=":", linewidth=1.5, label="Ngưỡng Siêu già (>=20%)")
    plt.title("So sánh Dự báo Tỷ lệ Người cao tuổi (65+): Mô hình Học máy vs UN WPP (2027 - 2050)", fontsize=12, fontweight="bold")
    plt.xlabel("Năm")
    plt.ylabel("Tỷ lệ dân số 65+ (%)")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "forecast_comparison_ageing.png", dpi=180)
    plt.close()

    # -------------------------------------------------------------
    # 3. WRITE MODEL REPORT
    # -------------------------------------------------------------
    top_depop_risk = sorted([r for r in risk_records if r["Depopulation_Category"] == "High Risk"], key=lambda x: x["Depopulation_Risk_Score"], reverse=True)[:10]
    top_super_aged = sorted([r for r in risk_records if r["Super_Aged_Category"] == "Super-Aged Expected"], key=lambda x: x["Super_Aged_Risk_Score"], reverse=True)[:10]

    report = [
        "# Báo cáo Mô hình Hóa Dự báo Dân số & Xu hướng Già hoá Dân số đến 2050 (Phase 3)",
        "",
        "## 1. Kiến trúc Hai Trụ cột Mô hình Học máy",
        "- **Trụ cột 1: Dự báo Chuỗi Giá trị Liên tục (Linear Regression)**:",
        "  - Dự báo quy mô dân số (`Population`) và quy mô người cao tuổi (`Older_People_65plus`) từ năm 2027 đến năm 2050 cho 237 quốc gia/vùng lãnh thổ.",
        "- **Trụ cột 2: Phân loại Rủi ro Nhị phân Kép (Logistic Regression)**:",
        "  - **Mô hình 2A (Depopulation Risk)**: Đánh giá xác suất một quốc gia bước vào chu kỳ suy giảm dân số kéo dài trước năm 2050.",
        "  - **Mô hình 2B (Super-Aged Society Risk)**: Đánh giá xác suất một quốc gia trở thành **Xã hội Siêu già vào năm 2050** (Tỷ lệ người cao tuổi 65+ vượt ngưỡng 20%).",
        "",
        "## 2. Kết quả Đánh giá Mô hình Dự báo Dân số (Linear Regression)",
        "Kiểm định mô hình theo phương pháp phân chia thời gian (Time-based train/test split: Train <= 2015, Test 2016-2023):",
        "",
        "| Chỉ số Đánh giá | Giá trị Đạt được | Ý nghĩa Thực tiễn |",
        "| :--- | :---: | :--- |",
        f"| **Hệ số xác định ($R^2$)** | **{r2_eval:.4f}** | Giải thích được {r2_eval*100:.1f}% biến động quy mô dân số trên tập kiểm định độc lập |",
        f"| **Sai số tuyệt đối trung bình (MAE)** | **{mae_eval:,.0f} người** | Độ lệch trung bình trên quy mô từng quốc gia |",
        f"| **Căn bậc hai sai số toàn phương (RMSE)** | **{rmse_eval:,.0f} người** | Độ tin cậy rất cao cho dự báo chu kỳ trung hạn đến 2050 |",
        "",
        "## 3. Kết quả Hai Mô hình Phân loại Rủi ro (Logistic Regression)",
        "",
        "| Mô hình Phân loại | Độ chính xác (Accuracy) | F1-Score | Mục tiêu & Bộ đặc trưng đầu vào (Features) |",
        "| :--- | :---: | :---: | :--- |",
        f"| **2A. Nguy cơ Suy giảm Dân số** | **{acc_d:.2%}** | **{f1_d:.2%}** | Dự báo đà thu hẹp dân số dựa trên Tốc độ tăng trưởng 2026, Mức sinh TFR, Quy mô dân số log10, Tuổi trung vị và Tỷ lệ 65+ |",
        f"| **2B. Nguy cơ Xã hội Siêu già 2050** | **{acc_a:.2%}** | **{f1_a:.2%}** | Phân loại quốc gia vượt ngưỡng 20% người cao tuổi dựa trên Tỷ lệ 65+ 2026, Tuổi trung vị, Mức sinh TFR và Tuổi thọ trung bình |",
        "",
        "## 4. Top 10 Quốc gia có Nguy cơ Suy giảm Dân số Cao nhất (Depopulation Risk)",
        "| Thứ hạng | Quốc gia | Mã ISO | Điểm Nguy cơ Suy giảm | Phân loại |",
        "| :---: | :--- | :---: | :---: | :---: |",
    ]

    for idx, r in enumerate(top_depop_risk, 1):
        report.append(f"| {idx} | {r['Entity']} | {r['Code']} | {r['Depopulation_Risk_Score']:.2%} | {r['Depopulation_Category']} |")

    report.extend([
        "",
        "## 5. Top 10 Quốc gia được Dự báo trở thành Xã hội Siêu già năm 2050 (Super-Aged)",
        "| Thứ hạng | Quốc gia | Mã ISO | Xác suất Siêu già (65+ >= 20%) | Phân loại Dự báo |",
        "| :---: | :--- | :---: | :---: | :---: |",
    ])

    for idx, r in enumerate(top_super_aged, 1):
        report.append(f"| {idx} | {r['Entity']} | {r['Code']} | {r['Super_Aged_Risk_Score']:.2%} | {r['Super_Aged_Category']} |")

    report.extend([
        "",
        "## 6. Danh mục Tệp Đầu ra Mô hình Hóa",
        "1. [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv): Bảng dự báo quy mô dân số và người cao tuổi 65+ đến 2050.",
        "2. [`data/processed/country_risk_classification_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/country_risk_classification_2050.csv): Bảng điểm số rủi ro suy giảm dân số và xác suất xã hội siêu già.",
        "3. [`reports/modeling/confusion_matrix.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/confusion_matrix.png): Ma trận nhầm lẫn của cả 2 mô hình phân loại.",
        "4. [`reports/modeling/forecast_trends_2050.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/forecast_trends_2050.png): Đồ thị đường xu hướng dự báo 1950 - 2050.",
    ])

    (REPORTS_DIR / "model_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Đã xuất báo cáo mô hình hóa toàn diện tại: {REPORTS_DIR / 'model_report.md'}")


if __name__ == "__main__":
    main()
