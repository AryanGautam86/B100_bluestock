import pandas as pd

# files = [
#     "companies",
#     "analysis",
#     "balancesheet",
#     "cashflow",
#     "profitandloss",
#     "prosandcons",
#     "documents"
# ]

# for f in files:
#     df = pd.read_csv(f"cleaned_data/{f}.csv")
#     print(f"\n===== {f.upper()} =====")
#     print(df.columns.tolist())

companies = pd.read_csv("data/clean/companies.csv")

companies = companies.rename(columns={"id":"company_id"})

companies["company_id"] = (
    companies["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

print(companies["company_id"].tolist())