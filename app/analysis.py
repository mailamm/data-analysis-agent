import pandas as pd
import streamlit as st
from config import (
    INVOICE_DATE_COL,
    COUNTRY_COL,
    CUSTOMER_ID_COL,
    DESCRIPTION_COL,
)
from anomaly_detector import detect_revenue_anomalies_iforest

@st.cache_data
def aggregate_weekly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates revenue by calendar week.

    Args:
        df (pd.DataFrame): DataFrame containing transaction data.

    Returns:
        pd.DataFrame: DataFrame with columns ["Date", "Revenue"] for each week.
    """
    dates = pd.to_datetime(df[INVOICE_DATE_COL])
    weekly = (
        df.assign(Week=dates.dt.to_period("W").apply(lambda r: r.start_time))
        .groupby("Week")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Week": "Date"})
    )
    weekly["Date"] = pd.to_datetime(weekly["Date"])
    return weekly


def compute_core_kpis(df: pd.DataFrame) -> dict:
    """
    Computes core KPIs from transaction data.

    Args:
        df (pd.DataFrame): DataFrame containing transaction data.

    Returns:
        dict: Dictionary of KPIs including total revenue, transactions, AOV,
              top country/product, and unique customers.
    """
    total_revenue = df["Revenue"].sum()
    num_transactions = df["Revenue"].count()
    avg_order_value = total_revenue / num_transactions if num_transactions else 0.0

    # Top country by revenue
    if COUNTRY_COL in df.columns:
        revenue_by_country = (
            df.groupby(COUNTRY_COL)["Revenue"].sum().sort_values(ascending=False)
        )
        top_country = revenue_by_country.index[0]
        top_country_revenue = revenue_by_country.iloc[0]
    else:
        top_country = None
        top_country_revenue = None

    # Top product by revenue
    if DESCRIPTION_COL in df.columns:
        product_revenue = (
            df.groupby(DESCRIPTION_COL)["Revenue"].sum().sort_values(ascending=False)
        )
        top_product = product_revenue.index[0]
        top_product_revenue = product_revenue.iloc[0]
    else:
        top_product = None
        top_product_revenue = None

    # Unique customers
    if CUSTOMER_ID_COL in df.columns:
        unique_customers = df[CUSTOMER_ID_COL].nunique()
    else:
        unique_customers = None

    return {
        "total_revenue": float(total_revenue),
        "num_transactions": int(num_transactions),
        "avg_order_value": float(avg_order_value),
        "top_country": top_country,
        "top_country_revenue": float(top_country_revenue) if top_country_revenue else None,
        "top_product": top_product,
        "top_product_revenue": float(top_product_revenue) if top_product_revenue else None,
        "unique_customers": int(unique_customers) if unique_customers is not None else None,
    }

@st.cache_data
def build_summary(df: pd.DataFrame, contamination) -> dict:
    """
    Builds a summary dictionary for downstream analysis.

    Includes KPIs, recent weekly trends, detected anomalies,
    and top N dataframes for charting.

    Args:
        df (pd.DataFrame): DataFrame containing transaction data.
        contamination (float): Contamination factor for anomaly detection.

    Returns:
        dict: Summary dictionary with keys "core_kpis", "recent_trend",
              "anomalies", "top_products_df", "top_countries_df".
    """
    weekly = aggregate_weekly_revenue(df)
    core_kpis = compute_core_kpis(df)

    # Last 8 week revenue for simple trend
    recent_trend = weekly.tail(8).to_dict(orient="records")

    # Anomaly detection
    anomalies_df = detect_revenue_anomalies_iforest(weekly, contamination=contamination)
    anomalies = anomalies_df.to_dict(orient="records")

    # Generate Top 10 Products DataFrame for charting
    top_products_df = pd.DataFrame()
    if DESCRIPTION_COL in df.columns:
        top_products_df = (
            df.groupby(DESCRIPTION_COL)["Revenue"]
            .sum()
            .nlargest(10)
            .reset_index()
        )

    # Generate Top 10 Countries DataFrame for charting
    top_countries_df = pd.DataFrame()
    if COUNTRY_COL in df.columns:
        top_countries_df = (
            df.groupby(COUNTRY_COL)["Revenue"]
            .sum()
            .nlargest(10)
            .reset_index()
        )

    summary = {
        "core_kpis": core_kpis,
        "recent_trend": recent_trend,
        "anomalies": anomalies,
        "top_products_df": top_products_df,
        "top_countries_df": top_countries_df,
    }
    return summary