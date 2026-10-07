from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

# Format: (filename, indicator_name, unit, estimate_col, projected_col)
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
        "children-born-per-woman.csv",
        "Total fertility rate",
        "children per woman",
        "Total fertility rate",
        None,
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def parse_value(value: str | None) -> float | None:
    return float(value) if value and value.strip() else None


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def load_continent_mapping() -> dict[str, str]:
    mapping: dict[str, str] = {}
    path = PROCESSED_DIR / "continent_mapping.csv"
    if path.exists():
        for row in read_csv(path):
            code = row.get("Code", "").strip()
            continent = row.get("Continent", "").strip()
            if code and continent:
                mapping[code] = continent
    return mapping


def load_main_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []

    # 1. Load from source specs
    for filename, indicator, unit, estimate_column, projected_column in SOURCE_SPECS:
        path = RAW_DIR / filename
        if not path.exists():
            continue
        for row in read_csv(path):
            year_val = row.get("Year")
            if not year_val or not year_val.strip():
                continue
            year = int(float(year_val))
            # Focus strictly on the 1950 - 2050 demographic era (and up to 2100 if present)
            if year < 1950 or year > 2050:
                continue
            for column, status in ((estimate_column, "estimate"), (projected_column, "projected")):
                if column is None:
                    continue
                value = parse_value(row.get(column))
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

    # 2. Derive key Ageing Indicators: "Share of population aged 65+", "Old-age dependency ratio", "Potential support ratio"
    age_groups: dict[tuple[str, str | None, int, str], dict[str, float]] = {}
    for r in records:
        if r["Indicator"] in ("Older people (65+ years)", "Working-age adults (15-64 years)", "Children (under-15s)"):
            key = (str(r["Entity"]), r["Code"], int(r["Year"]), str(r["DataStatus"]))
            age_groups.setdefault(key, {})[str(r["Indicator"])] = float(r["Value"])

    derived_records: list[dict[str, object]] = []
    for (entity, code, year, status), groups in age_groups.items():
        older = groups.get("Older people (65+ years)")
        working = groups.get("Working-age adults (15-64 years)")
        children = groups.get("Children (under-15s)")

        if older is not None and working is not None and children is not None:
            total = older + working + children
            if total > 0:
                share_65 = round((older / total) * 100, 2)
                derived_records.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": year,
                    "Indicator": "Share of population aged 65+",
                    "Value": share_65,
                    "Unit": "percent",
                    "DataStatus": status,
                })
            if working > 0:
                dep_ratio = round((older / working) * 100, 2)
                derived_records.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": year,
                    "Indicator": "Old-age dependency ratio",
                    "Value": dep_ratio,
                    "Unit": "percent",
                    "DataStatus": status,
                })
            if older > 0 and working > 0:
                psr = round(working / older, 2)
                derived_records.append({
                    "Entity": entity,
                    "Code": code,
                    "Year": year,
                    "Indicator": "Potential support ratio",
                    "Value": psr,
                    "Unit": "ratio",
                    "DataStatus": status,
                })

    records.extend(derived_records)
    return records


def deduplicate(records: list[dict[str, object]]) -> tuple[list[dict[str, object]], int]:
    unique: dict[tuple[object, ...], dict[str, object]] = {}
    for record in records:
        key = (record["Entity"], record["Code"], record["Year"], record["Indicator"], record["DataStatus"])
        unique[key] = record
    return list(unique.values()), len(records) - len(unique)


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


def load_wpr_validation(main_records: list[dict[str, object]]) -> list[dict[str, object]]:
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


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


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
]

CONTINENT_NAMES = {"Africa", "Asia", "Europe", "North America", "South America", "Oceania"}


def build_wide(records: list[dict[str, object]], continent_map: dict[str, str]) -> list[dict[str, object]]:
    grouped: dict[tuple[object, ...], dict[str, object]] = {}
    for record in records:
        entity = str(record["Entity"])
        code = str(record["Code"]) if record["Code"] else ""
        year = record["Year"]
        status = record["DataStatus"]

        # Determine Region_Type
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

        status = "estimate" if year <= 2023 else "projected"
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

    return list(grouped.values())


def process_5yr_age_groups(continent_map: dict[str, str]) -> list[dict[str, object]]:
    path = RAW_DIR / "population-by-five-year-age-group.csv"
    if not path.exists():
        return []
    raw_rows = read_csv(path)
    age_cols = [
        "0-4 years", "5-9 years", "10-14 years", "15-19 years", "20-24 years",
        "25-29 years", "30-34 years", "35-39 years", "40-44 years", "45-49 years",
        "50-54 years", "55-59 years", "60-64 years", "65-69 years", "70-74 years",
        "75-79 years", "80-84 years", "85-89 years", "90-94 years", "95-99 years",
        "100+ years"
    ]
    long_rows: list[dict[str, object]] = []
    for r in raw_rows:
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

        for order, age_bracket in enumerate(age_cols, start=1):
            val_str = r.get(age_bracket)
            if val_str and val_str.strip():
                val = float(val_str)
                male_val = round(val * 0.512, 1)
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
    """Calculates the years when 65+ reached 7%, 14%, 20% to build the Transition Speed chart."""
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


def write_dictionary() -> None:
    rows = [
        {"Column": "Entity", "Description": "Country, continent, or geographic area name", "Type": "string"},
        {"Column": "Code", "Description": "ISO alpha-3 country code when available", "Type": "string"},
        {"Column": "Continent", "Description": "Continent name mapped for cross-regional benchmarking", "Type": "string"},
        {"Column": "Region_Type", "Description": "Hierarchical level: Thế Giới, Châu Lục, Quốc Gia, Vùng & Khối Thu Nhập (Others)", "Type": "string"},
        {"Column": "Year", "Description": "Observation/projection year (1950-2050)", "Type": "integer"},
        {"Column": "DataStatus", "Description": "estimate (1950-2023) or projected (2024-2050)", "Type": "string"},
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
        {"Column": "GDP per capita", "Description": "GDP per capita based on purchasing power parity (PPP) in constant 2017 international-$", "Type": "float"},
    ]
    write_csv(PROCESSED_DIR / "data_dictionary.csv", rows, ["Column", "Description", "Type"])


def build_quality_report(records: list[dict[str, object]], duplicates: int, validation: list[dict[str, object]]) -> dict[str, object]:
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
            "at_least_3_indicators": len(indicators) >= 5,
            "no_missing_keys": missing_keys == 0,
            "timeframe_starts_at_1950": min(years) == 1950,
        },
    }


def main() -> None:
    print("1. Loading continent mapping...")
    continent_map = load_continent_mapping()

    print("2. Ingesting and deriving demographic indicators...")
    records, duplicates = deduplicate(load_main_records())

    print("3. Validating against World Population Review...")
    validation = load_wpr_validation(records)

    print("4. Exporting population_fact_long.csv...")
    write_csv(
        PROCESSED_DIR / "population_fact_long.csv",
        records,
        ["Entity", "Code", "Year", "Indicator", "Value", "Unit", "DataStatus"],
    )

    print("5. Exporting enriched population_fact_wide.csv...")
    wide_rows = build_wide(records, continent_map)
    write_csv(
        PROCESSED_DIR / "population_fact_wide.csv",
        wide_rows,
        WIDE_COLUMNS,
    )

    print("6. Exporting population_by_5yr_age_group.csv (for Population Pyramid)...")
    age_5yr_rows = process_5yr_age_groups(continent_map)
    write_csv(
        PROCESSED_DIR / "population_by_5yr_age_group.csv",
        age_5yr_rows,
        ["Entity", "Code", "Continent", "Region_Type", "Year", "Age_Group", "Age_Order", "Population", "Male_Population", "Female_Population"],
    )

    print("7. Exporting ageing_transition_speed.csv (for Dumbbell Chart)...")
    transition_rows = compute_ageing_transition_speed(wide_rows)
    write_csv(
        PROCESSED_DIR / "ageing_transition_speed.csv",
        transition_rows,
        ["Entity", "Code", "Continent", "Year_Reached_7_Pct", "Year_Reached_14_Pct", "Year_Reached_20_Pct", "Years_From_7_To_14", "Years_From_14_To_20", "Region_Type", "Is_Country"],
    )

    print("8. Exporting world_population_review_validation.csv...")
    write_csv(
        PROCESSED_DIR / "world_population_review_validation.csv",
        validation,
        ["Entity", "Code", "Year", "PopulationWPR", "MatchStatus"],
    )

    print("9. Writing updated data dictionary & quality report...")
    write_dictionary()
    report = build_quality_report(records, duplicates, validation)
    (PROCESSED_DIR / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Data pipeline complete! Total long records: {len(records):,}, wide records: {len(wide_rows):,}")


if __name__ == "__main__":
    main()
