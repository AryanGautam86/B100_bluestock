import pandas as pd

# Load cashflow data
df = pd.read_csv("data/clean/cashflow.csv")

# Convert columns to numeric
cols = [
    "operating_activity",
    "investing_activity"
]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Free Cash Flow
df["free_cash_flow"] = (
    df["operating_activity"] +
    df["investing_activity"]
)

print(
    df[
        [
            "company_id",
            "year",
            "operating_activity",
            "investing_activity",
            "free_cash_flow"
        ]
    ].head(20)
)

# Save output
df.to_csv(
    "data/clean/cashflow_with_fcf.csv",
    index=False
)

print("\nFree Cash Flow calculation completed.")