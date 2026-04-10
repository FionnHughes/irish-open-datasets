# Irish Open Datasets

Python scripts that collect and clean Irish public data into 
analysis-ready flat files.

All datasets are free on Kaggle and Hugging Face.

## Datasets

| # | Dataset | Kaggle | Hugging Face |
|---|---------|--------|--------------|
| 1 | Property Price Register | [Kaggle](https://www.kaggle.com/datasets/fionnhughes/property-price-register) | [HF](https://huggingface.co/datasets/FionnHughes/irish-property-price-register) |
| 2 | EP Voting Records | coming soon | coming soon |
| 3 | CSO Ireland Stats | coming soon | coming soon |
| 4 | Planning Applications | coming soon | coming soon |
| 5 | Charities Register | coming soon | coming soon |
| 6 | CRO Companies | coming soon | coming soon |
| 7 | FSAI Enforcement | coming soon | coming soon |
| 8 | RTB Rent Index | coming soon | coming soon |

## Scripts

| Script | Dataset |
|--------|---------|
| 01_property_price_register.py | Property Price Register |
| 02_ep_voting_records.py | European Parliament votes |
| 03_cso_ireland_stats.py | CSO Ireland stats |
| 04_planning_applications.py | Planning applications |
| 05_charities_register.py | Charities register |
| 06_cro_companies.py | CRO companies |
| 07_fsai_enforcement.py | FSAI enforcement |
| 08_rtb_rent_index.py | RTB rent index |

## Requirements
pip install requests pandas pyarrow openpyxl pdfplumber

## Licence
Scripts: MIT  
Data: CC BY 4.0 (see individual dataset pages for source licences)
