# Irish & EU Open Datasets

Publicly available data that's hard to access — cleaned, flattened and analysis-ready.

Each dataset is free on Kaggle. Scripts are here if you want to run your own updates or see how the data was collected.

| Dataset | Rows | Updated | Kaggle | Notebook | Hugging Face |
|---------|------|---------|--------|----------|--------------|
| Irish Property Price Register | 778k | Monthly | [Kaggle](https://www.kaggle.com/datasets/fionnhughes/property-price-register) | [Notebook](https://www.kaggle.com/code/fionnhughes/irish-property-price-analysis) | [Hugging Face](https://huggingface.co/datasets/FionnHughes/irish-property-price-register) |
| EU Weekly Oil Bulletin | 106k | Weekly | [Kaggle](https://www.kaggle.com/datasets/fionnhughes/eu-oil-bulletin) | [Notebook](https://www.kaggle.com/code/fionnhughes/eu-weekly-oil-bulletin) | [Hugging Face](https://huggingface.co/datasets/FionnHughes/eu-weekly-oil-bulletin) |
| Irish Building Energy Ratings | 1.4M | Monthly | [Kaggle](https://www.kaggle.com/datasets/fionnhughes/irish-building-energy-ratings) | [Notebook](https://www.kaggle.com/code/fionnhughes/irish-building-energy-ratings-analysis) | [Hugging Face](https://huggingface.co/datasets/FionnHughes/irish-building-energy-ratings) |

## About

First-year Computer Science student based in Dublin. I build datasets from Irish and European government sources that are publicly available but poorly accessible — scattered across PDFs, messy Excel files, or buried behind pagination with no bulk download.

Everything is cleaned and analysis-ready. Scripts are here if you want to run your own updates.

## Updates

Every dataset stays current automatically. GitHub Actions runs each scraper on a cron, pushes the fresh data to both Kaggle and Hugging Face, and the analysis notebooks pick it up on their next scheduled rerun. No manual touching.

- Property Price Register: 1st of each month, 03:00 UTC
- EU Weekly Oil Bulletin: every Wednesday, 14:00 UTC
- Irish Building Energy Ratings: 1st of each month, 03:00 UTC

## Structure

```
datasets/          - one folder per dataset, script + README + kaggle metadata
notebooks/         - analysis notebooks (one per dataset)
.github/workflows/ - cron jobs that scrape and publish
```

## Licence

Each dataset inherits the licence of its source. Specifics in each dataset's README.
