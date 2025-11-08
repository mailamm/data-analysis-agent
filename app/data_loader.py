import pandas as pd
import streamlit as st
from config import INVOICE_DATE_COL, QUANTITY_COL, UNIT_PRICE_COL


def _read_any_file(uploaded_file):
    """
    Reads an uploaded file (CSV or Excel) and returns a pandas DataFrame.
    """
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file, encoding="latin1", low_memory=False)
    elif name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload CSV or Excel.")


@st.cache_data
def load_transactions(uploaded_file) -> pd.DataFrame:
    """
    Loads and lightly cleans an e-commerce transactions dataset.

    Wrapped with @st.cache_data to ensure the file is only loaded
    and processed once.
    """
    df = _read_any_file(uploaded_file)

    # Basic cleaning
    if INVOICE_DATE_COL not in df.columns:
        raise ValueError(f"Expected column '{INVOICE_DATE_COL}' not found in file.")

    df[INVOICE_DATE_COL] = pd.to_datetime(df[INVOICE_DATE_COL], errors="coerce")
    df = df.dropna(subset=[INVOICE_DATE_COL])

    # Ensure numeric
    for col in [QUANTITY_COL, UNIT_PRICE_COL]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=[QUANTITY_COL, UNIT_PRICE_COL])

    # Compute revenue
    df["Revenue"] = df[QUANTITY_COL] * df[UNIT_PRICE_COL]

    # Filter obviously bad rows if needed
    df = df[df["Revenue"].notna()]

    return df