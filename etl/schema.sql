-- ==========================
-- DIMENSION TABLES
-- ==========================

CREATE TABLE IF NOT EXISTS dim_company (
    company_id VARCHAR(50) PRIMARY KEY,
    company_name TEXT,
    company_logo TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value NUMERIC,
    book_value NUMERIC,
    roce_percentage NUMERIC,
    roe_percentage NUMERIC,
    about_company TEXT
);

CREATE TABLE IF NOT EXISTS dim_year (
    year_id SERIAL PRIMARY KEY,
    year_label VARCHAR(50) UNIQUE
);

-- ==========================
-- FACT TABLES
-- ==========================

CREATE TABLE IF NOT EXISTS fact_profit_loss (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(50),
    year_label VARCHAR(50),

    sales NUMERIC,
    expenses NUMERIC,
    operating_profit NUMERIC,
    opm_percentage NUMERIC,
    other_income NUMERIC,
    interest NUMERIC,
    depreciation NUMERIC,
    profit_before_tax NUMERIC,
    tax_percentage NUMERIC,
    net_profit NUMERIC,
    eps NUMERIC,
    dividend_payout NUMERIC,

    FOREIGN KEY (company_id)
        REFERENCES dim_company(company_id)
);

CREATE TABLE IF NOT EXISTS fact_balance_sheet (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(50),
    year_label VARCHAR(50),

    equity_capital NUMERIC,
    reserves NUMERIC,
    borrowings NUMERIC,
    other_liabilities NUMERIC,
    total_liabilities NUMERIC,
    fixed_assets NUMERIC,
    cwip NUMERIC,
    investments NUMERIC,
    other_asset NUMERIC,
    total_assets NUMERIC,

    FOREIGN KEY (company_id)
        REFERENCES dim_company(company_id)
);

CREATE TABLE IF NOT EXISTS fact_cash_flow (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(50),
    year_label VARCHAR(50),

    operating_activity NUMERIC,
    investing_activity NUMERIC,
    financing_activity NUMERIC,
    net_cash_flow NUMERIC,

    FOREIGN KEY (company_id)
        REFERENCES dim_company(company_id)
);

CREATE TABLE IF NOT EXISTS fact_analysis (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(50),

    compounded_sales_growth TEXT,
    compounded_profit_growth TEXT,
    stock_price_cagr TEXT,
    roe TEXT,

    FOREIGN KEY (company_id)
        REFERENCES dim_company(company_id)
);

CREATE TABLE IF NOT EXISTS fact_pros_cons (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(50),
    pros TEXT,
    cons TEXT,

    FOREIGN KEY (company_id)
        REFERENCES dim_company(company_id)
);

CREATE TABLE IF NOT EXISTS fact_documents (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(50),
    year_label VARCHAR(50),
    annual_report TEXT,

    FOREIGN KEY (company_id)
        REFERENCES dim_company(company_id)
);