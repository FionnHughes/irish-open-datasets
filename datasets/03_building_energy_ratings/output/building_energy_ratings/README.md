---
license: cc-by-4.0
language:
- en
tags:
- ireland
- energy
- housing
- ber
- seai
- buildings
- sustainability
size_categories:
- 1M<n<10M
pretty_name: Irish Building Energy Ratings
---

# Irish Building Energy Ratings (BER)

Every BER cert ever issued in Ireland. About 1.4 million homes, 211 fields per cert: A-G rating, kWh/m²/yr, what fuel they burn, wall U-values, floor area, the lot.

## Why this dataset exists

SEAI hides this data behind an ASP.NET form button on their BER Research Tool. Click "Download All Data" and you get a 250MB zipped tab-separated file. No API, no static URL you can curl. Annoying. So I scraped it and flattened it into a clean CSV and Parquet you can `pd.read_csv` straight away.

## Columns (highlights)

| Column | Description |
|--------|-------------|
| countyname | Irish county the dwelling is in |
| dwellingtypedescr | Detached, semi-detached, apartment, etc. |
| year_of_construction | Year the dwelling was built |
| energyrating | Letter rating (A1, A2, B1 ... G) |
| berrating | Numeric kWh/m²/yr |
| co2rating | kg CO₂/m²/yr |
| mainspaceheatingfuel | Main fuel for space heating |
| mainwaterheatingfuel | Main fuel for water heating |
| groundfloorarea(sq_m) | Floor area, square metres |
| nostoreys | Number of storeys |
| dateofassessment | When the BER assessment was done |
| structuretype | Cavity wall, solid, timber frame, etc. |

The other 199 columns are mostly U-values, boiler details and mechanical stuff. Full schema is in the parquet file's metadata.

## Files

- `building_energy_ratings.csv` (1.3 GB) - flat UTF-8 CSV with snake_case columns
- `building_energy_ratings.parquet` (240 MB) - same data, much faster to load

## Usage

```python
import pandas as pd
df = pd.read_parquet("hf://datasets/FionnHughes/irish-building-energy-ratings/building_energy_ratings.parquet")
```

## Source

Scraped from SEAI's National BER Research Tool: https://ndber.seai.ie/BERResearchTool/ber/search.aspx

Heads up on timing: the Irish BER scale changes on 24 May 2026, going from the current 15-point system (A1, A2, B1 ...) to flat A-G plus a new A0 grade for zero-emission homes. This dataset is the old version, captured right before SEAI swaps it out.

Updated monthly by a GitHub Actions cron. Source code: https://github.com/FionnHughes/irish-open-datasets

## Licence

CC BY 4.0 - free reuse with attribution to SEAI.
