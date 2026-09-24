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
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def parse_value(value: str | None) -> float | None:
    return float(value) if value and value.strip() else None


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def load_main_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []

    # 1. Load from source specs
    for filename, indicator, unit, estimate_column, projected_column in SOURCE_SPECS:
        path = RAW_DIR / filename
        if not path.exists():
            continue
        for row in read_csv(path):
            year = int(row["Year"])
            # Focus strictly on the 1950 - 2100 demographic era
            if year < 1950:
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
                    "Source": "UN WPP 2024 (OWID)",
                })

    # 2. Derive key Ageing Indicators: "Share of population aged 65+" and "Old-age dependency ratio"
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
                    "Source": "UN WPP 2024 (OWID)",
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
                    "Source": "UN WPP 2024 (OWID)",
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
    "Year",
    "DataStatus",
    "Population",
    "Population growth rate",
    "Total fertility rate",
    "Median age",
    "Life expectancy",
    "Older people (65+ years)",
    "Working-age adults (15-64 years)",
    "Children (under-15s)",
    "Share of population aged 65+",
    "Old-age dependency ratio",
]


def build_wide(records: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[object, ...], dict[str, object]] = {}
    for record in records:
        key = (record["Entity"], record["Code"], record["Year"], record["DataStatus"])
        row = grouped.setdefault(
            key,
            {"Entity": record["Entity"], "Code": record["Code"], "Year": record["Year"], "DataStatus": record["DataStatus"]},
        )
        row[record["Indicator"]] = record["Value"]
    return list(grouped.values())


def write_dictionary() -> None:
    rows = [
        {"Column": "Entity", "Description": "Country or area name", "Type": "string"},
        {"Column": "Code", "Description": "ISO alpha-3 code when available", "Type": "string"},
        {"Column": "Year", "Description": "Observation year (1950-2100)", "Type": "integer"},
        {"Column": "Indicator", "Description": "Demographic or Ageing indicator name", "Type": "string"},
        {"Column": "Value", "Description": "Indicator value", "Type": "float"},
        {"Column": "Unit", "Description": "Measurement unit (people, percent, years, children per woman)", "Type": "string"},
        {"Column": "DataStatus", "Description": "estimate (1950-2023) or projected (2024-2100)", "Type": "string"},
        {"Column": "Source", "Description": "Data provider and processing", "Type": "string"},
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
    records, duplicates = deduplicate(load_main_records())
    validation = load_wpr_validation(records)
    write_csv(
        PROCESSED_DIR / "population_fact_long.csv",
        records,
        ["Entity", "Code", "Year", "Indicator", "Value", "Unit", "DataStatus", "Source"],
    )
    write_csv(
        PROCESSED_DIR / "population_fact_wide.csv",
        build_wide(records),
        WIDE_COLUMNS,
    )
    write_csv(
        PROCESSED_DIR / "world_population_review_validation.csv",
        validation,
        ["Entity", "Code", "Year", "PopulationWPR", "MatchStatus"],
    )
    write_dictionary()
    report = build_quality_report(records, duplicates, validation)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
