import pandas as pd
from config import INVOICE_DATE_COL, QUANTITY_COL, UNIT_PRICE_COL


def _read_any_file(uploaded_file):
    """
    Reads an uploaded file (CSV or Excel) and returns a pandas DataFrame.

    Args:
        uploaded_file: File-like object, expected to be a CSV or Excel file.

    Returns:
        pd.DataFrame: DataFrame containing the file's data.

    Raises:
        ValueError: If the file type is unsupported.
    """
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file, encoding="latin1", low_memory=False)
    elif name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload CSV or Excel.")



def load_transactions(uploaded_file) -> pd.DataFrame:
    """
    Loads and lightly cleans an e-commerce transactions dataset.

    - Reads the uploaded file into a DataFrame.
    - Checks for required columns.
    - Converts date and numeric columns to appropriate types.
    - Computes a 'Revenue' column.
    - Filters out invalid rows.

    Args:
        uploaded_file: File-like object containing transaction data.

    Returns:
        pd.DataFrame: Cleaned DataFrame with a 'Revenue' column.

    Raises:
        ValueError: If required columns are missing.
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
