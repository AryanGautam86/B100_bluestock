import pandas as pd

# Load Profit & Loss data
df = pd.read_csv("data/clean/profitandloss.csv")

# Convert to numeric
cols = [
    "operating_profit",
    "interest"
]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Interest Coverage Ratio
df["interest_coverage"] = (
    df["operating_profit"] /
    df["interest"]
)

# Remove infinite values
df["interest_coverage"] = (
    df["interest_coverage"]
    .replace([float("inf"), float("-inf")], None)
)

print(
    df[
        [
            "company_id",
            "year",
            "operating_profit",
            "interest",
            "interest_coverage"
        ]
    ].head(20)
)

df.to_csv(
    "data/clean/profitandloss_with_interest_coverage.csv",
    index=False
)

print("\nInterest Coverage calculation completed.")