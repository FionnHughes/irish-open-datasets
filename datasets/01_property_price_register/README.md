# Irish Property Price Register

Every residential property sale in Ireland from January 2010 to present.

| | |
|---|---|
| **Rows** | 778,508 |
| **Updated** | Monthly |
| **Source** | Property Services Regulatory Authority (PSRA) |
| **Licence** | PSI Open Licence — free reuse with attribution |
| **Kaggle** | [Link](https://www.kaggle.com/datasets/fionnhughes/property-price-register) |
| **Notebook** | [Link](https://www.kaggle.com/code/fionnhughes/irish-property-price-analysis) |
| **Hugging Face** | [Link](https://huggingface.co/datasets/FionnHughes/irish-property-price-register) |

## Columns

| Column | Description |
|--------|-------------|
| date_of_sale | Date the sale was completed and registered |
| address | Full address as submitted to the PSRA |
| county | County where the property is located |
| eircode | Irish postal code (blank before 2015) |
| price_eur | Sale price in euros |
| not_full_market_price | True if not sold at full market value |
| vat_exclusive | True if price excludes VAT (typically new builds) |
| description | Property type — new or second-hand dwelling |
| property_size | Size category where available |

## How to run

```bash
pip install requests pandas pyarrow openpyxl
python 01_property_price_register.py
```

Output saved to `output/property_price_register/`