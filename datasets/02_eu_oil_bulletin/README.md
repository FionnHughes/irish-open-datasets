# EU Weekly Oil Bulletin — Fuel Prices 2005–Present

Weekly pump prices for petrol, diesel, heating oil, fuel oil and LPG across all 27 EU member states + UK since January 2005.

| | |
|---|---|
| **Rows** | 106,028 |
| **Updated** | Weekly (every Wednesday) |
| **Source** | European Commission DG ENER Weekly Oil Bulletin |
| **Licence** | CC BY 4.0 — free reuse with attribution |
| **Kaggle** | [Link](https://www.kaggle.com/datasets/fionnhughes/eu-oil-bulletin) |
| **Notebook** | [Link](https://www.kaggle.com/code/fionnhughes/eu-weekly-oil-bulletin) |
| **Hugging Face** | [Link](https://huggingface.co/datasets/FionnHughes/eu-weekly-oil-bulletin) |

## Columns

| Column | Description |
|--------|-------------|
| date | Week of price reporting |
| country | 2-letter ISO country code |
| fuel_type | petrol_95, diesel, heating_oil, fuel_oil, lpg |
| price_eur_per_litre | Pump price in EUR/litre including all taxes |

## Notes

- Prices include VAT, excise duty and carbon tax
- Non-euro countries converted using ECB reference exchange rates
- EU and EUR rows are weighted averages, not individual countries
- Some countries have missing data for early years (joined EU reporting later)

## How to run

```bash
pip install requests pandas pyarrow openpyxl
python 02_eu_oil_bulletin.py
```

Output saved to `output/eu_oil_bulletin/`