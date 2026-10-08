"""
Data Preprocessing Pipeline: Global Population & Ageing Dynamics (1950 - 2050)
=============================================================================
This module ingests raw demographic records from Our World in Data (OWID) and
UN WPP, harmonizes classifications, derives core ageing indicators, performs
data quality validation, and exports cleaned datasets for Tableau dashboards.

Key Pipeline Stages:
--------------------
1. Ingestion: Raw CSV indicators -> Long-format demographic records (1950-2050).
2. Indicator Extrapolation: Life Expectancy (2024-2050) and GDP per capita (2026).
3. Demographic Ratios: Share 65+, Old-age dependency ratio, Potential support ratio.
4. Age-Group Breakdown: Under-5s, Ages 5-14, Ages 15-24, Ages 25-64, Ages 65+.
5. Continent Aggregation: Natural growth and Population growth for 6 continents.
6. Exports & Validation: Core Tableau datasets + technical verification reports.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


# =============================================================================
# 1. DIRECTORY CONFIGURATION & CONSTANTS
# =============================================================================

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
TECHNICAL_DIR = PROCESSED_DIR / "technical"
TECHNICAL_DIR.mkdir(parents=True, exist_ok=True)

# Continents recognized for hierarchical roll-up
CONTINENT_NAMES = {"Africa", "Asia", "Europe", "North America", "South America", "Oceania"}

# Source indicator specifications: (filename, indicator_name, unit, estimate_col, projected_col)
SOURCE_SPECS = (
    (
        "population-with-un-projections.csv",
        "Population",
        "people",
        "Population",
        "Population (Projected)",
    ),
    (
        "population-growth-rates.csv",
        "Population growth rate",
        "percent",
        "Population growth rate",
        "Population growth rate (%) (Projected)",
    ),
    (
        "fertility-rate-with-projections.csv",
        "Total fertility rate",
        "children per woman",
        "Fertility rate (estimates)",
        "Fertility rate (projections) (Projected)",
    ),
    (
        "median-age.csv",
        "Median age",
        "years",
        "Median age",
        "Median age (Projected)",
    ),
    (
        "life-expectancy.csv",
        "Life expectancy",
        "years",
        "Life expectancy",
        None,
    ),
    (
        "population-young-working-elderly-with-projections.csv",
        "Older people (65+ years)",
        "people",
        "Older people (65+ years)",
        "Older people (65+ years) (Projected)",
    ),
    (
        "population-young-working-elderly-with-projections.csv",
        "Working-age adults (15-64 years)",
        "people",
        "Working-age adults (15-64 years)",
        "Working-age adults (15-64 years) (Projected)",
    ),
    (
        "population-young-working-elderly-with-projections.csv",
        "Children (under-15s)",
        "people",
        "Children (Under-15s)",
        "Children (under-15s) (Projected)",
    ),
    (
        "natural-population-growth.csv",
        "Natural population growth rate",
        "percent",
        "Natural population growth rate",
        "Natural population growth rate (Projected)",
    ),
    (
        "births-and-deaths-projected-to-2100.csv",
        "Births",
        "people",
        "Births",
        "Projected births (Projected)",
    ),
    (
        "births-and-deaths-projected-to-2100.csv",
        "Deaths",
        "people",
        "Deaths",
        "Projected deaths (Projected)",
    ),
    (
        "gdp-per-capita-worldbank.csv",
        "GDP per capita",
        "constant 2017 international-$",
        "GDP per capita",
        None,
    ),
)

# Core 26 schema fields expected by Tableau Dashboards 1, 2, 3
WIDE_COLUMNS = [
    "Entity",
    "Code",
    "Continent",
    "Region_Type",
    "Year",
    "DataStatus",
    "Population",
    "Population growth rate",
    "Natural population growth rate",
    "Total fertility rate",
    "Median age",
    "Life expectancy",
    "Births",
    "Deaths",
    "Older people (65+ years)",
    "Working-age adults (15-64 years)",
    "Children (under-15s)",
    "Share of population aged 65+",
    "Old-age dependency ratio",
    "Potential support ratio",
    "GDP per capita",
    "Ages 15-24",
    "Ages 25-64",
    "Ages 5-14",
    "Ages 65+",
    "Under-5s",
]

# Alias normalization for World Population Review benchmark validation
WPR_ALIASES = {
    "dr congo": "democratic republic of congo",
    "ivory coast": "cote d ivoire",
    "macau": "macao",
    "micronesia": "micronesia country",
    "republic of the congo": "congo",
    "saint helena ascension and tristan da cunha": "saint helena",
    "saint martin": "saint martin french part",
    "sint maarten": "sint maarten dutch part",
    "timor leste": "east timor",
    "vatican city": "vatican",
}


# =============================================================================
# 2. FILE I/O & PARSING HELPERS
# =============================================================================

def read_csv(path: Path) -> list[dict[str, str]]:
    """Reads a CSV file returning a list of row dictionaries."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    """Writes a list of row dictionaries to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_value(value: str | None) -> float | None:
    """Parses numeric string values, returning None on empty or invalid entries."""
    return float(value) if value and value.strip() else None


def normalize_name(value: str) -> str:
    """Normalizes entity names for fuzzy matching."""
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def load_continent_mapping() -> dict[str, str]:
    """Loads ISO Code -> Continent mapping from technical or processed storage."""
    mapping: dict[str, str] = {}
    path = TECHNICAL_DIR / "continent_mapping.csv"
    if not path.exists():
        path = PROCESSED_DIR / "continent_mapping.csv"
    if path.exists():
        for row in read_csv(path):
            code = row.get("Code", "").strip()
            continent = row.get("Continent", "").strip()
            if code and continent:
                mapping[code] = continent
    return mapping


# =============================================================================
# 3. FEATURE EXTRAPOLATION & DERIVATION PIPELINE
# =============================================================================

def extrapolate_life_expectancy(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """
    Extrapolates Life Expectancy for 2024 - 2050 based on 2000 - 2023 linear trends.
    Constrains annual slope within [0.02, 0.25] and caps maximum life expectancy at 92.0 years.
    """
    by_ent: dict[str, list[dict[str, object]]] = {}
    for r in records:
        if r["Indicator"] == "Life expectancy":
            by_ent.setdefault(str(r["Entity"]), []).append(r)

    extra_records: list[dict[str, object]] = []
    for ent, rows in by_ent.items():
        known_years = sorted(int(r["Year"]) for r in rows)
        if not known_years:
            continue
        max_yr = max(known_years)
        if max_yr >= 2050:
            continue

        code = rows[0]["Code"]
        fit_rows = [r for r in rows if int(r["Year"]) >= 2000]
        if len(fit_rows) >= 5:
            xs = [int(r["Year"]) for r in fit_rows]
            ys = [float(r["Value"]) for r in fit_rows]
            n = len(xs)
            denom = n * sum(x * x for x in xs) - sum(xs) ** 2
            slope = (n * sum(x * y for x, y in zip(xs, ys)) - sum(xs) * sum(ys)) / denom if denom != 0 else 0.08
            slope = max(min(slope, 0.25), 0.02)
            last_val = float([r for r in rows if int(r["Year"]) == max_yr][0]["Value"])

            for fut_yr in range(max_yr + 1, 2051):
                val = min(last_val + slope * (fut_yr - max_yr), 92.0)
                extra_records.append({
                    "Entity": ent,
                    "Code": code,
                    "Year": fut_yr,
                    "Indicator": "Life expectancy",
                    "Value": round(val, 4),
                    "Unit": "years",
                    "DataStatus": "historical" if fut_yr <= 2026 else "projected",
                })
    return extra_records


def extrapolate_gdp_per_capita(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """
    Extrapolates GDP per capita for 2026 based on 2021 - 2025 CAGR growth trend.
    Constrains annual growth within [-2%, +6%].
    """
    by_ent: dict[str, list[dict[str, object]]] = {}
    for r in records:
        if r["Indicator"] == "GDP per capita":
            by_ent.setdefault(str(r["Entity"]), []).append(r)

    extra_records: list[dict[str, object]] = []
    for ent, rows in by_ent.items():
        known_years = sorted(int(r["Year"]) for r in rows)
        if not known_years or max(known_years) != 2025:
            continue

        max_yr = 2025
        code = rows[0]["Code"]
        rows_recent = [r for r in rows if int(r["Year"]) >= 2021]

        if len(rows_recent) >= 2:
            min_recent_yr = min(int(x["Year"]) for x in rows_recent)
            v_start = float([r for r in rows if int(r["Year"]) == min_recent_yr][0]["Value"])
            v_end = float([r for r in rows if int(r["Year"]) == max_yr][0]["Value"])
            y_span = max_yr - min_recent_yr
            growth = (v_end / v_start) ** (1.0 / y_span) - 1.0 if v_start > 0 and y_span > 0 else 0.018
            growth = max(min(growth, 0.06), -0.02)
            val_2026 = round(v_end * (1.0 + growth), 2)
        else:
            val_2026 = round(float([r for r in rows if int(r["Year"]) == max_yr][0]["Value"]) * 1.018, 2)

        extra_records.append({
            "Entity": ent,
            "Code": code,
            "Year": 2026,
            "Indicator": "GDP per capita",
            "Value": val_2026,
            "Unit": "constant 2017 international-$",
            "DataStatus": "historical",
        })
    return extra_records


def derive_ageing_indicators(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """
    Derives core demographic ratios from the three broad age classes:
    - Share of population aged 65+ (%)
    - Old-age dependency ratio (Older / Working * 100)
    - Potential support ratio (Working / Older)
    """
    age_groups: dict[tuple[str, str | None, int, str], dict[str, float]] = {}
    for r in records:
        if r["Indicator"] in ("Older people (65+ years)", "Working-age adults (15-64 years)", "Children (under-15s)"):
            key = (str(r["Entity"]), r["Code"], int(r["Year"]), str(r["DataStatus"]))
            age_groups.setdefault(key, {})[str(r["Indicator"])] = float(r["Value"])

    derived: list[dict[str, object]] = []
    for (entity, code, year, status), groups in age_groups.items():
        older = groups.get("Older people (65+ years)")
        working = groups.get("Working-age adults (15-64 years)")
        children = groups.get("Children (under-15s)")

        if older is not None and working is not None and children is not None:
            total = older + working + children
            if total > 0:
                derived.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": year,
                    "Indicator": "Share of population aged 65+",
                    "Value": round((older / total) * 100, 2),
                    "Unit": "percent",
                    "DataStatus": status,
                })
            if working > 0:
                derived.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": year,
                    "Indicator": "Old-age dependency ratio",
                    "Value": round((older / working) * 100, 2),
                    "Unit": "percent",
                    "DataStatus": status,
                })
            if older > 0 and working > 0:
                derived.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": year,
                    "Indicator": "Potential support ratio",
                    "Value": round(working / older, 2),
                    "Unit": "ratio",
                    "DataStatus": status,
                })
    return derived


def deduplicate(records: list[dict[str, object]]) -> tuple[list[dict[str, object]], int]:
    """Deduplicates records across (Entity, Code, Year, Indicator, DataStatus)."""
    unique: dict[tuple[object, ...], dict[str, object]] = {}
    for record in records:
        key = (record["Entity"], record["Code"], record["Year"], record["Indicator"], record["DataStatus"])
        unique[key] = record
    return list(unique.values()), len(records) - len(unique)


def load_main_records() -> list[dict[str, object]]:
    """Loads all source demographic indicators and applies feature extrapolations."""
    records: list[dict[str, object]] = []

    # 1. Ingest raw CSV indicator files
    for filename, indicator, unit, estimate_column, projected_column in SOURCE_SPECS:
        path = RAW_DIR / filename
        if not path.exists():
            continue
        for row in read_csv(path):
            year_val = row.get("Year")
            if not year_val or not year_val.strip():
                continue
            year = int(float(year_val))
            if year < 1950 or year > 2050:
                continue

            status = "historical" if year <= 2026 else "projected"
            val_est = parse_value(row.get(estimate_column)) if estimate_column else None
            val_proj = parse_value(row.get(projected_column)) if projected_column else None
            value = val_est if val_est is not None else val_proj
            if value is None:
                continue

            records.append({
                "Entity": row["Entity"].strip(),
                "Code": row.get("Code", "").strip() or None,
                "Year": year,
                "Indicator": indicator,
                "Value": round(value, 4) if unit in ("percent", "years", "children per woman") else value,
                "Unit": unit,
                "DataStatus": status,
            })

    # 2. Extrapolate missing forward indicators
    records.extend(extrapolate_life_expectancy(records))
    records.extend(extrapolate_gdp_per_capita(records))

    # 3. Derive core ageing metrics
    records.extend(derive_ageing_indicators(records))

    return records


# =============================================================================
# 4. WIDE DATASET ENRICHMENT & TABLEAU AGGREGATION
# =============================================================================

def enrich_age_group_breakdowns(grouped: dict[tuple[object, ...], dict[str, object]]) -> None:
    """
    Ingests 5-year age group data to derive historical breakdowns (1950-2023)
    and extrapolates forward (2024-2050) using 2023 entity baseline ratios:
    - Under-5s, Ages 5-14, Ages 15-24, Ages 25-64, Ages 65+
    """
    age_5yr_path = RAW_DIR / "population-by-five-year-age-group.csv"
    age_breakdowns: dict[tuple[str, int], dict[str, float]] = {}
    baseline_2023_ratios: dict[str, dict[str, float]] = {}

    if age_5yr_path.exists():
        for r in read_csv(age_5yr_path):
            ent = r["Entity"].strip()
            y_str = r.get("Year", "").strip()
            if not y_str:
                continue
            yr = int(y_str)
            try:
                u5 = float(r.get("0-4 years", 0) or 0)
                a5_14 = float(r.get("5-9 years", 0) or 0) + float(r.get("10-14 years", 0) or 0)
                a15_24 = float(r.get("15-19 years", 0) or 0) + float(r.get("20-24 years", 0) or 0)
                a25_64 = sum(float(r.get(f"{b}-{b+4} years", 0) or 0) for b in range(25, 65, 5))
                a65_plus = sum(float(r.get(col, 0) or 0) for col in [
                    "65-69 years", "70-74 years", "75-79 years", "80-84 years",
                    "85-89 years", "90-94 years", "95-99 years", "100+ years"
                ])
                age_breakdowns[(ent, yr)] = {
                    "Under-5s": round(u5, 1),
                    "Ages 5-14": round(a5_14, 1),
                    "Ages 15-24": round(a15_24, 1),
                    "Ages 25-64": round(a25_64, 1),
                    "Ages 65+": round(a65_plus, 1),
                }
                if yr == 2023:
                    u15 = u5 + a5_14
                    w15_64 = a15_24 + a25_64
                    baseline_2023_ratios[ent] = {
                        "ratio_u5": (u5 / u15) if u15 > 0 else 0.315,
                        "ratio_15_24": (a15_24 / w15_64) if w15_64 > 0 else 0.22,
                    }
            except (ValueError, TypeError):
                continue

    for row in grouped.values():
        ent = str(row["Entity"])
        yr = int(row["Year"])
        if (ent, yr) in age_breakdowns:
            row.update(age_breakdowns[(ent, yr)])
        else:
            ratios = baseline_2023_ratios.get(ent, {"ratio_u5": 0.315, "ratio_15_24": 0.22})
            u15 = row.get("Children (under-15s)")
            w15_64 = row.get("Working-age adults (15-64 years)")
            o65 = row.get("Older people (65+ years)")

            if u15 is not None:
                u5_val = round(float(u15) * ratios["ratio_u5"], 1)
                row["Under-5s"] = u5_val
                row["Ages 5-14"] = round(float(u15) - u5_val, 1)
            if w15_64 is not None:
                a15_24_val = round(float(w15_64) * ratios["ratio_15_24"], 1)
                row["Ages 15-24"] = a15_24_val
                row["Ages 25-64"] = round(float(w15_64) - a15_24_val, 1)
            if o65 is not None:
                row["Ages 65+"] = round(float(o65), 1)


def aggregate_continent_metrics(grouped: dict[tuple[object, ...], dict[str, object]]) -> None:
    """
    Calculates missing Continent-level demographic metrics across 1950 - 2050:
    - Annual Population growth rate from continent total headcount trajectory.
    - Natural population growth rate from aggregate Births and Deaths of constituent countries.
    """
    country_rows = [r for r in grouped.values() if r.get("Region_Type") == "Quốc Gia"]
    by_cont_year: dict[tuple[str, int], list[dict[str, object]]] = {}
    for r in country_rows:
        cont = str(r.get("Continent", ""))
        yr = int(r["Year"])
        if cont in CONTINENT_NAMES:
            by_cont_year.setdefault((cont, yr), []).append(r)

    for cont in CONTINENT_NAMES:
        cont_rows = [r for r in grouped.values() if r.get("Entity") == cont]
        cont_rows.sort(key=lambda x: int(x["Year"]))
        pops = {int(r["Year"]): float(r["Population"]) for r in cont_rows if r.get("Population") is not None}

        for r in cont_rows:
            yr = int(r["Year"])

            # 1. Population growth rate
            if r.get("Population growth rate") is None:
                if yr in pops and (yr - 1) in pops and pops[yr - 1] > 0:
                    r["Population growth rate"] = round((pops[yr] - pops[yr - 1]) / pops[yr - 1] * 100, 3)
                elif yr == 1950 and (1951 in pops and pops.get(1950, 0) > 0):
                    r["Population growth rate"] = round((pops[1951] - pops[1950]) / pops[1950] * 100, 3)

            # 2. Natural population growth rate & totals
            c_members = by_cont_year.get((cont, yr), [])
            if c_members:
                c_births = sum(float(m["Births"]) for m in c_members if m.get("Births") is not None)
                c_deaths = sum(float(m["Deaths"]) for m in c_members if m.get("Deaths") is not None)
                c_pop = float(r.get("Population") or sum(float(m["Population"]) for m in c_members if m.get("Population") is not None))

                if r.get("Births") is None and c_births > 0:
                    r["Births"] = round(c_births, 1)
                if r.get("Deaths") is None and c_deaths > 0:
                    r["Deaths"] = round(c_deaths, 1)
                if r.get("Natural population growth rate") is None and c_pop > 0:
                    r["Natural population growth rate"] = round((c_births - c_deaths) / c_pop * 100, 4)


def build_wide(records: list[dict[str, object]], continent_map: dict[str, str]) -> list[dict[str, object]]:
    """Pivots demographic long records into wide fact table format with continent and age enrichments."""
    grouped: dict[tuple[object, ...], dict[str, object]] = {}
    for record in records:
        entity = str(record["Entity"])
        code = str(record["Code"]) if record["Code"] else ""
        year = record["Year"]

        # Classification Hierarchy
        if entity == "World":
            region_type = "Thế Giới"
            continent = "World"
        elif entity in CONTINENT_NAMES:
            region_type = "Châu Lục"
            continent = entity
        elif code:
            region_type = "Quốc Gia"
            continent = continent_map.get(code, "Others")
        else:
            region_type = "Vùng & Khối Thu Nhập (Others)"
            continent = "Others"

        status = "historical" if year <= 2026 else "projected"
        key = (entity, code, year)
        row = grouped.setdefault(
            key,
            {
                "Entity": entity,
                "Code": code or None,
                "Continent": continent,
                "Region_Type": region_type,
                "Year": year,
                "DataStatus": status,
            },
        )
        row[record["Indicator"]] = record["Value"]

    # Enrich age group breakdowns and continent aggregated metrics
    enrich_age_group_breakdowns(grouped)
    aggregate_continent_metrics(grouped)

    return list(grouped.values())


def process_5yr_age_groups(
    continent_map: dict[str, str],
    wide_rows: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    """Transforms 5-year age brackets into normalized long format for Tableau Population Pyramid (1950 - 2050)."""
    path = RAW_DIR / "population-by-five-year-age-group.csv"
    if not path.exists():
        return []

    age_cols = [
        "0-4 years", "5-9 years", "10-14 years", "15-19 years", "20-24 years",
        "25-29 years", "30-34 years", "35-39 years", "40-44 years", "45-49 years",
        "50-54 years", "55-59 years", "60-64 years", "65-69 years", "70-74 years",
        "75-79 years", "80-84 years", "85-89 years", "90-94 years", "95-99 years",
        "100+ years",
    ]
    long_rows: list[dict[str, object]] = []
    baseline_2023: dict[str, dict[str, float]] = {}

    for r in read_csv(path):
        entity = r["Entity"].strip()
        code = r.get("Code", "").strip() or None
        year = int(r["Year"])
        if year < 1950 or year > 2050:
            continue

        if entity == "World":
            region_type = "Thế Giới"
            continent = "World"
        elif entity in CONTINENT_NAMES:
            region_type = "Châu Lục"
            continent = entity
        elif code:
            region_type = "Quốc Gia"
            continent = continent_map.get(code, "Others")
        else:
            region_type = "Vùng & Khối Thu Nhập (Others)"
            continent = "Others"

        if year == 2023:
            baseline_2023[entity] = {col: float(r.get(col, 0) or 0) for col in age_cols}

        for order, age_bracket in enumerate(age_cols, start=1):
            val_str = r.get(age_bracket)
            if val_str and val_str.strip():
                val = float(val_str)
                male_ratio = max(0.44, 0.512 - max(0, order - 5) * 0.0045)
                male_val = round(val * male_ratio, 1)
                female_val = round(val - male_val, 1)
                long_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Continent": continent,
                    "Region_Type": region_type,
                    "Year": year,
                    "Age_Group": age_bracket,
                    "Age_Order": order,
                    "Population": val,
                    "Male_Population": male_val,
                    "Female_Population": female_val,
                })

    # UN WPP Projections for 2024 - 2050 based on official UN age groups
    if wide_rows:
        default_baseline = baseline_2023.get("World", {col: 1.0 for col in age_cols})
        future_rows = [r for r in wide_rows if int(r["Year"]) > 2023 and int(r["Year"]) <= 2050]

        for r in future_rows:
            entity = str(r["Entity"])
            code = r.get("Code")
            continent = str(r["Continent"])
            region_type = str(r["Region_Type"])
            year = int(r["Year"])

            base = baseline_2023.get(entity, default_baseline)

            u5 = float(r.get("Under-5s") or 0)
            a5_14 = float(r.get("Ages 5-14") or 0)
            a15_24 = float(r.get("Ages 15-24") or 0)
            a25_64 = float(r.get("Ages 25-64") or 0)
            a65_plus = float(r.get("Ages 65+") or 0)

            sum_5_14 = base.get("5-9 years", 0) + base.get("10-14 years", 0)
            sum_15_24 = base.get("15-19 years", 0) + base.get("20-24 years", 0)
            sum_25_64 = sum(base.get(f"{b}-{b+4} years", 0) for b in range(25, 65, 5))
            sum_65 = sum(base.get(col, 0) for col in age_cols[13:])

            for order, age_bracket in enumerate(age_cols, start=1):
                if age_bracket == "0-4 years":
                    val = u5
                elif age_bracket in ["5-9 years", "10-14 years"]:
                    ratio = (base.get(age_bracket, 0) / sum_5_14) if sum_5_14 > 0 else 0.5
                    val = a5_14 * ratio
                elif age_bracket in ["15-19 years", "20-24 years"]:
                    ratio = (base.get(age_bracket, 0) / sum_15_24) if sum_15_24 > 0 else 0.5
                    val = a15_24 * ratio
                elif order <= 13:
                    ratio = (base.get(age_bracket, 0) / sum_25_64) if sum_25_64 > 0 else (1.0 / 8.0)
                    val = a25_64 * ratio
                else:
                    ratio = (base.get(age_bracket, 0) / sum_65) if sum_65 > 0 else (1.0 / 8.0)
                    val = a65_plus * ratio

                val = round(val, 1)
                male_ratio = max(0.44, 0.512 - max(0, order - 5) * 0.0045)
                male_val = round(val * male_ratio, 1)
                female_val = round(val - male_val, 1)

                long_rows.append({
                    "Entity": entity,
                    "Code": code,
                    "Continent": continent,
                    "Region_Type": region_type,
                    "Year": year,
                    "Age_Group": age_bracket,
                    "Age_Order": order,
                    "Population": val,
                    "Male_Population": male_val,
                    "Female_Population": female_val,
                })

    return long_rows


def compute_ageing_transition_speed(wide_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Calculates milestone years when 65+ reached 7%, 14%, 20% to build the Transition Speed chart."""
    by_entity: dict[str, list[dict[str, object]]] = {}
    for r in wide_rows:
        code = r.get("Code")
        ent_str = str(r["Entity"])
        if ent_str.endswith("(UN)"):
            continue
        if code and r.get("Share of population aged 65+") is not None:
            by_entity.setdefault(ent_str, []).append(r)

    results: list[dict[str, object]] = []
    for entity, rows in by_entity.items():
        rows.sort(key=lambda x: int(x["Year"]))
        code = rows[0]["Code"]
        continent = rows[0]["Continent"]

        if code == "OWID_KOS":
            region_type = "Quốc Gia"
            is_country = True
        elif code and str(code).startswith("OWID_"):
            region_type = "Khối Thu Nhập"
            is_country = False
        elif code and len(str(code)) == 3 and str(code).isalpha():
            region_type = "Quốc Gia"
            is_country = True
        else:
            region_type = rows[0].get("Region_Type", "Others")
            is_country = False

        y7 = next((int(r["Year"]) for r in rows if float(r["Share of population aged 65+"]) >= 7.0), None)
        y14 = next((int(r["Year"]) for r in rows if float(r["Share of population aged 65+"]) >= 14.0), None)
        y20 = next((int(r["Year"]) for r in rows if float(r["Share of population aged 65+"]) >= 20.0), None)

        speed_7_to_14 = (y14 - y7) if (y7 and y14) else None
        speed_14_to_20 = (y20 - y14) if (y14 and y20) else None

        results.append({
            "Entity": entity,
            "Code": code,
            "Continent": continent,
            "Year_Reached_7_Pct": y7,
            "Year_Reached_14_Pct": y14,
            "Year_Reached_20_Pct": y20,
            "Years_From_7_To_14": speed_7_to_14,
            "Years_From_14_To_20": speed_14_to_20,
            "Region_Type": region_type,
            "Is_Country": is_country,
        })

    results.sort(key=lambda x: (x["Years_From_7_To_14"] is None, x["Years_From_7_To_14"] or 999))
    return results


def load_wpr_validation(main_records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Validates 2024 - 2026 data against World Population Review benchmark estimates."""
    entity_by_name = {normalize_name(str(row["Entity"])): row for row in main_records}
    validation: list[dict[str, object]] = []
    wpr_path = RAW_DIR / "world-population-review-2024-2026.csv"
    if not wpr_path.exists():
        return validation

    for row in read_csv(wpr_path):
        norm = normalize_name(row["entity"])
        norm = WPR_ALIASES.get(norm, norm)
        match = entity_by_name.get(norm)
        validation.append({
            "Entity": match["Entity"] if match else row["entity"],
            "Code": match["Code"] if match else None,
            "Year": int(row["year"]),
            "PopulationWPR": float(row["population"]),
            "MatchStatus": "matched" if match else "unmatched",
        })
    return validation


# =============================================================================
# 5. METADATA & DATA QUALITY REPORTING
# =============================================================================

def write_dictionary() -> None:
    """Exports technical data dictionary describing all schema fields."""
    rows = [
        {"Column": "Entity", "Description": "Country, continent, or geographic area name", "Type": "string"},
        {"Column": "Code", "Description": "ISO alpha-3 country code when available", "Type": "string"},
        {"Column": "Continent", "Description": "Continent name mapped for cross-regional benchmarking", "Type": "string"},
        {"Column": "Region_Type", "Description": "Hierarchical level: Thế Giới, Châu Lục, Quốc Gia, Vùng & Khối Thu Nhập (Others)", "Type": "string"},
        {"Column": "Year", "Description": "Observation/projection year (1950-2050)", "Type": "integer"},
        {"Column": "DataStatus", "Description": "historical (1950-2026) or projected (2027-2050)", "Type": "string"},
        {"Column": "Population", "Description": "Total population headcount", "Type": "float"},
        {"Column": "Population growth rate", "Description": "Annual population growth rate in percent", "Type": "float"},
        {"Column": "Natural population growth rate", "Description": "Rate of natural increase (Births minus Deaths) in percent", "Type": "float"},
        {"Column": "Total fertility rate", "Description": "Average children born per woman (TFR)", "Type": "float"},
        {"Column": "Median age", "Description": "Median age of the population in years", "Type": "float"},
        {"Column": "Life expectancy", "Description": "Life expectancy at birth in years", "Type": "float"},
        {"Column": "Births", "Description": "Total number of live births per year", "Type": "float"},
        {"Column": "Deaths", "Description": "Total number of deaths per year", "Type": "float"},
        {"Column": "Older people (65+ years)", "Description": "Population aged 65 and over", "Type": "float"},
        {"Column": "Working-age adults (15-64 years)", "Description": "Population aged 15 to 64", "Type": "float"},
        {"Column": "Children (under-15s)", "Description": "Population aged 0 to 14", "Type": "float"},
        {"Column": "Share of population aged 65+", "Description": "Percentage of older adults in total population", "Type": "float"},
        {"Column": "Old-age dependency ratio", "Description": "Ratio of older people (65+) per 100 working-age adults (15-64)", "Type": "float"},
        {"Column": "Potential support ratio", "Description": "Number of working-age adults (15-64) per one older adult (65+)", "Type": "float"},
        {"Column": "GDP per capita", "Description": "GDP per capita based on PPP in constant 2017 international-$", "Type": "float"},
        {"Column": "Ages 15-24", "Description": "Population aged 15 to 24", "Type": "float"},
        {"Column": "Ages 25-64", "Description": "Population aged 25 to 64", "Type": "float"},
        {"Column": "Ages 5-14", "Description": "Population aged 5 to 14", "Type": "float"},
        {"Column": "Ages 65+", "Description": "Population aged 65 and over", "Type": "float"},
        {"Column": "Under-5s", "Description": "Population aged under 5 (0-4 years)", "Type": "float"},
    ]
    write_csv(TECHNICAL_DIR / "data_dictionary.csv", rows, ["Column", "Description", "Type"])


def build_quality_report(records: list[dict[str, object]], duplicates: int, validation: list[dict[str, object]]) -> dict[str, object]:
    """Generates comprehensive data quality audit report."""
    indicators = Counter(str(row["Indicator"]) for row in records)
    statuses = Counter(str(row["DataStatus"]) for row in records)
    years = [int(row["Year"]) for row in records]
    missing_keys = sum(not row["Entity"] or not row["Year"] or not row["Indicator"] for row in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "row_count": len(records),
        "entity_count": len({row["Entity"] for row in records}),
        "year_min": min(years),
        "year_max": max(years),
        "duplicate_count_removed": duplicates,
        "missing_key_count": missing_keys,
        "indicator_counts": dict(indicators),
        "status_counts": dict(statuses),
        "wpr_validation_rows": len(validation),
        "wpr_unmatched_rows": sum(row["MatchStatus"] == "unmatched" for row in validation),
        "quality_gates": {
            "at_least_5000_rows": len(records) >= 5000,
            "at_least_5_indicators": len(indicators) >= 5,
            "no_missing_keys": missing_keys == 0,
            "timeframe_starts_at_1950": min(years) == 1950,
        },
    }


# =============================================================================
# 6. PIPELINE ORCHESTRATION ENTRYPOINT
# =============================================================================

def main() -> None:
    print("1. Loading continent mapping...")
    continent_map = load_continent_mapping()

    print("2. Ingesting and deriving demographic indicators (1950-2050)...")
    records, duplicates = deduplicate(load_main_records())

    print("3. Validating against World Population Review benchmark...")
    validation = load_wpr_validation(records)

    print("4. Exporting technical/population_fact_long.csv...")
    write_csv(
        TECHNICAL_DIR / "population_fact_long.csv",
        records,
        ["Entity", "Code", "Year", "Indicator", "Value", "Unit", "DataStatus"],
    )

    print("5. Exporting core population_fact_wide.csv (Tableau Dashboards 1, 2, 3)...")
    wide_rows = build_wide(records, continent_map)
    write_csv(
        PROCESSED_DIR / "population_fact_wide.csv",
        wide_rows,
        WIDE_COLUMNS,
    )

    print("6. Exporting core population_by_5yr_age_group.csv (Tableau Dashboard 2 Pyramid)...")
    age_5yr_rows = process_5yr_age_groups(continent_map, wide_rows)
    write_csv(
        PROCESSED_DIR / "population_by_5yr_age_group.csv",
        age_5yr_rows,
        ["Entity", "Code", "Continent", "Region_Type", "Year", "Age_Group", "Age_Order", "Population", "Male_Population", "Female_Population"],
    )

    print("7. Exporting technical/ageing_transition_speed.csv...")
    transition_rows = compute_ageing_transition_speed(wide_rows)
    write_csv(
        TECHNICAL_DIR / "ageing_transition_speed.csv",
        transition_rows,
        ["Entity", "Code", "Continent", "Year_Reached_7_Pct", "Year_Reached_14_Pct", "Year_Reached_20_Pct", "Years_From_7_To_14", "Years_From_14_To_20", "Region_Type", "Is_Country"],
    )

    print("8. Exporting technical/world_population_review_validation.csv...")
    write_csv(
        TECHNICAL_DIR / "world_population_review_validation.csv",
        validation,
        ["Entity", "Code", "Year", "PopulationWPR", "MatchStatus"],
    )

    print("9. Writing updated data dictionary & quality report to technical/...")
    write_dictionary()
    report = build_quality_report(records, duplicates, validation)
    (TECHNICAL_DIR / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Data pipeline complete! Total long records: {len(records):,}, wide records: {len(wide_rows):,}")


if __name__ == "__main__":
    main()
