import pandas as pd

# Load Profit & Loss data
df = pd.read_csv("data/clean/profitandloss.csv")

# Convert required columns to numeric
cols = [
    "sales",
    "net_profit"
]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Calculate Net Profit Margin %
df["net_profit_margin_pct"] = (
    df["net_profit"] / df["sales"]
) * 100

# Remove infinite values
df["net_profit_margin_pct"] = (
    df["net_profit_margin_pct"]
    .replace([float("inf"), float("-inf")], None)
)

print(
    df[
        [
            "company_id",
            "year",
            "sales",
            "net_profit",
            "net_profit_margin_pct"
        ]
    ].head(20)
)

# Save result
df.to_csv(
    "data/clean/profitandloss_with_margin.csv",
    index=False
)

print("\nNet Profit Margin calculation completed.")