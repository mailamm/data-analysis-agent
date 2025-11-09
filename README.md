# Data-to-Insight AI Agent

This project is a Streamlit web application that acts as an "AI Data Analyst." It accepts sales data (CSV or Excel), performs a comprehensive analysis, and uses a Generative AI (Google's Gemini) to produce a concise, non-technical business summary with scannable insights and recommended actions.

**Live Demo:** [Streamlit-App-Link](https://mainapppy-6pvekcegzz8z7pz9bimq8t.streamlit.app/)

## Project Objective

The goal is to automate the time-consuming manual process of reviewing weekly sales data. This prototype is designed for a mid-size retail client who needs to quickly understand performance, identify trends, and spot anomalies without deep technical expertise.

### Project Structure

The project is organized into a modular `app` package, with key files in the root for configuration and setup.

```
data-analysis-agent/
│
├── app/
│   ├── __init__.py          # Makes 'app' a Python package
│   ├── main_app.py          # Main Streamlit application script
│   ├── data_loader.py       # Handles file reading and data cleaning
│   ├── analysis.py          # Performs all calculations (KPIs, trends, Top 10)
│   ├── anomaly_detector.py  # Contains the IsolationForest anomaly logic
│   ├── insight_engine.py    # Formats the prompt and calls the Gemini API
│   └── config.py            # Stores constants (column names, API key retrieval)
├── data.csv                 # Sample data file for demoing
├── requirements.txt         # List of Python dependencies for pip
└── README.md                # Project documentation
```

### Key File Descriptions

* **`app/main_app.py`**: The main entry point for the Streamlit app. It handles the UI layout (tabs, sidebar), charts, and button logic. It calls all other modules to get its data.
* **`app/data_loader.py`**: Loads the user's uploaded CSV/Excel file into a Pandas DataFrame. Cleans data, parses dates, and computes the `Revenue` column.
* **`app/analysis.py`**: This module contains the functions to calculate all Core KPIs, aggregate data weekly, run the anomaly detection, and generate the Top 10 DataFrames for the charts.
* **`app/anomaly_detector.py`**: A dedicated module for the `IsolationForest` model. It takes the weekly data and returns a DataFrame of detected anomalies.
* **`app/insight_engine.py`**: Responsible for all AI interaction. It formats the data from `analysis.py` into a detailed prompt and handles the API call to Google Gemini.
* **`app/config.py`**: A central file to store global constants, such as the exact column names (`InvoiceDate`, `Country`, etc.) and to load the `GEMINI_API_KEY` from the environment.
* **`requirements.txt`**: Defines all project dependencies (`streamlit`, `pandas`, `scikit-learn`, `google-generativeai`, etc.) needed to run the app.
---
## Features

* **File Upload:** Accepts `.csv`, `.xlsx`, or `.xls` files.
* **AI-Generated Insights:** A "Get Key Insights" button calls the Gemini API to provide a narrative summary of the data.
* **Interactive Dashboard:** A tabbed dashboard displays:
    * **KPIs:** Total Revenue, Transactions, Avg. Order Value, etc.
    * **Trend Chart:** An interactive Plotly chart showing weekly revenue.
    * **Anomaly Detection:** Anomalies are flagged and overlaid on the trend chart.
    * **Top Performers:** Bar charts for Top 10 Countries and Products.
* **Adjustable Sensitivity:** A sidebar slider allows the user to control the sensitivity of the `IsolationForest` anomaly detection model.

---
## Solution Architecture & Design Flow

The application follows a simple, five-step data flow:

1.  **Upload:** The user uploads a data file via the Streamlit sidebar (`st.file_uploader`).
2.  **Load & Clean:** `data_loader.py` reads the file (Pandas), parses `InvoiceDate`, and computes the `Revenue` column.
3.  **Analyze:** `analysis.py` aggregates data weekly, computes all core KPIs, runs the `IsolationForest` model to find anomalies, and generates Top 10 lists for products/countries.
4.  **Visualize:** `main_app.py` uses Streamlit tabs (`st.tabs`), custom markdown "metrics", and Plotly charts (`go.Figure`, `px.bar`) to build the interactive dashboard.
5.  **Reason:** `insight_engine.py` formats the analysis summary into a detailed prompt and sends it to the Gemini API to generate the final business report.

---

## Data Source

This app is designed to work with the **E-Commerce Data** dataset from Kaggle.

* **Link:** [kaggle.com/datasets/carrie1/ecommerce-data](https://www.kaggle.com/datasets/carrie1/ecommerce-data)
* A `data.csv` file from this dataset is included in the repository. You can download it from the app's sidebar to run a demo.

---
## Key Assumptions

* **Schema:** The uploaded file is expected to have columns matching the configuration in `config.py` (`InvoiceDate`, `Quantity`, `UnitPrice`, `Country`, `Description`).
* **Data Quality:** Assumes `Quantity` and `UnitPrice` are numeric and `InvoiceDate` is a parsable date format.
* **Connectivity:** The app requires an active internet connection to contact the Google Gemini API.
---

## How to Run Locally

### 1. Prerequisites

* Python 3.9+
* Git

### 2. Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/mailamm/data-analysis-agent.git
    cd data-analysis-agent
    ```

2.  **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**

Get your free API key from **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
    Create a file named `.env` in the root of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

### 3. Run the App

```sh
streamlit run main_app.py
```
