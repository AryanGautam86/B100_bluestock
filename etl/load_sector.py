import pandas as pd
from sqlalchemy import create_engine
from decouple import config

engine = create_engine(
    f"postgresql+psycopg2://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
)

sector_df = pd.read_csv("data/sector_mapping.csv")

dim_sector = pd.DataFrame({
    "sector_name": sector_df["sector"].drop_duplicates()
})

dim_sector.to_sql(
    "dim_sector",
    engine,
    if_exists="append",
    index=False
)

print("dim_sector loaded")
print(dim_sector)