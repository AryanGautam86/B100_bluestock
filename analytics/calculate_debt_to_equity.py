import pandas as pd

# Load balance sheet
df = pd.read_csv("data/clean/balancesheet.csv")

# Convert to numeric
cols = [
    "equity_capital",
    "reserves",
    "borrowings"
]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Calculate debt_to_equity
df["debt_to_equity"] = (
    df["borrowings"] /
    (df["equity_capital"] + df["reserves"])
)

# Replace inf values
df["debt_to_equity"] = (
    df["debt_to_equity"]
    .replace([float("inf"), float("-inf")], None)
)

print(
    df[
        [
            "company_id",
            "year",
            "borrowings",
            "equity_capital",
            "reserves",
            "debt_to_equity"
        ]
    ].head(20)
)

# Save for verification
df.to_csv(
    "data/clean/balancesheet_with_de_ratio.csv",
    index=False
)

print("\nDebt-to-equity calculation completed.")