from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "https://worldpopulationreview.com"
COUNTRIES_URL = f"{BASE_URL}/countries"
TARGET_YEARS = (2024, 2025, 2026)
EXCLUDED_SLUGS = {"by-gdp"}
USER_AGENT = "population-trends-project/1.0"
COUNTRY_LINK_PATTERN = re.compile(r'href=["\'](?:https://worldpopulationreview\.com)?/countries/([^/"?#]+)["\']')
POPULATION_PATTERN = re.compile(r'\{"year":(2024|2025|2026),"population":([0-9]+(?:\.[0-9]+)?)')


@dataclass(frozen=True)
class Country:
    slug: str
    name: str


@dataclass(frozen=True)
class PopulationRecord:
    entity: str
    slug: str
    code: str
    year: int
    population: int
    source_url: str


def fetch_text(url: str, retries: int, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8")
        except (HTTPError, URLError, TimeoutError) as error:
            last_error = error
            if attempt < retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Could not fetch {url}: {last_error}")


def display_name(slug: str) -> str:
    return " ".join(word.capitalize() for word in slug.replace("-", " ").split())


def get_countries(page: str) -> list[Country]:
    slugs = sorted(set(COUNTRY_LINK_PATTERN.findall(page)) - EXCLUDED_SLUGS)
    return [Country(slug=slug, name=display_name(slug)) for slug in slugs]


def parse_population_records(country: Country, page: str) -> list[PopulationRecord]:
    decoded_page = html.unescape(page)
    values: dict[int, int] = {}
    for year_text, population_text in POPULATION_PATTERN.findall(decoded_page):
        year = int(year_text)
        values.setdefault(year, round(float(population_text)))

    source_url = f"{BASE_URL}/countries/{country.slug}"
    return [
        PopulationRecord(
            entity=country.name,
            slug=country.slug,
            code=country.slug,
            year=year,
            population=values[year],
            source_url=source_url,
        )
        for year in TARGET_YEARS
        if year in values
    ]


def write_records(path: Path, records: list[PopulationRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=PopulationRecord.__annotations__.keys())
        writer.writeheader()
        writer.writerows(record.__dict__ for record in records)


def write_metadata(path: Path, records: list[PopulationRecord], errors: list[dict[str, str]]) -> None:
    metadata = {
        "source": "World Population Review",
        "source_url": COUNTRIES_URL,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "years": list(TARGET_YEARS),
        "country_count": len({record.slug for record in records}),
        "record_count": len(records),
        "error_count": len(errors),
        "notes": [
            "Population values are extracted from embedded page data and rounded to whole people.",
            "The source includes countries, dependent territories, special administrative regions and disputed territories.",
            "Country names and codes in this file are URL-based labels from the source page.",
        ],
        "errors": errors,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def crawl(output: Path, delay: float, retries: int, timeout: int) -> tuple[int, int]:
    countries = get_countries(fetch_text(COUNTRIES_URL, retries, timeout))
    records: list[PopulationRecord] = []
    errors: list[dict[str, str]] = []

    for index, country in enumerate(countries):
        url = f"{BASE_URL}/countries/{country.slug}"
        try:
            page_records = parse_population_records(country, fetch_text(url, retries, timeout))
            if len(page_records) != len(TARGET_YEARS):
                raise ValueError(f"Expected {len(TARGET_YEARS)} years, found {len(page_records)}")
            records.extend(page_records)
        except (RuntimeError, ValueError) as error:
            errors.append({"slug": country.slug, "url": url, "error": str(error)})
        print(f"[{index + 1}/{len(countries)}] {country.name}")
        if index + 1 < len(countries):
            time.sleep(delay)

    write_records(output, records)
    write_metadata(output.with_suffix(".metadata.json"), records, errors)
    return len(countries), len(errors)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/raw/world-population-review-2024-2026.csv"),
    )
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    country_count, error_count = crawl(
        output=arguments.output,
        delay=arguments.delay,
        retries=arguments.retries,
        timeout=arguments.timeout,
    )
    print(f"Completed: {country_count} countries, {error_count} errors")


if __name__ == "__main__":
    main()