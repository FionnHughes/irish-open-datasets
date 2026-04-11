import requests
import pandas as pd
import io
from pathlib import Path

# output folder
OUTPUT_DIR = Path("output/eu_oil_bulletin")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# the ec publishes one big xlsx with everything from 2005 — same url updated weekly in place
HISTORY_URL = (
    "https://energy.ec.europa.eu/document/download/"
    "906e60ca-8b6a-44e7-8589-652854d2fd3f_en"
    "?filename=Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx"
)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DatasetBuilder/1.0)"}
PRICES_SHEET = "Prices with taxes"

# column names in the xlsx end with these suffixes — map them to readable labels
# fuel_oil_2 gets skipped, it's barely reported and not useful
FUEL_TYPES = {
    "euro95":      "petrol_95",
    "diesel":      "diesel",
    "heating_oil": "heating_oil",
    "fuel_oil_1":  "fuel_oil",
    "LPG":         "lpg",
}


def download_xlsx():
    # just grabs the xlsx from the ec server and returns the raw bytes
    print("downloading EC oil bulletin xlsx...")
    try:
        r = requests.get(HISTORY_URL, headers=HEADERS, timeout=120)
        r.raise_for_status()
        print(f"  got it — {len(r.content) / 1024:.0f} KB")
        return r.content
    except Exception as e:
        print(f"    error: {e}")
        return None


def parse_prices(xl):
    # the sheet has a weird header — row 0 is the column ids, rows 1-2 are
    # human readable labels and units we dont need, actual data starts row 3
    df = xl.parse(PRICES_SHEET, header=0, skiprows=[1, 2], index_col=0)

    # drop completely empty rows and parse dates
    df = df.dropna(how="all")
    df.index = pd.to_datetime(df.index, errors="coerce")
    df = df[df.index.notna()]
    df.index.name = "date"

    # columns we want all follow the pattern XX_price_with_tax_FUELTYPE
    # e.g. IE_price_with_tax_diesel — grab only those
    price_cols = [c for c in df.columns if "_price_with_tax_" in str(c)]
    df = df[price_cols]

    rows = []
    for col in price_cols:
        # split IE_price_with_tax_diesel into country=IE and fuel=diesel
        parts = str(col).split("_price_with_tax_")
        if len(parts) != 2:
            continue

        country = parts[0].rstrip("_")
        fuel_suffix = parts[1]
        fuel_label = FUEL_TYPES.get(fuel_suffix)

        # skip anything we dont have a label for
        if fuel_label is None:
            continue

        series = pd.to_numeric(df[col], errors="coerce").dropna()
        series = series[series > 0]

        tmp = series.reset_index()
        tmp.columns = ["date", "price_raw"]
        tmp["country"] = country
        tmp["fuel_type"] = fuel_label

        # source is in eur per 1000 litres — convert to per litre
        tmp["price_eur_per_litre"] = tmp["price_raw"] / 1000
        tmp = tmp[["date", "country", "fuel_type", "price_eur_per_litre"]]
        rows.append(tmp)

    full = pd.concat(rows, ignore_index=True)
    full = full.sort_values(["date", "country", "fuel_type"]).reset_index(drop=True)
    return full


def main():
    base = OUTPUT_DIR / "eu_oil_bulletin"
    csv_path = base.with_suffix(".csv")

    # if we already have the csv just convert formats and bail out
    # saves re-downloading the 4mb xlsx every time
    if csv_path.exists():
        print("csv already exists, converting formats...")
        df = pd.read_csv(csv_path)
        df.to_json(f"{base}.json", orient="records", lines=True, date_format="iso")
        df.to_parquet(f"{base}.parquet", index=False)
        print(f"done — {len(df):,} rows")
        return

    xlsx_bytes = download_xlsx()
    if xlsx_bytes is None:
        print("download failed, giving up")
        return

    xl = pd.ExcelFile(io.BytesIO(xlsx_bytes))
    df = parse_prices(xl)

    print(f"\ntotal rows: {len(df):,}")
    print(f"date range: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"countries: {sorted(df['country'].unique())}")
    print(f"fuel types: {sorted(df['fuel_type'].unique())}")
    print(df[df["country"] == "IE"].tail(5).to_string())

    df.to_csv(f"{base}.csv", index=False, encoding="utf-8-sig")
    df.to_json(f"{base}.json", orient="records", lines=True, date_format="iso")
    df.to_parquet(f"{base}.parquet", index=False)
    print(f"\nsaved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()