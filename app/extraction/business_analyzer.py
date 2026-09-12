import pandas as pd


def load_business_metrics(path: str = "data/business_metrics.csv") -> pd.DataFrame:
    return pd.read_csv(path)


def analyze_business_metrics(row: dict) -> dict:
    growth = float(row["revenue_growth_pct"])
    customer_growth = float(row["customer_growth_pct"])
    churn = float(row["churn_pct"])
    conversion = float(row["conversion_rate_pct"])
    cac = float(row["cac_usd"])
    ltv = float(row["ltv_usd"])

    ltv_cac = round(ltv / cac, 2) if cac else 0

    growth_signal = (
        "strong" if growth >= 20
        else "moderate" if growth >= 10
        else "weak"
    )

    retention_signal = (
        "strong" if churn < 2.5
        else "moderate" if churn < 5
        else "weak"
    )

    acquisition_signal = (
        "strong" if conversion >= 6
        else "moderate" if conversion >= 3
        else "weak"
    )

    opportunity_score = 0

    if growth >= 20:
        opportunity_score += 30
    elif growth >= 10:
        opportunity_score += 20

    if customer_growth >= 20:
        opportunity_score += 25
    elif customer_growth >= 10:
        opportunity_score += 15

    if churn < 2.5:
        opportunity_score += 20
    elif churn < 5:
        opportunity_score += 10

    if ltv_cac >= 10:
        opportunity_score += 25
    elif ltv_cac >= 5:
        opportunity_score += 15

    opportunity_score = min(opportunity_score, 100)

    return {
        "ltv_cac_ratio": ltv_cac,
        "growth_signal": growth_signal,
        "retention_signal": retention_signal,
        "acquisition_signal": acquisition_signal,
        "opportunity_score": opportunity_score,
    }
