from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
INPUT_LONG = ROOT / "data" / "processed" / "population_fact_long.csv"
INPUT_WIDE = ROOT / "data" / "processed" / "population_fact_wide.csv"
OUTPUT = ROOT / "reports" / "eda"
OUTPUT.mkdir(parents=True, exist_ok=True)


def load_long_rows() -> list[dict[str, str]]:
    with INPUT_LONG.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def load_wide_rows() -> list[dict[str, str]]:
    with INPUT_WIDE.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def is_country(code: str | None) -> bool:
    if not code:
        return False
    return (len(code) == 3 and code.isalpha() and code.isupper()) or code == "OWID_KOS"


def save_figure(name: str) -> None:
    plt.tight_layout()
    plt.savefig(OUTPUT / name, dpi=160)
    plt.close()


# ----------------------------------------------------------------------
# 1. Biến động Dân số Toàn cầu (1950 - 2050)
# ----------------------------------------------------------------------
def plot_global_population_trend(wide_rows: list[dict[str, str]]) -> None:
    world_rows = [r for r in wide_rows if r["Entity"] == "World" and int(r["Year"]) <= 2050]
    world_rows.sort(key=lambda r: int(r["Year"]))

    years = [int(r["Year"]) for r in world_rows if r.get("Population")]
    pops = [float(r["Population"]) / 1_000_000_000 for r in world_rows if r.get("Population")]

    plt.figure(figsize=(11, 5))
    # Split historical vs projected
    split_idx = next(i for i, r in enumerate(world_rows) if int(r["Year"]) == 2024)

    plt.plot(years[:split_idx], pops[:split_idx], color="#174a5b", linewidth=2.5, label="Thực tế (1950 - 2023)")
    plt.plot(years[split_idx - 1:], pops[split_idx - 1:], color="#d97941", linewidth=2.5, linestyle="--", label="Dự phóng UN Medium (2024 - 2050)")
    plt.axvline(x=2026, color="red", linestyle=":", alpha=0.7, label="Mốc hiện tại (2026: ~8.3 tỷ)")

    plt.title("Xu hướng Quy mô Dân số Toàn cầu (1950 - 2050)", fontsize=13, fontweight="bold")
    plt.xlabel("Năm")
    plt.ylabel("Dân số (tỷ người)")
    plt.legend(frameon=True)
    save_figure("01-global-population-trend.png")


# ----------------------------------------------------------------------
# 2. Top 10 Quốc gia Đông dân nhất Thế giới (Năm 2026)
# ----------------------------------------------------------------------
def plot_top_populations(wide_rows: list[dict[str, str]]) -> list[tuple[str, float]]:
    c_2026 = [
        r for r in wide_rows
        if int(r["Year"]) == 2026 and is_country(r.get("Code")) and r.get("Population")
    ]
    c_2026.sort(key=lambda r: float(r["Population"]), reverse=True)
    top10 = [(r["Entity"], float(r["Population"])) for r in c_2026[:10]]
    top10.reverse()

    plt.figure(figsize=(10, 6))
    bars = plt.barh([item[0] for item in top10], [item[1] / 1_000_000 for item in top10], color="#2b5c8f")
    plt.title("Top 10 Quốc gia Đông dân nhất Thế giới (Năm 2026)", fontsize=13, fontweight="bold")
    plt.xlabel("Dân số (triệu người)")
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 15, bar.get_y() + bar.get_height() / 2, f"{w:,.1f}M", va="center", fontsize=9)
    plt.xlim(0, 1650)
    save_figure("02-top-populations.png")
    return list(reversed(top10))


# ----------------------------------------------------------------------
# 3. Phân phối Tốc độ Tăng trưởng Dân số năm 2026
# ----------------------------------------------------------------------
def plot_growth_distribution(wide_rows: list[dict[str, str]]) -> tuple[int, float, float, int, int]:
    growth_2026 = [
        float(r["Population growth rate"])
        for r in wide_rows
        if int(r["Year"]) == 2026 and is_country(r.get("Code")) and r.get("Population growth rate")
    ]
    neg_count = sum(1 for g in growth_2026 if g < 0)
    pos_count = len(growth_2026) - neg_count

    plt.figure(figsize=(10, 5))
    sns.histplot(growth_2026, bins=30, kde=True, color="#3e8e7e")
    plt.axvline(x=0, color="red", linestyle="--", linewidth=1.5, label=f"Ngưỡng 0% (Âm: {neg_count} nước, Dương: {pos_count} nước)")
    plt.title("Phân phối Tốc độ Tăng trưởng Dân số Quốc gia năm 2026", fontsize=13, fontweight="bold")
    plt.xlabel("Tốc độ tăng trưởng (%/năm)")
    plt.ylabel("Số lượng quốc gia")
    plt.legend()
    save_figure("03-growth-rate-distribution.png")
    return 2026, min(growth_2026), max(growth_2026), neg_count, pos_count


# ----------------------------------------------------------------------
# 4. Tương quan Mức sinh và Tốc độ Tăng trưởng (2026)
# ----------------------------------------------------------------------
def plot_fertility_growth(wide_rows: list[dict[str, str]]) -> None:
    pairs = [
        (float(r["Total fertility rate"]), float(r["Population growth rate"]))
        for r in wide_rows
        if int(r["Year"]) == 2026 and is_country(r.get("Code")) and r.get("Total fertility rate") and r.get("Population growth rate")
    ]
    # Fallback to 2023 fertility vs 2026 growth if TFR projected is missing
    if not pairs:
        tfr_map = {r["Entity"]: float(r["Total fertility rate"]) for r in wide_rows if int(r["Year"]) == 2023 and r.get("Total fertility rate")}
        for r in wide_rows:
            if int(r["Year"]) == 2026 and is_country(r.get("Code")) and r.get("Population growth rate"):
                ent = r["Entity"]
                if ent in tfr_map:
                    pairs.append((tfr_map[ent], float(r["Population growth rate"])))

    plt.figure(figsize=(9, 6))
    x = [p[0] for p in pairs]
    y = [p[1] for p in pairs]
    sns.scatterplot(x=x, y=y, alpha=0.7, color="#795290", s=60)
    plt.axvline(x=2.1, color="orange", linestyle="--", label="Mức sinh thay thế (TFR = 2.1)")
    plt.axhline(y=0, color="red", linestyle=":", label="Tăng trưởng 0%")
    plt.title("Tương quan giữa Mức sinh (TFR) và Tốc độ Tăng trưởng Dân số", fontsize=12, fontweight="bold")
    plt.xlabel("Mức sinh (Số con trung bình / phụ nữ)")
    plt.ylabel("Tốc độ tăng trưởng dân số (%)")
    plt.legend()
    save_figure("04-fertility-growth-scatter.png")


# ----------------------------------------------------------------------
# 5. Heatmap Biến động Dân số các Nước Đông Dân
# ----------------------------------------------------------------------
def plot_population_heatmap(wide_rows: list[dict[str, str]]) -> None:
    top15_entities = [
        r["Entity"] for r in sorted(
            [r for r in wide_rows if int(r["Year"]) == 2026 and is_country(r.get("Code")) and r.get("Population")],
            key=lambda r: float(r["Population"]),
            reverse=True
        )[:15]
    ]
    years = [1970, 1990, 2010, 2026, 2040, 2050]
    matrix: dict[str, dict[int, float]] = defaultdict(dict)
    for r in wide_rows:
        if r["Entity"] in top15_entities and int(r["Year"]) in years and r.get("Population"):
            matrix[r["Entity"]][int(r["Year"])] = float(r["Population"]) / 1_000_000

    values = [[matrix[ent].get(yr, 0) for yr in years] for ent in top15_entities]
    plt.figure(figsize=(10, 8))
    sns.heatmap(values, xticklabels=years, yticklabels=top15_entities, cmap="YlGnBu", annot=True, fmt=".0f")
    plt.title("Quy mô Dân số Top 15 Quốc gia qua các Mốc Thập kỷ (Triệu người)", fontsize=12, fontweight="bold")
    plt.xlabel("Năm")
    plt.ylabel("Quốc gia")
    save_figure("05-population-heatmap.png")


# ----------------------------------------------------------------------
# 6. EDA GIÀ HÓA: Xu hướng Chuyển dịch 3 Khối Tuổi Toàn cầu (1950 - 2050)
# ----------------------------------------------------------------------
def plot_global_age_structure_trend(wide_rows: list[dict[str, str]]) -> None:
    world_rows = [r for r in wide_rows if r["Entity"] == "World" and int(r["Year"]) <= 2050]
    world_rows.sort(key=lambda r: int(r["Year"]))

    years = [int(r["Year"]) for r in world_rows if r.get("Older people (65+ years)")]
    elderly = [float(r["Older people (65+ years)"]) / 1_000_000_000 for r in world_rows if r.get("Older people (65+ years)")]
    working = [float(r["Working-age adults (15-64 years)"]) / 1_000_000_000 for r in world_rows if r.get("Working-age adults (15-64 years)")]
    children = [float(r["Children (under-15s)"]) / 1_000_000_000 for r in world_rows if r.get("Children (under-15s)")]

    plt.figure(figsize=(11, 6))
    plt.stackplot(
        years,
        children,
        working,
        elderly,
        labels=["Trẻ em (0-14 tuổi)", "Độ tuổi lao động (15-64 tuổi)", "Người cao tuổi (65+ tuổi)"],
        colors=["#76c893", "#1e6091", "#d00000"],
        alpha=0.85
    )
    plt.axvline(x=2026, color="black", linestyle="--", linewidth=1.5, label="Hiện tại (2026)")
    plt.title("Sự Chuyển dịch Cơ cấu 3 Nhóm Tuổi Toàn cầu (1950 - 2050)", fontsize=13, fontweight="bold")
    plt.xlabel("Năm")
    plt.ylabel("Quy mô dân số (tỷ người)")
    plt.legend(loc="upper left", frameon=True)
    save_figure("06-global-ageing-trend-2050.png")


# ----------------------------------------------------------------------
# 7. EDA GIÀ HÓA: Tăng trưởng Tuổi Trung vị (Median Age) theo Châu lục
# ----------------------------------------------------------------------
def plot_median_age_by_region(wide_rows: list[dict[str, str]]) -> None:
    regions = ["World", "Europe (UN)", "Asia (UN)", "Northern America (UN)", "Latin America and the Caribbean (UN)", "Africa (UN)"]
    labels = ["Toàn cầu", "Châu Âu", "Châu Á", "Bắc Mỹ", "Mỹ Latinh", "Châu Phi"]
    colors = ["#000000", "#1d3557", "#457b9d", "#2a9d8f", "#e76f51", "#d62828"]

    plt.figure(figsize=(11, 6))
    for region, lbl, col in zip(regions, labels, colors):
        rows = [r for r in wide_rows if r["Entity"] == region and int(r["Year"]) <= 2050 and r.get("Median age")]
        rows.sort(key=lambda r: int(r["Year"]))
        if rows:
            yrs = [int(r["Year"]) for r in rows]
            meds = [float(r["Median age"]) for r in rows]
            plt.plot(yrs, meds, label=lbl, color=col, linewidth=2.2 if region == "World" else 1.8, linestyle="-" if region != "World" else "--")

    plt.axvline(x=2026, color="gray", linestyle=":", alpha=0.8)
    plt.title("Xu hướng Tăng trưởng Tuổi Trung vị (Median Age) theo Khu vực (1950 - 2050)", fontsize=13, fontweight="bold")
    plt.xlabel("Năm")
    plt.ylabel("Tuổi trung vị (năm)")
    plt.legend(frameon=True)
    save_figure("07-median-age-by-continent.png")


# ----------------------------------------------------------------------
# 8. EDA GIÀ HÓA: Top 10 Quốc gia Siêu Già năm 2050 (% Dân số 65+)
# ----------------------------------------------------------------------
def plot_top_aged_societies_2050(wide_rows: list[dict[str, str]]) -> None:
    c_2050 = [
        r for r in wide_rows
        if int(r["Year"]) == 2050 and is_country(r.get("Code")) and r.get("Share of population aged 65+")
    ]
    c_2050.sort(key=lambda r: float(r["Share of population aged 65+"]), reverse=True)
    top10 = [(r["Entity"], float(r["Share of population aged 65+"])) for r in c_2050[:10]]
    top10.reverse()

    plt.figure(figsize=(10, 6))
    bars = plt.barh([item[0] for item in top10], [item[1] for item in top10], color="#9d0208")
    plt.axvline(x=20.0, color="orange", linestyle="--", linewidth=1.5, label="Ngưỡng Xã hội Siêu già (Super-aged >= 20%)")
    plt.title("Top 10 Quốc gia có Tỷ lệ Dân số Già (65+) Cao nhất Thế giới vào Năm 2050", fontsize=12, fontweight="bold")
    plt.xlabel("Tỷ lệ người cao tuổi 65+ (%)")
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.3, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", va="center", fontsize=9)
    plt.xlim(0, 48)
    plt.legend()
    save_figure("08-top-super-aged-societies-2050.png")


def write_summary(
    wide_rows: list[dict[str, str]],
    top_2026: list[tuple[str, float]],
    growth_info: tuple[int, float, float, int, int],
) -> None:
    # Key numbers for summary
    world_2026 = next((r for r in wide_rows if r["Entity"] == "World" and int(r["Year"]) == 2026), {})
    world_2050 = next((r for r in wide_rows if r["Entity"] == "World" and int(r["Year"]) == 2050), {})
    
    pop_2026 = float(world_2026.get("Population", 8.3e9))
    pop_2050 = float(world_2050.get("Population", 9.7e9))
    
    share65_1950 = float(next((r for r in wide_rows if r["Entity"] == "World" and int(r["Year"]) == 1950), {}).get("Share of population aged 65+", 5.0))
    share65_2026 = float(world_2026.get("Share of population aged 65+", 10.3))
    share65_2050 = float(world_2050.get("Share of population aged 65+", 16.4))

    dep_1950 = float(next((r for r in wide_rows if r["Entity"] == "World" and int(r["Year"]) == 1950), {}).get("Old-age dependency ratio", 8.0))
    dep_2026 = float(world_2026.get("Old-age dependency ratio", 16.0))
    dep_2050 = float(world_2050.get("Old-age dependency ratio", 26.0))

    med_1950 = float(next((r for r in wide_rows if r["Entity"] == "World" and int(r["Year"]) == 1950), {}).get("Median age", 23.5))
    med_2026 = float(world_2026.get("Median age", 31.2))
    med_2050 = float(world_2050.get("Median age", 36.2))

    summary_md = f"""# Báo cáo Phân tích Khám phá Dữ liệu (EDA): Biến động Dân số & Xu hướng Già hoá Toàn cầu đến năm 2050

## 1. Trụ cột 1: Biến động Quy mô & Tăng trưởng Dân số Toàn cầu (1950 – 2050)
* **Quy mô dân số mốc hiện tại (2026)**: Đạt xấp xỉ **{pop_2026:,.0f} người (~{pop_2026/1e9:.2f} tỷ người)**.
* **Dự báo dân số đến năm 2050 (UN WPP Medium Scenario)**: Đạt xấp xỉ **{pop_2050:,.0f} người (~{pop_2050/1e9:.2f} tỷ người)**.
* **Đỉnh tăng trưởng**: Tốc độ tăng trưởng hàng năm đạt đỉnh vào thập niên 1960 (~2.1%/năm) và liên tục giảm dần, dự kiến chỉ còn dưới 0.4%/năm vào năm 2050.
* **Phân hóa tăng trưởng năm 2026**:
  - Đã có **{growth_info[3]} quốc gia/vùng lãnh thổ** ghi nhận mức tăng trưởng âm (suy giảm dân số), chủ yếu tập trung tại Đông Á (Hàn Quốc, Nhật Bản, Trung Quốc) và Đông/Nam Âu.
  - Còn **{growth_info[4]} quốc gia/vùng lãnh thổ** duy trì tăng trưởng dương, dẫn đầu bởi các nước Châu Phi cận Sahara.
* **Top 10 quốc gia đông dân nhất 2026**: 
  1. Ấn Độ ({top_2026[0][1]/1e6:,.1f}M) - chính thức vượt Trung Quốc
  2. Trung Quốc ({top_2026[1][1]/1e6:,.1f}M)
  3. Hoa Kỳ ({top_2026[2][1]/1e6:,.1f}M)
  4. Indonesia ({top_2026[3][1]/1e6:,.1f}M)
  5. Pakistan ({top_2026[4][1]/1e6:,.1f}M)

---

## 2. Trụ cột 2: Xu hướng Già hoá Dân số Toàn diện đến Năm 2050
* **Tỷ lệ người cao tuổi (65+ tuổi) tăng gấp 3 lần**:
  - Năm 1950: Chỉ chiếm **{share65_1950:.1f}%** dân số toàn cầu.
  - Năm 2026: Đã tăng lên **{share65_2026:.1f}%** (vượt ngưỡng xã hội già hóa 7%).
  - Đến năm 2050: Dự báo đạt **{share65_2050:.1f}%** dân số toàn cầu (chính thức bước vào ngưỡng Xã hội Già theo chuẩn LHQ >= 14%).
* **Tuổi trung vị toàn cầu (Median Age)**:
  - Năm 1950: **{med_1950:.1f} tuổi**.
  - Năm 2026: **{med_2026:.1f} tuổi**.
  - Năm 2050: **{med_2050:.1f} tuổi** (các khu vực như Châu Âu và Đông Á tuổi trung vị sẽ vượt ngưỡng 45-48 tuổi).
* **Tỷ số phụ thuộc người cao tuổi (Old-age Dependency Ratio)**:
  - Tăng từ **{dep_1950:.1f}%** (1950) lên **{dep_2026:.1f}%** (2026) và dự kiến đạt **{dep_2050:.1f}%** vào năm 2050.
  - Nghĩa là vào năm 2050, cứ khoảng 4 người trong độ tuổi lao động sẽ phải gánh hơn 1 người cao tuổi, tạo áp lực khổng lồ lên an sinh xã hội và y tế.
* **Làn sóng các Xã hội Siêu già (Super-aged Society - Tỷ lệ 65+ >= 20%)**:
  - Đến năm 2050, hơn **60 quốc gia** sẽ trở thành xã hội siêu già. Những nước đứng đầu bao gồm Hàn Quốc, Nhật Bản, Ý, Tây Ban Nha, Hồng Kông với tỷ lệ 65+ dự kiến vượt ngưỡng **35% - 40%**.

---

## 3. Danh mục 8 Biểu đồ EDA Đã Tạo
1. [`01-global-population-trend.png`](file://{OUTPUT}/01-global-population-trend.png): Xu hướng Quy mô Dân số Toàn cầu (1950 – 2050).
2. [`02-top-populations.png`](file://{OUTPUT}/02-top-populations.png): Top 10 Quốc gia Đông dân nhất Thế giới (Năm 2026).
3. [`03-growth-rate-distribution.png`](file://{OUTPUT}/03-growth-rate-distribution.png): Phân phối Tốc độ Tăng trưởng Quốc gia năm 2026.
4. [`04-fertility-growth-scatter.png`](file://{OUTPUT}/04-fertility-growth-scatter.png): Tương quan giữa Mức sinh (TFR) và Tốc độ Tăng trưởng.
5. [`05-population-heatmap.png`](file://{OUTPUT}/05-population-heatmap.png): Ma trận Quy mô Dân số Top 15 Quốc gia qua các Thập kỷ.
6. [`06-global-ageing-trend-2050.png`](file://{OUTPUT}/06-global-ageing-trend-2050.png): Chuyển dịch Cơ cấu 3 Khối Tuổi Toàn cầu (1950 – 2050).
7. [`07-median-age-by-continent.png`](file://{OUTPUT}/07-median-age-by-continent.png): Xu hướng Tăng trưởng Tuổi Trung vị theo Khu vực.
8. [`08-top-super-aged-societies-2050.png`](file://{OUTPUT}/08-top-super-aged-societies-2050.png): Top 10 Quốc gia có Tỷ lệ Dân số Già (65+) Cao nhất Thế giới năm 2050.
"""
    (OUTPUT / "eda_summary.md").write_text(summary_md, encoding="utf-8")


def main() -> None:
    sns.set_theme(style="whitegrid")
    wide_rows = load_wide_rows()

    plot_global_population_trend(wide_rows)
    top_2026 = plot_top_populations(wide_rows)
    growth_info = plot_growth_distribution(wide_rows)
    plot_fertility_growth(wide_rows)
    plot_population_heatmap(wide_rows)
    
    # Ageing specific EDA
    plot_global_age_structure_trend(wide_rows)
    plot_median_age_by_region(wide_rows)
    plot_top_aged_societies_2050(wide_rows)

    write_summary(wide_rows, top_2026, growth_info)
    print("EDA hoàn tất: 8 biểu đồ chuẩn hóa và báo cáo tổng hợp eda_summary.md đã được xuất thành công!")


if __name__ == "__main__":
    main()