
import pandas as pd
from sqlalchemy import create_engine, text
from decouple import config

# =========================
# DATABASE CONNECTION
# =========================

DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Connected to PostgreSQL")

# =========================
# LOAD + CLEAN COMPANIES
# =========================

companies = pd.read_csv("data/clean/companies.csv")

# rename id -> company_id
companies = companies.rename(columns={"id": "company_id"})

# clean all string columns
for col in companies.columns:
    if companies[col].dtype == "object":
        companies[col] = companies[col].astype(str).str.strip()

# normalize company_id
companies["company_id"] = (
    companies["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# remove invalid rows
companies = companies.dropna(subset=["company_id"])
companies = companies[companies["company_id"] != ""]
companies = companies[companies["company_id"].str.len() > 0]

# remove unwanted column
if "chart_link" in companies.columns:
    companies = companies.drop(columns=["chart_link"])

# =========================
# ADD WIPRO IF MISSING
# =========================

if "WIPRO" not in companies["company_id"].values:

    wipro_row = {
        "company_id": "WIPRO",
        "company_name": "Wipro Ltd",
        "company_logo": None,
        "website": "https://www.wipro.com/",
        "nse_profile": None,
        "bse_profile": None,
        "face_value": None,
        "book_value": None,
        "roce_percentage": None,
        "roe_percentage": None,
        "about_company": None
    }

    companies = pd.concat(
        [companies, pd.DataFrame([wipro_row])],
        ignore_index=True
    )

    print("Added missing company: WIPRO")

# =========================
# DEBUG
# =========================

print("Unique companies count:", companies["company_id"].nunique())
print("WIPRO exists?", "WIPRO" in companies["company_id"].values)

# =========================
# RESET TABLES
# =========================

with engine.begin() as conn:
    conn.execute(
        text(
            """
            TRUNCATE TABLE
                fact_analysis,
                fact_balance_sheet,
                fact_cash_flow,
                fact_profit_loss,
                fact_pros_cons,
                fact_documents,
                dim_company
            RESTART IDENTITY CASCADE;
            """
        )
    )

# =========================
# LOAD DIM COMPANY
# =========================

companies.to_sql(
    "dim_company",
    engine,
    if_exists="append",
    index=False
)

print(f"Loaded companies: {len(companies)}")

# =========================
# GENERIC FACT LOADER
# =========================

def load_table(file_path, table_name):

    df = pd.read_csv(file_path)

    # Convert year -> year_label
    if "year" in df.columns:
        df.rename(columns={"year": "year_label"}, inplace=True)

    # Remove CSV id column because PostgreSQL creates it automatically
    if "id" in df.columns:
        df.drop(columns=["id"], inplace=True)

    if "company_id" in df.columns:

        df["company_id"] = (
            df["company_id"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        valid_ids = set(
            companies["company_id"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        missing_ids = sorted(
            set(df["company_id"]) - valid_ids
        )

        if missing_ids:
            print(f"\nMissing companies in {table_name}:")
            print(missing_ids)

        before = len(df)

        df = df[df["company_id"].isin(valid_ids)]

        removed = before - len(df)

        print(f"{table_name}: removed {removed} invalid rows")

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {table_name}: {len(df)}")

# =========================
# LOAD FACT TABLES
# =========================

load_table(
    "data/clean/analysis.csv",
    "fact_analysis"
)

load_table(
    "data/clean/balancesheet.csv",
    "fact_balance_sheet"
)

load_table(
    "data/clean/cashflow.csv",
    "fact_cash_flow"
)

load_table(
    "data/clean/profitandloss.csv",
    "fact_profit_loss"
)

load_table(
    "data/clean/prosandcons.csv",
    "fact_pros_cons"
)

load_table(
    "data/clean/documents.csv",
    "fact_documents"
)

print("\nALL TABLES LOADED SUCCESSFULLY")