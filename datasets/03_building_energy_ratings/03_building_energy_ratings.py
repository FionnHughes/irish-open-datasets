import requests
import pandas as pd
import io
import re
import zipfile
from pathlib import Path
import urllib3
urllib3.disable_warnings()

# output folder
OUTPUT_DIR = Path("output/building_energy_ratings")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# seai's ber research tool - public, no auth needed
# this is an asp.net page so we have to do the viewstate dance to "click" the download button
BASE_URL = "https://ndber.seai.ie/BERResearchTool/ber/search.aspx"

# the button name to post back - found by inspecting the form on the page
DOWNLOAD_BUTTON = "ctl00$DefaultContent$BERSearch$dfExcelDownlaod$DownloadAllData"
DOWNLOAD_VALUE = "Download All Data"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DatasetBuilder/1.0)",
    "Referer": BASE_URL,
}


def extract_hidden_field(html, name):
    # asp.net renders hidden fields like <input type="hidden" name="X" value="Y" />
    # grab the value for a given field
    pattern = rf'name="{re.escape(name)}"[^>]*value="([^"]*)"'
    m = re.search(pattern, html)
    return m.group(1) if m else None


def fetch_dataset_zip():
    print("loading the seai ber search page...")
    s = requests.Session()
    s.headers.update(HEADERS)

    r = s.get(BASE_URL, timeout=60, verify=False)
    r.raise_for_status()
    html = r.text

    # grab the viewstate stuff - we need it in the post body
    viewstate = extract_hidden_field(html, "__VIEWSTATE")
    viewstate_gen = extract_hidden_field(html, "__VIEWSTATEGENERATOR")
    event_validation = extract_hidden_field(html, "__EVENTVALIDATION")

    if not viewstate or not event_validation:
        print("    error: couldn't find viewstate fields - page layout may have changed")
        return None

    print(f"  got viewstate ({len(viewstate):,} chars)")

    # post back with the download button "clicked"
    print("posting back to trigger the download...")
    payload = {
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstate_gen or "",
        "__EVENTVALIDATION": event_validation,
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        DOWNLOAD_BUTTON: DOWNLOAD_VALUE,
    }

    # this can be a big file, give it a long timeout
    r = s.post(BASE_URL, data=payload, timeout=600, verify=False, stream=True)
    r.raise_for_status()

    ct = r.headers.get("content-type", "").lower()
    # zip can be served as application/zip, octet-stream, or x-zip-compressed
    if "zip" not in ct and "octet-stream" not in ct:
        print(f"    error: expected zip, got content-type: {ct}")
        print(f"    first 500 chars of response: {r.text[:500]}")
        return None

    content = r.content
    print(f"  got it - {len(content) / 1024 / 1024:.1f} MB")
    return content


def extract_and_parse(zip_bytes):
    # open the zip and read the data file straight into pandas
    # this skips holding a decoded-text python string in memory which on a 250mb zip
    # ends up being ~2gb of ram for nothing
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        print(f"  zip contents: {names}")

        if not names:
            return None

        # the zip has the data file plus a readme.txt - find the actual data one
        target = next((n for n in names if "search" in n.lower() or "ber" in n.lower()), names[0])
        print(f"  reading {target}...")

        with zf.open(target) as f:
            if target.lower().endswith((".xlsx", ".xls")):
                return pd.read_excel(f)

            # ber file is tab-separated, latin-1 encoded
            # quoting=3 (QUOTE_NONE) - address fields contain stray quotes that confuse pandas
            # on_bad_lines='skip' drops any rare malformed row instead of crashing
            df = pd.read_csv(
                f,
                sep="\t",
                encoding="latin-1",
                quoting=3,
                on_bad_lines="skip",
            )
            print(f"  parsed - {len(df):,} rows, {len(df.columns)} columns")
            return df


def clean(df):
    # column names to lowercase snake_case
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # strip whitespace from string columns
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.strip()

    return df


def main():
    zip_bytes = fetch_dataset_zip()
    if zip_bytes is None:
        print("download failed, giving up")
        return

    df = extract_and_parse(zip_bytes)
    if df is None:
        print("zip was empty")
        return

    df = clean(df)

    print(f"\ntotal rows: {len(df):,}")
    print(f"columns ({len(df.columns)}): {list(df.columns)[:10]}{' ...' if len(df.columns) > 10 else ''}")
    print(df.head(3).to_string())

    base = OUTPUT_DIR / "building_energy_ratings"
    print("\nwriting csv...")
    df.to_csv(f"{base}.csv", index=False, encoding="utf-8-sig")
    print("writing parquet...")
    df.to_parquet(f"{base}.parquet", index=False)
    # skipping json - 1m+ rows with a wide schema would be a 1-2gb file and slow to write
    # skipping excel - 1m+ rows is over excel's row limit anyway
    print(f"\nsaved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
