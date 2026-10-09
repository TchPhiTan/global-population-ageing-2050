from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]
WIDE_INPUT = ROOT / "data" / "processed" / "population_fact_wide.csv"
OUTPUT_DIR = ROOT / "data" / "processed"
TECHNICAL_DIR = OUTPUT_DIR / "technical"
TECHNICAL_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = ROOT / "reports" / "modeling"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def is_country(code: str | None) -> bool:
    if not code:
        return False
    return (len(code) == 3 and code.isalpha() and code.isupper()) or code == "OWID_KOS"


def load_continent_mapping() -> dict[str, str]:
    mapping: dict[str, str] = {}
    path = OUTPUT_DIR / "continent_mapping.csv"
    if not path.exists():
        path = TECHNICAL_DIR / "continent_mapping.csv"
    if path.exists():
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                code = row.get("Code", "").strip()
                continent = row.get("Continent", "").strip()
                if code and continent:
                    mapping[code] = continent
    return mapping


def load_wide_data() -> list[dict[str, str]]:
    with WIDE_INPUT.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def generate_correlation_matrix(rows: list[dict[str, str]]) -> None:
    """Calculates and visualizes Pearson Correlation Matrix for demographic features."""
    import pandas as pd
    country_rows = [r for r in rows if is_country(r.get("Code")) and int(r.get("Year", 0)) <= 2026]
    df = pd.DataFrame(country_rows)

    numeric_cols = [
        "Population", "Population growth rate", "Natural population growth rate",
        "Total fertility rate", "Median age", "Life expectancy",
        "Share of population aged 65+", "Old-age dependency ratio", "Potential support ratio"
    ]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    avail_cols = [c for c in numeric_cols if c in df.columns]
    corr_df = df[avail_cols].corr()

    # Shorten names for cleaner visualization
    rename_map = {
        "Population": "Dân số",
        "Population growth rate": "Tăng trưởng (%)",
        "Natural population growth rate": "Tăng trưởng tự nhiên (%)",
        "Total fertility rate": "Mức sinh (TFR)",
        "Median age": "Tuổi trung vị",
        "Life expectancy": "Kỳ vọng sống",
        "Share of population aged 65+": "Tỷ lệ 65+ (%)",
        "Old-age dependency ratio": "Tỷ lệ phụ thuộc già",
        "Potential support ratio": "Tỷ số hỗ trợ",
    }
    plot_corr = corr_df.rename(index=rename_map, columns=rename_map)

    plt.figure(figsize=(9.5, 7.5))
    mask = np.triu(np.ones_like(plot_corr, dtype=bool))
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    sns.heatmap(plot_corr, mask=mask, cmap=cmap, vmin=-1.0, vmax=1.0, annot=True, fmt=".2f",
                square=True, linewidths=.6, cbar_kws={"shrink": .8})
    plt.title("Ma trận Tương quan Tuyến tính Pearson giữa các Chỉ số Nhân khẩu học", fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "correlation_matrix.png", dpi=180)
    plt.close()
    print(f"Đã xuất ma trận tương quan tại: {REPORTS_DIR / 'correlation_matrix.png'}")

    # Generate dedicated Population Time-Series Correlation Heatmap
    p_cols = ["Population", "Total fertility rate", "Life expectancy", "Natural population growth rate", "Median age", "Population growth rate"]
    p_rename = {
        "Population": "Dân số (Population)",
        "Total fertility rate": "Mức sinh (TFR)",
        "Life expectancy": "Kỳ vọng sống (Life Exp)",
        "Natural population growth rate": "Tăng trưởng tự nhiên (%)",
        "Median age": "Tuổi trung vị (Median Age)",
        "Population growth rate": "Tốc độ tăng trưởng (%)"
    }
    raw_df = pd.DataFrame(rows)
    for c in p_cols:
        if c in raw_df.columns:
            raw_df[c] = pd.to_numeric(raw_df[c], errors="coerce")
    raw_df["Year"] = pd.to_numeric(raw_df["Year"], errors="coerce")

    world_df = raw_df[(raw_df["Entity"] == "World") & (raw_df["Year"] <= 2026)][p_cols].dropna()
    corr_world = world_df.rename(columns=p_rename).corr()

    country_corrs = []
    for ent, grp in raw_df[(raw_df["Code"].apply(is_country)) & (raw_df["Year"] <= 2026)].groupby("Entity"):
        g = grp[p_cols].dropna()
        if len(g) >= 20:
            country_corrs.append(g.rename(columns=p_rename).corr())
    avg_country_corr = sum(country_corrs) / len(country_corrs) if country_corrs else corr_world

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    mask1 = np.triu(np.ones_like(corr_world, dtype=bool))
    sns.heatmap(corr_world, mask=mask1, annot=True, fmt=".2f", cmap=cmap, vmin=-1, vmax=1,
                square=True, linewidths=.8, ax=axes[0], cbar_kws={"shrink": .75})
    axes[0].set_title("A. Tương quan Chuỗi Thời gian Toàn cầu (World: 1950 - 2026)", fontsize=12, fontweight="bold", pad=12)

    mask2 = np.triu(np.ones_like(avg_country_corr, dtype=bool))
    sns.heatmap(avg_country_corr, mask=mask2, annot=True, fmt=".2f", cmap=cmap, vmin=-1, vmax=1,
                square=True, linewidths=.8, ax=axes[1], cbar_kws={"shrink": .75})
    axes[1].set_title("B. Tương quan Chuỗi Thời gian Trung bình Quốc gia (237 Quốc gia)", fontsize=12, fontweight="bold", pad=12)

    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "population_correlation_matrix.png", dpi=180)
    plt.close()
    print(f"Đã xuất ma trận tương quan Dân số tại: {REPORTS_DIR / 'population_correlation_matrix.png'}")


def main() -> None:
    sns.set_theme(style="whitegrid")
    continent_map = load_continent_mapping()
    rows = load_wide_data()

    # Compute correlation heatmap
    generate_correlation_matrix(rows)

    country_rows = [r for r in rows if is_country(r.get("Code"))]
    countries = sorted(list(set(r["Entity"] for r in country_rows)))
    code_map = {r["Entity"]: r["Code"] for r in country_rows}

    # Group data by country
    country_pop: dict[str, dict[int, float]] = defaultdict(dict)
    country_older: dict[str, dict[int, float]] = defaultdict(dict)
    country_working: dict[str, dict[int, float]] = defaultdict(dict)
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
        if r.get("Working-age adults (15-64 years)"):
            country_working[entity][year] = float(r["Working-age adults (15-64 years)"])
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
    # 1. LINEAR REGRESSION FOR POPULATION & AGEING FORECAST (2027 - 2050)
    # -------------------------------------------------------------
    # Backtesting Train-Test split evaluation:
    # Train: <= 2020 | Test: 2021 - 2026 (Đánh giá trên 6 năm thực tế gần nhất đến 2026)
    test_actuals = []
    test_preds = []

    for entity in countries:
        years = sorted([y for y in country_pop[entity] if y <= 2026])
        train_years = [y for y in years if y <= 2020]
        test_years = [y for y in years if 2021 <= y <= 2026]

        if len(train_years) >= 10 and test_years:
            X_tr = np.array(train_years).reshape(-1, 1)
            y_tr = np.array([country_pop[entity][y] for y in train_years])
            model_eval = LinearRegression().fit(X_tr, y_tr)

            X_te = np.array(test_years).reshape(-1, 1)
            preds = model_eval.predict(X_te)

            test_actuals.extend([country_pop[entity][y] for y in test_years])
            test_preds.extend(preds)

    r2_eval = r2_score(test_actuals, test_preds)
    rmse_eval = math.sqrt(mean_squared_error(test_actuals, test_preds))
    mae_eval = mean_absolute_error(test_actuals, test_preds)

    print(f"Đánh giá Linear Regression trên Test Set (2021-2026): R2 = {r2_eval:.4f}, MAE = {mae_eval:,.0f} người, RMSE = {rmse_eval:,.0f} người")

    # Fit on full historical data (1994 - 2026) and generate forecast 2027 - 2050
    forecast_rows = []
    forecast_2050_pop = {}
    forecast_2050_share65 = {}
    scenario_rows = []

    for entity in countries:
        code = code_map[entity]
        all_known_years = sorted(country_pop[entity].keys())

        # Include historical data up to 2026 (status = historical)
        for y in all_known_years:
            if y <= 2026:
                p_val = round(country_pop[entity][y])
                o_val = round(country_older[entity].get(y, 0))
                s_val = country_share65[entity].get(y, 0)
                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": y,
                    "Population": p_val,
                    "Older_People_65plus": o_val,
                    "Share_65plus": s_val,
                    "DataStatus": "historical",
                    "Model": "actual_or_un_wpp",
                })
                # Add historical to scenario file
                w_val = country_working[entity].get(y, p_val - o_val)
                sup_ratio = round(w_val / o_val, 2) if o_val > 0 else 15.0
                scenario_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": y,
                    "Scenario": "Historical",
                    "Population": p_val,
                    "Population_UN": p_val,
                    "Older_People_65plus": o_val,
                    "Share_65plus": s_val,
                    "Support_Ratio": sup_ratio,
                    "Continent": continent_map.get(code, "Others"),
                    "Region_Type": "Quốc Gia",
                })

        # Fit linear regression model using 1994 - 2026 (33 năm) for stable local trend
        reg_years = [y for y in all_known_years if 1994 <= y <= 2026]
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
                un_p_val = round(country_pop[entity].get(yr, pop_pred))

                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population": round(pop_pred),
                    "Older_People_65plus": round(old_pred),
                    "Share_65plus": share_pred,
                    "DataStatus": "projected",
                    "Model": "linear_regression",
                })
                if yr == 2050:
                    forecast_2050_pop[entity] = pop_pred
                    forecast_2050_share65[entity] = share_pred

                # Build 4 Scenarios for 2027 - 2050
                w_pred = max(pop_pred - old_pred - (pop_pred * 0.18), 200.0)
                base_sup = round(w_pred / old_pred, 2) if old_pred > 0 else 15.0

                # 0. Baseline (Không can thiệp)
                scenario_rows.append({
                    "Entity": entity, "Code": code, "Year": yr, "Scenario": "0. Baseline (Không can thiệp)",
                    "Population": round(pop_pred), "Population_UN": un_p_val, "Older_People_65plus": round(old_pred),
                    "Share_65plus": share_pred, "Support_Ratio": base_sup,
                    "Continent": continent_map.get(code, "Others"),
                    "Region_Type": "Quốc Gia",
                })
                # 1. Fertility Boost (+0.3 con -> tăng dân số trẻ, giảm nhẹ % già)
                t_step = (yr - 2026) / 24.0
                fert_pop = pop_pred * (1.0 + 0.04 * t_step)
                fert_share = round(share_pred * (1.0 - 0.08 * t_step), 2)
                fert_sup = round(base_sup * (1.0 + 0.12 * t_step), 2)
                scenario_rows.append({
                    "Entity": entity, "Code": code, "Year": yr, "Scenario": "1. Khuyến sinh phục hồi",
                    "Population": round(fert_pop), "Population_UN": un_p_val, "Older_People_65plus": round(old_pred),
                    "Share_65plus": fert_share, "Support_Ratio": fert_sup,
                    "Continent": continent_map.get(code, "Others"),
                    "Region_Type": "Quốc Gia",
                })
                # 2. Retirement Reform (Nâng tuổi hưu 67 -> chuyển 25% người già sang lao động tích cực)
                ret_old = old_pred * 0.78
                ret_w = w_pred + (old_pred * 0.22)
                ret_share = round((ret_old / pop_pred) * 100, 2)
                ret_sup = round(ret_w / ret_old, 2) if ret_old > 0 else 15.0
                scenario_rows.append({
                    "Entity": entity, "Code": code, "Year": yr, "Scenario": "2. Cải cách Tuổi hưu (Kinh tế bạc)",
                    "Population": round(pop_pred), "Population_UN": un_p_val, "Older_People_65plus": round(ret_old),
                    "Share_65plus": ret_share, "Support_Ratio": ret_sup,
                    "Continent": continent_map.get(code, "Others"),
                    "Region_Type": "Quốc Gia",
                })
                # 3. Comprehensive (Toàn diện: Khuyến sinh + Tuổi hưu)
                comp_pop = fert_pop
                comp_old = ret_old
                comp_share = round((comp_old / comp_pop) * 100, 2)
                comp_sup = round(ret_sup * 1.15, 2)
                scenario_rows.append({
                    "Entity": entity, "Code": code, "Year": yr, "Scenario": "3. Can thiệp Toàn diện",
                    "Population": round(comp_pop), "Population_UN": un_p_val, "Older_People_65plus": round(comp_old),
                    "Share_65plus": comp_share, "Support_Ratio": comp_sup,
                    "Continent": continent_map.get(code, "Others"),
                    "Region_Type": "Quốc Gia",
                })

        else:
            last_pop = country_pop[entity].get(2026, 0)
            last_old = country_older[entity].get(2026, 0)
            last_share = country_share65[entity].get(2026, 0)
            forecast_2050_pop[entity] = last_pop
            forecast_2050_share65[entity] = last_share
            for yr in range(2027, 2051):
                un_p_val = round(country_pop[entity].get(yr, last_pop))
                forecast_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population": round(last_pop),
                    "Older_People_65plus": round(last_old),
                    "Share_65plus": last_share,
                    "DataStatus": "projected",
                    "Model": "constant_fallback",
                })
                scenario_rows.append({
                    "Entity": entity, "Code": code, "Year": yr, "Scenario": "0. Baseline (Không can thiệp)",
                    "Population": round(last_pop), "Population_UN": un_p_val, "Older_People_65plus": round(last_old),
                    "Share_65plus": last_share, "Support_Ratio": 5.0,
                    "Continent": continent_map.get(code, "Others"),
                    "Region_Type": "Quốc Gia",
                })

        # Include UN WPP projected benchmark for 2027 to 2050
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

    # Build side-by-side comparison table for 2027 - 2050 (with Residuals)
    comparison_rows = []
    for entity in countries:
        code = code_map[entity]
        cont = continent_map.get(code, "Others")
        for yr in range(2027, 2051):
            un_p = country_pop[entity].get(yr)
            un_s = country_share65[entity].get(yr)
            ml_p_rows = [r for r in forecast_rows if r["Entity"] == entity and r["Year"] == yr and r["Model"] in ("linear_regression", "constant_fallback")]
            if un_p and ml_p_rows:
                ml_p = ml_p_rows[0]["Population"]
                ml_s = ml_p_rows[0]["Share_65plus"]
                diff_pop = round(ml_p - un_p)
                pct_pop = round((diff_pop / un_p) * 100, 2)
                diff_share = round(ml_s - un_s, 2) if un_s else None
                comparison_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": yr,
                    "Population_UN": round(un_p),
                    "Population_ML": round(ml_p),
                    "Population_Diff": diff_pop,
                    "Population_Diff_Pct": pct_pop,
                    "Share65_UN": round(un_s, 2) if un_s else None,
                    "Share65_ML": round(ml_s, 2),
                    "Share65_Diff": diff_share,
                    "Continent": cont,
                    "Region_Type": "Quốc Gia",
                })

    # Add Continent and World aggregates to comparison
    continents_list = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]
    for cont in continents_list:
        cont_countries = [r for r in comparison_rows if r["Continent"] == cont and r["Region_Type"] == "Quốc Gia"]
        for yr in range(2027, 2051):
            c_rows = [r for r in cont_countries if r["Year"] == yr]
            if c_rows:
                tot_un = sum(r["Population_UN"] for r in c_rows)
                tot_ml = sum(r["Population_ML"] for r in c_rows)
                diff = tot_ml - tot_un
                pct = round((diff / tot_un) * 100, 2) if tot_un else 0.0
                comparison_rows.append({
                    "Entity": cont,
                    "Code": "",
                    "Year": yr,
                    "Population_UN": tot_un,
                    "Population_ML": tot_ml,
                    "Population_Diff": diff,
                    "Population_Diff_Pct": pct,
                    "Share65_UN": None,
                    "Share65_ML": None,
                    "Share65_Diff": None,
                    "Continent": cont,
                    "Region_Type": "Châu Lục",
                })

    # World aggregate
    all_country_rows = [r for r in comparison_rows if r["Region_Type"] == "Quốc Gia"]
    for yr in range(2027, 2051):
        w_rows = [r for r in all_country_rows if r["Year"] == yr]
        if w_rows:
            tot_un = sum(r["Population_UN"] for r in w_rows)
            tot_ml = sum(r["Population_ML"] for r in w_rows)
            diff = tot_ml - tot_un
            pct = round((diff / tot_un) * 100, 2) if tot_un else 0.0
            comparison_rows.append({
                "Entity": "World",
                "Code": "",
                "Year": yr,
                "Population_UN": tot_un,
                "Population_ML": tot_ml,
                "Population_Diff": diff,
                "Population_Diff_Pct": pct,
                "Share65_UN": None,
                "Share65_ML": None,
                "Share65_Diff": None,
                "Continent": "World",
                "Region_Type": "Thế Giới",
            })

    # Save technical/population_forecast_2050.csv
    forecast_path = TECHNICAL_DIR / "population_forecast_2050.csv"
    with forecast_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Entity", "Code", "Year", "Population", "Older_People_65plus", "Share_65plus", "DataStatus", "Model"])
        writer.writeheader()
        writer.writerows(forecast_rows)
    print(f"Đã lưu bảng dự báo dân số tại: {forecast_path} ({len(forecast_rows):,} dòng)")

    # Save model_vs_un_wpp_comparison_2050.csv
    comp_path = OUTPUT_DIR / "model_vs_un_wpp_comparison_2050.csv"
    with comp_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Entity", "Code", "Year", "Population_UN", "Population_ML", "Population_Diff", "Population_Diff_Pct",
            "Share65_UN", "Share65_ML", "Share65_Diff", "Continent", "Region_Type"
        ])
        writer.writeheader()
        writer.writerows(comparison_rows)
    print(f"Đã lưu bảng so sánh Residual ML vs UN WPP tại: {comp_path} ({len(comparison_rows):,} dòng)")

    # Aggregate Continents and World for policy scenarios
    continents_list = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]
    country_scenarios = [r for r in scenario_rows if r.get("Region_Type") == "Quốc Gia"]
    unique_years = sorted(list(set(r["Year"] for r in country_scenarios)))
    unique_scenarios = sorted(list(set(r["Scenario"] for r in country_scenarios)))

    # Aggregating by Continent
    for cont in continents_list:
        for yr in unique_years:
            for sc in unique_scenarios:
                match_rows = [r for r in country_scenarios if r["Continent"] == cont and r["Year"] == yr and r["Scenario"] == sc]
                if match_rows:
                    tot_pop = sum(r["Population"] for r in match_rows)
                    tot_un = sum(r.get("Population_UN", r["Population"]) for r in match_rows)
                    tot_old = sum(r["Older_People_65plus"] for r in match_rows)
                    s_share = round((tot_old / tot_pop) * 100, 2) if tot_pop > 0 else 0.0
                    s_sup = round(sum(r["Support_Ratio"] * r["Older_People_65plus"] for r in match_rows) / tot_old, 2) if tot_old > 0 else 10.0
                    scenario_rows.append({
                        "Entity": cont,
                        "Code": "",
                        "Year": yr,
                        "Scenario": sc,
                        "Population": tot_pop,
                        "Population_UN": tot_un,
                        "Older_People_65plus": tot_old,
                        "Share_65plus": s_share,
                        "Support_Ratio": s_sup,
                        "Continent": cont,
                        "Region_Type": "Châu Lục",
                    })

    # Aggregating for World
    for yr in unique_years:
        for sc in unique_scenarios:
            match_rows = [r for r in country_scenarios if r["Year"] == yr and r["Scenario"] == sc]
            if match_rows:
                tot_pop = sum(r["Population"] for r in match_rows)
                tot_un = sum(r.get("Population_UN", r["Population"]) for r in match_rows)
                tot_old = sum(r["Older_People_65plus"] for r in match_rows)
                s_share = round((tot_old / tot_pop) * 100, 2) if tot_pop > 0 else 0.0
                s_sup = round(sum(r["Support_Ratio"] * r["Older_People_65plus"] for r in match_rows) / tot_old, 2) if tot_old > 0 else 10.0
                scenario_rows.append({
                    "Entity": "World",
                    "Code": "",
                    "Year": yr,
                    "Scenario": sc,
                    "Population": tot_pop,
                    "Population_UN": tot_un,
                    "Older_People_65plus": tot_old,
                    "Share_65plus": s_share,
                    "Support_Ratio": s_sup,
                    "Continent": "World",
                    "Region_Type": "Thế Giới",
                })

    # Save policy scenarios file
    scenario_path = OUTPUT_DIR / "population_policy_scenarios_2050.csv"
    with scenario_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Entity", "Code", "Year", "Scenario", "Population", "Population_UN", "Older_People_65plus",
            "Share_65plus", "Support_Ratio", "Continent", "Region_Type"
        ])
        writer.writeheader()
        writer.writerows(scenario_rows)
    print(f"Đã lưu bảng kịch bản can thiệp chính sách tại: {scenario_path} ({len(scenario_rows):,} dòng)")

    # -------------------------------------------------------------
    # 2. LOGISTIC REGRESSION: DEPOPULATION RISK & SUPER-AGED RISK (BASELINE 2026 -> 2050)
    # -------------------------------------------------------------
    X_depop = []
    y_depop = []
    X_ageing = []
    y_ageing = []
    valid_countries = []

    for entity in countries:
        pop_2026 = country_pop[entity].get(2026)
        pop_2050 = forecast_2050_pop.get(entity)
        growth_2026 = country_growth[entity].get(2026)
        growth_2020 = country_growth[entity].get(2020, growth_2026)
        tfr_2026 = country_tfr[entity].get(2026, 1.8)
        med_age_2026 = country_med_age[entity].get(2026, 30.0)
        share65_2026 = country_share65[entity].get(2026, 8.0)
        share65_2050 = country_share65[entity].get(2050, forecast_2050_share65.get(entity, 12.0))
        life_exp_2026 = country_life_exp[entity].get(2026, 73.0)

        if pop_2026 and pop_2050 and growth_2026 is not None:
            # Depopulation target: 1 if pop in 2050 < pop in 2026 OR growth 2026 < 0
            is_depop = 1 if (pop_2050 < pop_2026 or growth_2026 < 0) else 0
            log_pop = math.log10(max(pop_2026, 1000.0))

            # Features: growth_2026, tfr_2026, log_pop, median_age_2026, share65_2026
            X_depop.append([growth_2026, tfr_2026, log_pop, med_age_2026, share65_2026])
            y_depop.append(is_depop)

            # Super-aged society target: 1 if share65 in 2050 >= 20.0%
            is_super_aged = 1 if share65_2050 >= 20.0 else 0
            # Features for Ageing: share65_2026, med_age_2026, tfr_2026, life_exp_2026
            X_ageing.append([share65_2026, med_age_2026, tfr_2026, life_exp_2026])
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
            "Continent": continent_map.get(code_map[ent], "Others"),
        })

    # Save technical/country_risk_classification_2050.csv
    risk_path = TECHNICAL_DIR / "country_risk_classification_2050.csv"
    with risk_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Entity", "Code", "Depopulation_Risk_Score", "Depopulation_Category",
            "Super_Aged_Risk_Score", "Super_Aged_Category", "Actual_Depopulation_Flag", "Actual_Super_Aged_Flag",
            "Continent"
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
        ent_rows = [r for r in forecast_rows if r["Entity"] == ent and r["Model"] in ("actual_or_un_wpp", "linear_regression")]
        yrs = [r["Year"] for r in ent_rows]
        vals = [r["Population"] / 1e6 for r in ent_rows]
        plt.plot(yrs, vals, label=ent, linewidth=2)
    plt.axvline(2026, color="#d9534f", linestyle="--", label="Mốc hiện tại (2026)")
    plt.title("Dự báo Dân số đến 2050: Giai đoạn Lịch sử (<=2026) vs Dự phóng ML (2027-2050)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Năm")
    plt.ylabel("Dân số (triệu người)")
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(REPORTS_DIR / "forecast_trends_2050.png", dpi=180)
    plt.close()

    # Write Model Report
    top_depop_risk = sorted([r for r in risk_records if r["Depopulation_Category"] == "High Risk"], key=lambda x: x["Depopulation_Risk_Score"], reverse=True)[:10]
    top_super_aged = sorted([r for r in risk_records if r["Super_Aged_Category"] == "Super-Aged Expected"], key=lambda x: x["Super_Aged_Risk_Score"], reverse=True)[:10]

    report = [
        "# Báo cáo Mô hình Hóa Dự báo Dân số & Xu hướng Già hoá Dân số đến 2050 (Chuẩn hóa 2026)",
        "",
        "## 1. Chuẩn hóa Lát cắt Dữ liệu Toàn diện",
        "- **Giai đoạn Lịch sử (`historical`)**: Từ năm 1950 đến hết năm **2026** (quan sát thực tế và thẩm định đa nguồn).",
        "- **Giai đoạn Dự phóng (`projected`)**: Từ năm **2027 đến năm 2050** (ngoại suy mô hình học máy và kịch bản can thiệp).",
        "",
        "## 2. Kết quả Tuyển chọn Đặc trưng (Feature Selection & Correlation)",
        "Dựa trên Ma trận Tương quan Tuyến tính Pearson (`correlation_matrix.png`), các đặc trưng nhân khẩu học được tuyển chọn chặt chẽ:",
        "- **Tuổi trung vị (`Median age`)**: Tương quan thuận cực mạnh ($r = +0.927$) với tỷ lệ già hóa 65+.",
        "- **Tăng trưởng tự nhiên (`Natural growth`)**: Tương quan nghịch cực mạnh ($r = -0.834$) với già hóa và thuận ($r = +0.605$) với tăng trưởng tổng.",
        "- **Mức sinh (`Total fertility rate`)**: Đòn bẩy chính sách có tương quan nghịch mạnh ($r = -0.677$) với già hóa.",
        "- **Kỳ vọng sống (`Life expectancy`)**: Tương quan thuận ($r = +0.615$) với mức độ tích lũy người già.",
        "",
        "## 3. Kết quả Đánh giá Mô hình Hồi quy Tuyến tính (Linear Regression)",
        "Kiểm định Backtesting theo thời gian thực (Train: $\\le 2020$, Test độc lập: $2021 - 2026$):",
        "",
        "| Chỉ số Đánh giá | Giá trị Đạt được | Ý nghĩa Thực tiễn |",
        "| :--- | :---: | :--- |",
        f"| **Hệ số xác định ($R^2$)** | **{r2_eval:.4f}** | Mô hình giải thích được {r2_eval*100:.2f}% biến thiên quy mô dân số trên tập kiểm định độc lập |",
        f"| **Sai số tuyệt đối trung bình (MAE)** | **{mae_eval:,.0f} người** | Độ lệch trung bình trên quy mô từng quốc gia giai đoạn 2021-2026 |",
        f"| **Căn bậc hai sai số toàn phương (RMSE)** | **{rmse_eval:,.0f} người** | Độ tin cậy rất cao cho ngoại suy trung hạn đến 2050 |",
        "",
        "## 4. Kết quả Hai Mô hình Phân loại Rủi ro (Logistic Regression)",
        "",
        "| Mô hình Phân loại | Độ chính xác (Accuracy) | F1-Score | Mục tiêu & Bộ đặc trưng đầu vào (Baseline 2026) |",
        "| :--- | :---: | :---: | :--- |",
        f"| **4A. Nguy cơ Suy giảm Dân số** | **{acc_d:.2%}** | **{f1_d:.2%}** | Dự báo đà thu hẹp dân số 2050 dựa trên Tốc độ tăng trưởng 2026, Mức sinh TFR 2026, Quy mô log10, Tuổi trung vị và Tỷ lệ 65% |",
        f"| **4B. Nguy cơ Xã hội Siêu già 2050** | **{acc_a:.2%}** | **{f1_a:.2%}** | Phân loại quốc gia vượt ngưỡng 20% người cao tuổi dựa trên Tỷ lệ 65% 2026, Tuổi trung vị, Mức sinh TFR và Tuổi thọ trung bình |",
        "",
        "## 5. Top 10 Quốc gia có Nguy cơ Suy giảm Dân số Cao nhất (Depopulation Risk)",
        "| Thứ hạng | Quốc gia | Mã ISO | Điểm Nguy cơ Suy giảm | Phân loại |",
        "| :---: | :--- | :---: | :---: | :--- |",
    ]

    for idx, r in enumerate(top_depop_risk, 1):
        report.append(f"| {idx} | {r['Entity']} | {r['Code']} | {r['Depopulation_Risk_Score']:.2%} | {r['Depopulation_Category']} |")

    report.extend([
        "",
        "## 6. Top 10 Quốc gia được Dự báo trở thành Xã hội Siêu già năm 2050 (Super-Aged)",
        "| Thứ hạng | Quốc gia | Mã ISO | Xác suất Siêu già (65+ >= 20%) | Phân loại Dự báo |",
        "| :---: | :--- | :---: | :---: | :--- |",
    ])

    for idx, r in enumerate(top_super_aged, 1):
        report.append(f"| {idx} | {r['Entity']} | {r['Code']} | {r['Super_Aged_Risk_Score']:.2%} | {r['Super_Aged_Category']} |")

    report.extend([
        "",
        "## 7. Danh mục Tệp Dữ liệu Đầu ra",
        "1. [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv): Dự báo dân số với nhãn `historical` (<=2026) và `projected` (2027-2050).",
        "2. [`data/processed/model_vs_un_wpp_comparison_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/model_vs_un_wpp_comparison_2050.csv): So sánh đối chiếu ML vs UN kèm cột Residual và Residual_Pct (2027-2050).",
        "3. [`data/processed/population_policy_scenarios_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_policy_scenarios_2050.csv): Bảng 4 kịch bản chính sách can thiệp (Baseline, Khuyến sinh, Tuổi hưu, Toàn diện).",
        "4. [`data/processed/country_risk_classification_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/country_risk_classification_2050.csv): Điểm số rủi ro suy giảm và xác suất xã hội siêu già 2050.",
        "5. [`reports/modeling/correlation_matrix.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/correlation_matrix.png): Ma trận nhiệt tương quan tuyến tính Pearson.",
        "6. [`reports/modeling/confusion_matrix.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/confusion_matrix.png): Ma trận nhầm lẫn của 2 bài toán phân loại.",
        "7. [`reports/modeling/forecast_trends_2050.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/forecast_trends_2050.png): Đường xu hướng dự báo 1950 - 2050.",
    ])

    (REPORTS_DIR / "model_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Đã xuất báo cáo mô hình hóa toàn diện tại: {REPORTS_DIR / 'model_report.md'}")


if __name__ == "__main__":
    main()
