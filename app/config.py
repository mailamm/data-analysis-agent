import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

# Columns in the e-commerce dataset
INVOICE_DATE_COL = "InvoiceDate"
QUANTITY_COL = "Quantity"
UNIT_PRICE_COL = "UnitPrice"
COUNTRY_COL = "Country"
CUSTOMER_ID_COL = "CustomerID"
DESCRIPTION_COL = "Description"

# # Anomaly detection configuration
# ANOMALY_ROLLING_WINDOW_WEEKS = 3
# ANOMALY_Z_THRESHOLD = 2.0  # |z| >= 2 means anomaly

# General app settings
APP_TITLE = "Revenue Intelligence Dashboard"
APP_DESCRIPTION = (
    "Upload your sales data to uncover weekly trends, detect anomalies, "
    "and get clear business insights and recommendations."
)
