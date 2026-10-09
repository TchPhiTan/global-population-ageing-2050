import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.linear_model import LinearRegression

warnings.filterwarnings("ignore")

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

def main():
    print("Nạp dữ liệu từ population_fact_wide.csv...")
    df = pd.read_csv(PROCESSED_DIR / "population_fact_wide.csv")
    features = ["Year", "Total fertility rate", "Life expectancy", "Natural population growth rate", "Median age"]

    entities = df["Entity"].unique()
    all_chunks = []

    for entity in entities:
        sub = df[df["Entity"] == entity].sort_values("Year").copy()
        code = sub["Code"].dropna().iloc[0] if not sub["Code"].dropna().empty else ""
        cont = sub["Continent"].dropna().iloc[0] if not sub["Continent"].dropna().empty else "Others"
        reg_type = sub["Region_Type"].dropna().iloc[0] if not sub["Region_Type"].dropna().empty else "Quốc Gia"

        # Historical slice for training (<= 2026)
        hist = sub[sub["Year"] <= 2026].dropna(subset=["Population"])
        train_feats = [f for f in features if f in hist.columns and hist[f].notna().sum() >= 10]

        # 1. Train Single Linear Model (Year only)
        pred_single_all = np.zeros(len(sub))
        if len(hist) >= 5:
            m_single = LinearRegression().fit(hist[["Year"]].values, hist["Population"].values)
            pred_single_all = m_single.predict(sub[["Year"]].values)
        else:
            pred_single_all = sub["Population"].fillna(0).values

        # 2. Train Multiple Linear Model
        pred_multi_all = np.copy(pred_single_all)
        if len(train_feats) == 5 and len(hist.dropna(subset=train_feats)) >= 10:
            h_clean = hist.dropna(subset=train_feats)
            m_multi = LinearRegression().fit(h_clean[train_feats].values, h_clean["Population"].values)
            
            valid_mask = sub[train_feats].notna().all(axis=1)
            if valid_mask.any():
                pred_multi_all[valid_mask] = m_multi.predict(sub.loc[valid_mask, train_feats].values)

        pred_single_all = np.maximum(pred_single_all, 0)
        pred_multi_all = np.maximum(pred_multi_all, 0)

        # Build output chunk
        sub["Code"] = code
        sub["Continent"] = cont
        sub["Region_Type"] = reg_type
        sub["Population_UN"] = sub["Population"].round().astype("Int64")
        sub["Population_Actual"] = np.where(sub["Year"] <= 2026, sub["Population_UN"], np.nan)
        sub["Population_Single_ML"] = np.round(pred_single_all).astype(np.int64)
        sub["Population_Multi_ML"] = np.round(pred_multi_all).astype(np.int64)

        ref_pop = np.where(sub["Year"] <= 2026, sub["Population_Actual"], sub["Population_UN"])
        res_multi = ref_pop - sub["Population_Multi_ML"]
        res_multi_pct = np.where(ref_pop > 0, np.round((res_multi / ref_pop) * 100, 2), np.nan)

        res_single = ref_pop - sub["Population_Single_ML"]
        res_single_pct = np.where(ref_pop > 0, np.round((res_single / ref_pop) * 100, 2), np.nan)

        sub["Residual_Multi"] = np.round(res_multi).astype("Int64")
        sub["Residual_Multi_Pct"] = res_multi_pct
        sub["Residual_Single"] = np.round(res_single).astype("Int64")
        sub["Residual_Single_Pct"] = res_single_pct

        # Normal Q-Q Plot Coordinates (Theoretical Quantiles & Standardized Residuals)
        sub["Theoretical_Quantiles"] = np.nan
        sub["Standardized_Residuals"] = np.nan

        h_mask = sub["Year"] <= 2026
        if h_mask.sum() >= 5:
            res_vals = sub.loc[h_mask, "Residual_Multi"].values.astype(float)
            mean_res = np.mean(res_vals)
            std_res = np.std(res_vals, ddof=1)
            if std_res > 0:
                std_arr = (res_vals - mean_res) / std_res
                order = np.argsort(std_arr)
                ranks = np.empty_like(order)
                ranks[order] = np.arange(1, len(std_arr) + 1)
                probs = (ranks - 0.5) / len(std_arr)
                theo_q = stats.norm.ppf(probs)
                sub.loc[h_mask, "Theoretical_Quantiles"] = np.round(theo_q, 3)
                sub.loc[h_mask, "Standardized_Residuals"] = np.round(std_arr, 3)

        # Rename demographic indicators
        sub["Total_Fertility_Rate"] = sub["Total fertility rate"].round(3)
        sub["Life_Expectancy"] = sub["Life expectancy"].round(2)
        sub["Natural_Growth_Rate"] = sub["Natural population growth rate"].round(3)
        sub["Median_Age"] = sub["Median age"].round(2)
        sub["Share_65plus"] = sub["Share of population aged 65+"].round(2)
        p_gr = sub.get("Population growth rate", 0)
        n_gr = sub.get("Natural population growth rate", 0)
        sub["Net_Migration_Rate"] = (p_gr - n_gr).round(3)

        keep_cols = [
            "Entity", "Code", "Continent", "Region_Type", "Year", "DataStatus",
            "Population_Actual", "Population_UN", "Population_Single_ML", "Population_Multi_ML",
            "Residual_Multi", "Residual_Multi_Pct", "Residual_Single", "Residual_Single_Pct",
            "Theoretical_Quantiles", "Standardized_Residuals",
            "Total_Fertility_Rate", "Life_Expectancy", "Natural_Growth_Rate", "Median_Age", "Share_65plus",
            "Net_Migration_Rate"
        ]
        all_chunks.append(sub[keep_cols])

    out_df = pd.concat(all_chunks, ignore_index=True)

    # Impute missing continent Life_Expectancy as population-weighted average of member countries
    for cont in ["North America", "South America"]:
        cont_mask = (out_df["Entity"] == cont)
        country_sub = out_df[(out_df["Continent"] == cont) & (out_df["Region_Type"] == "Quốc Gia")]
        for yr in out_df.loc[cont_mask, "Year"].unique():
            yr_countries = country_sub[country_sub["Year"] == yr]
            if not yr_countries.empty and yr_countries["Life_Expectancy"].notna().any():
                tot_pop = yr_countries["Population_UN"].sum()
                w_le = (yr_countries["Life_Expectancy"] * yr_countries["Population_UN"]).sum() / tot_pop if tot_pop > 0 else yr_countries["Life_Expectancy"].mean()
                out_df.loc[cont_mask & (out_df["Year"] == yr), "Life_Expectancy"] = round(w_le, 2)

    out_path = PROCESSED_DIR / "multivariate_population_forecast.csv"
    out_df.to_csv(out_path, index=False)
    print(f"Xuất file thành công: {out_path} ({len(out_df)} dòng)")

    # Print verification stats
    w_out = out_df[out_df["Entity"] == "World"]
    for yr in [1950, 1980, 2000, 2026, 2030, 2050]:
        r = w_out[w_out["Year"] == yr].iloc[0]
        un_str = f"{r['Population_UN']:,.0f}" if pd.notna(r['Population_UN']) else "N/A"
        sg_str = f"{r['Population_Single_ML']:,.0f}" if pd.notna(r['Population_Single_ML']) else "N/A"
        ml_str = f"{r['Population_Multi_ML']:,.0f}" if pd.notna(r['Population_Multi_ML']) else "N/A"
        pct_str = f"{r['Residual_Multi_Pct']}%" if pd.notna(r['Residual_Multi_Pct']) else "N/A"
        q_str = f"{r['Theoretical_Quantiles']}" if pd.notna(r['Theoretical_Quantiles']) else "N/A"
        z_str = f"{r['Standardized_Residuals']}" if pd.notna(r['Standardized_Residuals']) else "N/A"
        print(f"World {yr:4d} | UN: {un_str:>14} | Multi ML: {ml_str:>14} | Res: {pct_str:>8} | Theo Q: {q_str:>6} | Std Res: {z_str:>6}")

if __name__ == "__main__":
    main()
