# Irish Building Energy Ratings (BER)

Every BER assessment ever issued in Ireland - energy ratings, fuel types, construction details, dwelling types, and dozens of other fields for around a million dwellings.

| | |
|---|---|
| **Rows** | ~1M+ |
| **Updated** | Monthly |
| **Source** | SEAI National BER Research Tool |
| **Licence** | CC BY 4.0 - free reuse with attribution |
| **Kaggle** | [Link](https://www.kaggle.com/datasets/fionnhughes/irish-building-energy-ratings) |
| **Notebook** | [Link](https://www.kaggle.com/code/fionnhughes/irish-building-energy-ratings) |
| **Hugging Face** | [Link](https://huggingface.co/datasets/FionnHughes/irish-building-energy-ratings) |

## Notes

- Captures the BER dataset under the legacy 15-point scale (A1, A2, B1, B2…) before the system shifts to flat A–G plus a new A0 zero-emission category on 24 May 2026
- All addresses are anonymised by SEAI before publication, no personal data
- The file inside the zip from SEAI is tab-separated, the script handles encoding detection automatically

## How to run

```bash
pip install requests pandas pyarrow openpyxl
python 03_building_energy_ratings.py
```

Output saved to `output/building_energy_ratings/` as CSV and Parquet. JSON and Excel are skipped - the dataset is over a million rows so Excel can't hold it and a line-delimited JSON would be 1–2GB for no real benefit over CSV.
