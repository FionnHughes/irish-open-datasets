import requests
import pandas as pd
import io
import time
from pathlib import Path
from datetime import datetime
import urllib3
urllib3.disable_warnings()

# output folder
OUTPUT_DIR = Path("output/property_price_register")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# url patterns - took a while to figure these out
# annual files exist for most years, fall back to county/month if not
ANNUAL_URL = (
    "https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf"
    "/Downloads/PPR-{year}.csv/$FILE/PPR-{year}.csv"
)

COUNTY_MONTH_URL = (
    "https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf"
    "/Downloads/PPR-{year}-{month:02d}-{county}.csv/$FILE/PPR-{year}-{month:02d}-{county}.csv"
)

COUNTIES = [
    "Carlow", "Cavan", "Clare", "Cork", "Donegal", "Dublin",
    "Galway", "Kerry", "Kildare", "Kilkenny", "Laois", "Leitrim",
    "Limerick", "Longford", "Louth", "Mayo", "Meath", "Monaghan",
    "Offaly", "Roscommon", "Sligo", "Tipperary", "Waterford",
    "Westmeath", "Wexford", "Wicklow",
]

START_YEAR = 2010
END_YEAR = datetime.now().year


def fetch_url(url):
    try:
        r = requests.get(url, timeout=30, verify=False)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        # site uses cp1252 encoding, utf-8 breaks it
        content = r.content.decode("cp1252", errors="replace")
        df = pd.read_csv(io.StringIO(content))
        if df.empty:
            return None
        return df
    except Exception as e:
        print(f"    error: {e}")
        return None


def fetch_year(year):
    now = datetime.now()

    # try annual file first
    url = ANNUAL_URL.format(year=year)
    print(f"[{year}] trying annual file...", end=" ", flush=True)
    df = fetch_url(url)
    if df is not None:
        print(f"got it - {len(df):,} rows")
        return df

    # if that doesnt work try per county per month
    print("not found, trying county/month...")
    frames = []
    max_month = now.month if year == now.year else 12

    for month in range(1, max_month + 1):
        for county in COUNTIES:
            url = COUNTY_MONTH_URL.format(year=year, month=month, county=county)
            df = fetch_url(url)
            if df is not None:
                frames.append(df)
        time.sleep(0.2)

    if not frames:
        print(f"nothing found for {year}")
        return None

    combined = pd.concat(frames, ignore_index=True)
    print(f"done - {len(combined):,} rows")
    return combined


def clean(df):
    # strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # rename columns to something sensible
    cols = ["date_of_sale", "address", "county", "eircode", "price_eur",
            "not_full_market_price", "vat_exclusive", "description", "property_size"]
    col_map = dict(zip(df.columns[:len(cols)], cols))
    df = df.rename(columns=col_map)
    df = df[[c for c in cols if c in df.columns]]

    # clean up price - remove euro sign and commas
    if "price_eur" in df.columns:
        df["price_eur"] = (
            df["price_eur"].astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["price_eur"] = pd.to_numeric(df["price_eur"], errors="coerce")

    if "date_of_sale" in df.columns:
        df["date_of_sale"] = pd.to_datetime(df["date_of_sale"], dayfirst=True, errors="coerce")

    # yes/no columns to bool
    for col in ["not_full_market_price", "vat_exclusive"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().map({"yes": True, "no": False})

    # strip whitespace from all string columns
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.strip()

    return df


def main():
    all_frames = []

    for year in range(START_YEAR, END_YEAR + 1):
        df = fetch_year(year)
        if df is not None:
            df = clean(df)
            all_frames.append(df)
        time.sleep(0.5)

    if not all_frames:
        print("no data fetched, something went wrong")
        return

    full = pd.concat(all_frames, ignore_index=True)
    full = full.drop_duplicates()
    full = full.sort_values("date_of_sale").reset_index(drop=True)

    print(f"\ntotal rows: {len(full):,}")
    print(full.head(3).to_string())

    # save outputs
    base = OUTPUT_DIR / "property_price_register"
    full.to_csv(f"{base}.csv", index=False, encoding="utf-8-sig")
    full.to_json(f"{base}.json", orient="records", lines=True, date_format="iso")
    full.to_parquet(f"{base}.parquet", index=False)
    print(f"\nsaved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()