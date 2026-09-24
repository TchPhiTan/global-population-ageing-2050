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

SOURCE_SPECS = (
    ("population-with-un-projections.csv", "Population", "people", "Population", "Population (Projected)"),
    ("population-growth-rates.csv", "Population growth rate", "percent", "Population growth rate", "Population growth rate (%) (Projected)"),
    ("children-born-per-woman.csv", "Total fertility rate", "children per woman", "Total fertility rate", None),
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
    for filename, indicator, unit, estimate_column, projected_column in SOURCE_SPECS:
        for row in read_csv(RAW_DIR / filename):
            for column, status in ((estimate_column, "estimate"), (projected_column, "projected")):
                if column is None:
                    continue
                value = parse_value(row.get(column))
                if value is None:
                    continue
                records.append({
                    "Entity": row["Entity"].strip(),
                    "Code": row.get("Code", "").strip() or None,
                    "Year": int(row["Year"]),
                    "Indicator": indicator,
                    "Value": value,
                    "Unit": unit,
                    "DataStatus": status,
                    "Source": "UN WPP 2024 processed by OWID",
                    "SourceUrl": "https://ourworldindata.org/grapher/population-with-un-projections",
                })
    return records


def deduplicate(records: list[dict[str, object]]) -> tuple[list[dict[str, object]], int]:
    unique: dict[tuple[object, ...], dict[str, object]] = {}
    for record in records:
        key = tuple(record[field] for field in ("Entity", "Code", "Year", "Indicator", "DataStatus"))
        unique[key] = record
    return list(unique.values()), len(records) - len(unique)


def load_wpr_validation(main_records: list[dict[str, object]]) -> list[dict[str, object]]:
    entity_by_name = {normalize_name(str(row["Entity"])): row for row in main_records}
    validation: list[dict[str, object]] = []
    for row in read_csv(RAW_DIR / "world-population-review-2024-2026.csv"):
        match = entity_by_name.get(normalize_name(row["entity"]))
        validation.append({
            "Entity": match["Entity"] if match else row["entity"],
            "Code": match["Code"] if match else None,
            "Year": int(row["year"]),
            "PopulationWPR": float(row["population"]),
            "SourceUrl": row["source_url"],
            "MatchStatus": "matched" if match else "unmatched",
        })
    return validation


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def build_wide(records: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[object, ...], dict[str, object]] = {}
    for record in records:
        key = (record["Entity"], record["Code"], record["Year"], record["DataStatus"])
        row = grouped.setdefault(key, {"Entity": record["Entity"], "Code": record["Code"], "Year": record["Year"], "DataStatus": record["DataStatus"]})
        row[record["Indicator"]] = record["Value"]
    return list(grouped.values())


def write_dictionary() -> None:
    rows = [
        {"Column": "Entity", "Description": "Country or area name", "Type": "string"},
        {"Column": "Code", "Description": "ISO alpha-3 code when available", "Type": "string"},
        {"Column": "Year", "Description": "Observation year", "Type": "integer"},
        {"Column": "Indicator", "Description": "Population indicator", "Type": "string"},
        {"Column": "Value", "Description": "Indicator value", "Type": "float"},
        {"Column": "Unit", "Description": "Measurement unit", "Type": "string"},
        {"Column": "DataStatus", "Description": "estimate or projected", "Type": "string"},
        {"Column": "Source", "Description": "Data provider and processing", "Type": "string"},
        {"Column": "SourceUrl", "Description": "Source reference", "Type": "string"},
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
            "at_least_3_indicators": len(indicators) >= 3,
            "no_missing_keys": missing_keys == 0,
        },
    }


def main() -> None:
    records, duplicates = deduplicate(load_main_records())
    validation = load_wpr_validation(records)
    write_csv(PROCESSED_DIR / "population_fact_long.csv", records, ["Entity", "Code", "Year", "Indicator", "Value", "Unit", "DataStatus", "Source", "SourceUrl"])
    write_csv(PROCESSED_DIR / "population_fact_wide.csv", build_wide(records), ["Entity", "Code", "Year", "DataStatus", "Population", "Population growth rate", "Total fertility rate"])
    write_csv(PROCESSED_DIR / "world_population_review_validation.csv", validation, ["Entity", "Code", "Year", "PopulationWPR", "SourceUrl", "MatchStatus"])
    write_dictionary()
    report = build_quality_report(records, duplicates, validation)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
