import pandas as pd
from sqlalchemy import create_engine
from decouple import config
import re

# =========================
# DATABASE CONNECTION
# =========================

engine = create_engine(
    f"postgresql+psycopg2://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
)

# =========================
# COLLECT YEARS
# =========================

files = [
    "data/clean/balancesheet.csv",
    "data/clean/cashflow.csv",
    "data/clean/profitandloss.csv",
    "data/clean/documents.csv"
]

years = set()

for file in files:

    print(f"Reading {file}")

    df = pd.read_csv(file)

    if "year" in df.columns:

        years.update(
            df["year"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

    elif "year_label" in df.columns:

        years.update(
            df["year_label"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

# =========================
# CONVERT EVERYTHING TO STRING
# =========================

years = sorted(
    [str(y).strip() for y in years]
)

print("\nYears found:")
print(years)

# =========================
# BUILD DIM_YEAR
# =========================

records = []

for idx, year in enumerate(years, start=1):

    if year.upper() == "TTM":

        records.append({
            "year_label": "TTM",
            "fiscal_year": None,
            "is_ttm": True,
            "sort_order": 999
        })

    else:

        # extract year like 2013, 2024 etc.
        match = re.search(r"(20\d{2})", year)

        fiscal_year = (
            int(match.group(1))
            if match
            else None
        )

        records.append({
            "year_label": year,
            "fiscal_year": fiscal_year,
            "is_ttm": False,
            "sort_order": fiscal_year
        })

# =========================
# CREATE DATAFRAME
# =========================

dim_year = pd.DataFrame(records)

# remove duplicates if any
dim_year = dim_year.drop_duplicates(
    subset=["year_label"]
)

# sort properly
dim_year = dim_year.sort_values(
    by="sort_order",
    na_position="last"
)

print("\nDim Year Preview:")
print(dim_year.head(20))

print("\nTotal Years:")
print(len(dim_year))

# =========================
# LOAD TO POSTGRESQL
# =========================

dim_year.to_sql(
    "dim_year",
    engine,
    if_exists="replace",
    index=False
)

print("\ndim_year loaded successfully")