# Population - Data package

This data package contains the data that powers the chart ["Population"](https://ourworldindata.org/grapher/population-with-un-projections?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website.

### Active Filters

A filtered subset of the full data was downloaded. The following filters were applied:

## CSV structure

Each row is an observation for an entity (usually a country or region) at a timepoint.

- "Entity" — the name of the entity, e.g. "United States".
- "Code" — our internal entity code. For most countries this is the [ISO alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code, e.g. "USA"; historical and other non-standard entities get a custom code.
- "Year" or "Day" — the timepoint. Annual data has a "Year" column holding an integer year; otherwise a "Day" column holds a date string in the form "YYYY-MM-DD".
- Every remaining column is a data column, each one a time series. Downloaded with the "full data" option each corresponds to one time series below; with "only selected data visible in the chart" they are transformed depending on the chart type, so the correspondence may be less direct.


## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc.

## How we process data at Our World in Data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stitch together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

Preparing this data involves several processing steps. Depending on the data, this can include standardizing country names and world region definitions, converting units, calculating derived indicators such as per capita measures, as well as adding or adapting metadata such as the name or the description given to an indicator.
[Read about our data pipeline](https://docs.owid.io/projects/etl/).

## Detailed information about each time series


### Population – UN WPP
Total population, measured on 1 July of the year shown.
Last updated: July 12, 2024  
Next expected update: July 2027  
Date range: 1950–2023  
Unit: people  
Source: UN, World Population Prospects (2024) – processed by Our World in Data  

#### How to cite this data

UN, World Population Prospects (2024) – processed by Our World in Data

#### Notes on our processing step for this indicator
The UN publishes population by single year of age. We aggregate these into the broader age groups shown here (e.g. 0–14, 15–64, 65+, 18+, 15–49). Our continental aggregates (Africa, Asia, Europe, North America, South America, Oceania) are computed by summing across countries, and may differ slightly from regional aggregates the UN publishes directly, which use a different country grouping.


### Population – with medium scenario projections – UN WPP
Total population, measured on 1 July of the year shown.  Future projections are based on the UN's medium scenario.
Last updated: July 12, 2024  
Next expected update: July 2027  
Date range: 2024–2100  
Unit: people  
Source: UN, World Population Prospects (2024) – processed by Our World in Data  

#### How to cite this data

UN, World Population Prospects (2024) – processed by Our World in Data

#### Notes on our processing step for this indicator
The UN publishes population by single year of age. We aggregate these into the broader age groups shown here (e.g. 0–14, 15–64, 65+, 18+, 15–49). Our continental aggregates (Africa, Asia, Europe, North America, South America, Oceania) are computed by summing across countries, and may differ slightly from regional aggregates the UN publishes directly, which use a different country grouping.


## Sources

These are the sources behind the data in this package. Each time series above names the ones it draws on in its citation.

### United Nations – World Population Prospects

World Population Prospects 2024 is the 28th edition of the official estimates and projections of the global population that have been published by the United Nations since 1951. The estimates are based on all available sources of data on population size and levels of fertility, mortality and international migration for 237 countries or areas. If you have questions about this dataset, please refer to [their FAQ](https://population.un.org/wpp/faqs). You can also explore [data sources](https://population.un.org/wpp/data-sources) for each country or visit [their main page](https://population.un.org/wpp/) for more details.

Producer: United Nations  
Published: 2024-07-11  
Retrieved on: 2024-07-11  
Retrieved from: https://population.un.org/wpp/downloads/  
Direct download: https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz  
License: CC BY 3.0 IGO (https://population.un.org/wpp/downloads/)  

Citation: United Nations, Department of Economic and Social Affairs, Population Division (2024). World Population Prospects 2024, Online Edition.

### United Nations – World Population Prospects – Interim Update

World Population Prospects 2024 is the 28th edition of the official estimates and projections of the global population that have been published by the United Nations since 1951. The estimates are based on all available sources of data on population size and levels of fertility, mortality and international migration for 237 countries or areas. If you have questions about this dataset, please refer to [their FAQ](https://population.un.org/wpp/faqs). You can also explore [data sources](https://population.un.org/wpp/data-sources) for each country or visit [their main page](https://population.un.org/wpp/) for more details.

This is an interim update containing revised medium-variant estimates and projections for Togo.

Producer: United Nations  
Published: 2026-01-19  
Retrieved on: 2026-03-31  
Retrieved from: https://population.un.org/wpp/downloads/  
Direct download: https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/WPP2024_CSV_files_update.zip  
License: CC BY 3.0 IGO (https://population.un.org/wpp/downloads/)  

Citation: United Nations, Department of Economic and Social Affairs, Population Division (2024). World Population Prospects 2024, Online Edition.

    