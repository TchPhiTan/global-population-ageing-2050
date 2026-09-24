from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "population_fact_long.csv"
OUTPUT = ROOT / "reports" / "eda"


def load_rows() -> list[dict[str, str]]:
    with INPUT.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def select(rows: list[dict[str, str]], indicator: str, status: str = "estimate") -> list[dict[str, str]]:
    return [row for row in rows if row["Indicator"] == indicator and row["DataStatus"] == status]


def latest_year(rows: list[dict[str, str]]) -> int:
    return max(int(row["Year"]) for row in rows)


def save_figure(name: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUTPUT / name, dpi=160)
    plt.close()


def plot_global_trend(rows: list[dict[str, str]]) -> None:
    population = select(rows, "Population")
    totals: dict[int, float] = defaultdict(float)
    for row in population:
        totals[int(row["Year"])] += float(row["Value"])
    years = sorted(totals)
    values = [totals[year] / 1_000_000_000 for year in years]
    plt.figure(figsize=(11, 5))
    plt.plot(years, values, color="#174a5b", linewidth=2)
    plt.title("Global population trend")
    plt.xlabel("Year")
    plt.ylabel("Population (billions)")
    save_figure("01-global-population-trend.png")


def plot_top_populations(rows: list[dict[str, str]]) -> list[tuple[str, float]]:
    population = select(rows, "Population")
    year = latest_year(population)
    values = sorted(
        ((row["Entity"], float(row["Value"])) for row in population if int(row["Year"]) == year),
        key=lambda item: item[1],
        reverse=True,
    )[:10]
    values.reverse()
    plt.figure(figsize=(10, 6))
    plt.barh([item[0] for item in values], [item[1] / 1_000_000 for item in values], color="#d97941")
    plt.title(f"Top 10 populations in {year}")
    plt.xlabel("Population (millions)")
    save_figure("02-top-populations.png")
    return list(reversed(values))


def plot_growth_distribution(rows: list[dict[str, str]]) -> tuple[int, float, float]:
    growth = select(rows, "Population growth rate")
    year = latest_year(growth)
    values = [float(row["Value"]) for row in growth if int(row["Year"]) == year]
    plt.figure(figsize=(10, 5))
    sns.histplot(values, bins=25, kde=True, color="#4b7f52")
    plt.title(f"Population growth rate distribution in {year}")
    plt.xlabel("Growth rate (%)")
    plt.ylabel("Number of entities")
    save_figure("03-growth-rate-distribution.png")
    return year, min(values), max(values)


def plot_fertility_growth(rows: list[dict[str, str]]) -> tuple[int, float]:
    fertility = {(
        row["Entity"], int(row["Year"])
    ): float(row["Value"]) for row in select(rows, "Total fertility rate")}
    growth = {(
        row["Entity"], int(row["Year"])
    ): float(row["Value"]) for row in select(rows, "Population growth rate")}
    common = [(fertility[key], growth[key]) for key in fertility if key in growth]
    year = max(key[1] for key in fertility)
    current = [
        (value, growth[key])
        for key, value in fertility.items()
        if key[1] == year and key in growth
    ]
    plt.figure(figsize=(9, 6))
    sns.scatterplot(x=[item[0] for item in common], y=[item[1] for item in common], alpha=0.35, color="#6d4c8d")
    plt.title("Fertility rate and population growth")
    plt.xlabel("Total fertility rate (children per woman)")
    plt.ylabel("Population growth rate (%)")
    save_figure("04-fertility-growth-scatter.png")
    return year, len(current)


def plot_heatmap(rows: list[dict[str, str]]) -> None:
    population = select(rows, "Population")
    latest = latest_year(population)
    top_entities = {
        row["Entity"] for row in population if int(row["Year"]) == latest
    }
    top_entities = {
        row["Entity"] for row in sorted(
            (row for row in population if int(row["Year"]) == latest),
            key=lambda row: float(row["Value"]),
            reverse=True,
        )[:15]
    }
    years = [2000, 2005, 2010, 2015, 2020, latest]
    matrix: dict[str, dict[int, float]] = defaultdict(dict)
    for row in population:
        if row["Entity"] in top_entities and int(row["Year"]) in years:
            matrix[row["Entity"]][int(row["Year"])] = float(row["Value"]) / 1_000_000
    entities = sorted(top_entities, key=lambda entity: matrix[entity].get(latest, 0), reverse=True)
    values = [[matrix[entity].get(year) for year in years] for entity in entities]
    plt.figure(figsize=(10, 8))
    sns.heatmap(values, xticklabels=years, yticklabels=entities, cmap="YlGnBu", annot=False)
    plt.title("Population heatmap for selected populous entities")
    plt.xlabel("Year")
    plt.ylabel("Entity")
    save_figure("05-population-heatmap.png")


def write_summary(rows: list[dict[str, str]], top: list[tuple[str, float]], growth: tuple[int, float, float], scatter: tuple[int, int]) -> None:
    population = select(rows, "Population")
    latest = latest_year(population)
    summary = [
        "# EDA Summary",
        "",
        f"- Latest historical population year: {latest}.",
        f"- Largest population in the latest historical year: {top[0][0]} ({top[0][1]:,.0f}).",
        f"- Growth-rate distribution year: {growth[0]}, range: {growth[1]:.2f}% to {growth[2]:.2f}%.",
        f"- Fertility-growth scatter uses {scatter[1]} latest-year paired observations around year {scatter[0]}.",
        "- Interpret projected years separately from estimates; the EDA charts use estimates unless stated otherwise.",
    ]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "eda_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


def main() -> None:
    sns.set_theme(style="whitegrid")
    rows = load_rows()
    plot_global_trend(rows)
    top = plot_top_populations(rows)
    growth = plot_growth_distribution(rows)
    scatter = plot_fertility_growth(rows)
    plot_heatmap(rows)
    write_summary(rows, top, growth, scatter)
    print("EDA completed: 5 figures and summary generated")


if __name__ == "__main__":
    main()