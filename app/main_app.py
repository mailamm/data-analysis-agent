import streamlit as st
import pandas as pd
from config import APP_TITLE, APP_DESCRIPTION
from data_loader import load_transactions
from analysis import build_summary, aggregate_weekly_revenue
from insight_engine import generate_insights
import plotly.express as px
import plotly.graph_objects as go


def main():
    """
    Main entry point for the Streamlit app.

    Handles:
        - File upload and sidebar controls.
        - Data loading, cleaning, and aggregation.
        - KPI calculation and display.
        - Weekly revenue trend visualization with anomaly detection.
        - Top products and countries bar charts.
        - AI-generated business summary.
        - Raw data and anomaly preview.
    """
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)

    # --- Sidebar ---
    with st.sidebar:
        st.header("⚙️ Controls")
        uploaded_file = st.file_uploader(
            "Upload sales data in CSV or Excel",
            type=["csv", "xlsx", "xls"]
        )

        with open("data.csv", "rb") as f:
            st.download_button(
                label="Download Sample Data",
                data=f,
                file_name="sample_data.csv",
                mime="text/csv"
            )

        st.subheader("Analysis Settings")
        contamination_rate = st.slider(
            "Anomaly Sensitivity",
            min_value=0.005,
            max_value=0.05,
            value=0.01,
            step=0.005,
            help="Lower values detect only the most extreme anomalies. (Default: 1%)"
        )

    if uploaded_file is None:
        st.info("Please upload a file using the sidebar to begin analysis.")
        return

    # --- Data Loading and Analysis ---
    try:
        # Load and clean uploaded data.
        df = load_transactions(uploaded_file)
        if df.empty:
            st.error("File loaded, but no data was found or parsed.")
            return

        # Aggregate weekly revenue.
        weekly_df = aggregate_weekly_revenue(df)
        # Build summary with anomaly detection.
        summary = build_summary(df, contamination_rate)

    except Exception as e:
        st.error(f"An error occurred during data processing: {e}")
        return

    # --- App Layout with Tabs ---
    tab1, tab2, tab3 = st.tabs([
        "📈 Dashboard",
        "📄 Uploaded Data",
        "🤖 Business Summary",
    ])

    # --- Tab 3: Business Summary ---
    with tab3:
        if st.button("Get Key Insights"):
            with st.spinner("🤖 Calling AI Analyst... Please wait."):
                try:
                    insights_md = generate_insights(summary)
                    st.markdown(insights_md)
                except Exception as e:
                    st.error(f"Error generating insights: {e}")

    # --- Tab 2: Dashboard with detailed analysis ---
    with tab1:
        st.header("Performance Dashboard")

        # --- KPIs ---
        st.subheader("Key Performance Indicators")
        kpis = summary["core_kpis"]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Revenue", f"${kpis.get('total_revenue', 0):.2f}")
        col2.metric("Transactions", f"{kpis.get('num_transactions', 0):,}")
        col3.metric("Average Order Value", f"${kpis.get('avg_order_value', 0):.2f}")
        col4.metric("Unique Customers", kpis.get('unique_customers', 'N/A'))

        st.divider()

        col5, col6 = st.columns(2)
        col5.metric(
            "Top Country",
            kpis.get('top_country', 'N/A'),
            f"${kpis.get('top_country_revenue', 0):.2f} in revenue"
        )

        col6.metric(
            "Top Product",
            kpis.get('top_product', 'N/A'),
            f"${kpis.get('top_product_revenue', 0):.2f} in revenue"
        )

        st.divider()

        # --- Weekly Revenue Trend with Anomalies ---
        st.subheader("Weekly Revenue Trend & Anomalies")

        # Prepare anomalies DataFrame.
        anomalies_df = pd.DataFrame(summary.get("anomalies", []))

        fig = go.Figure()

        # Add the main revenue line.
        fig.add_trace(go.Scatter(
            x=weekly_df['Date'],
            y=weekly_df['Revenue'],
            mode='lines+markers',
            name='Weekly Revenue'
        ))

        # Add the anomaly markers if any.
        if not anomalies_df.empty:
            anomalies_df['Date'] = pd.to_datetime(anomalies_df['Date']).dt.strftime("%Y-%m-%d")
            fig.add_trace(go.Scatter(
                x=anomalies_df['Date'],
                y=anomalies_df['Revenue'],
                mode='markers',
                marker=dict(color='red', size=12, symbol='x'),
                name='Detected Anomaly'
            ))

        fig.update_layout(
            title="Weekly Revenue Trend with Anomalies",
            xaxis_title="Date",
            yaxis_title="Revenue",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Top N Bar Charts ---
        st.subheader("Top Performing Categories")
        col7, col8 = st.columns(2)

        with col7:
            # Display top products by revenue.
            top_products_df = summary.get("top_products_df")
            if top_products_df is not None and not top_products_df.empty:
                fig_prod = px.bar(
                    top_products_df,
                    x='Revenue',
                    y='Description',
                    orientation='h',
                    title='Top 10 Products by Revenue'
                ).update_yaxes(categoryorder="total ascending")
                st.plotly_chart(fig_prod, use_container_width=True)
            else:
                st.write("Top product data not available.")

        with col8:
            # Display top countries by revenue.
            top_countries_df = summary.get("top_countries_df")
            if top_countries_df is not None and not top_countries_df.empty:
                fig_country = px.bar(
                    top_countries_df,
                    x='Revenue',
                    y='Country',
                    orientation='h',
                    title='Top 10 Countries by Revenue'
                ).update_yaxes(categoryorder="total ascending")
                st.plotly_chart(fig_country, use_container_width=True)
            else:
                st.write("Top country data not available.")

    # --- Tab 3: Preview Uploaded Data ---
    with tab2:
        st.header("Raw Data Preview")
        st.dataframe(df)

        st.header("Anomalies Data")
        if not anomalies_df.empty:
            st.dataframe(anomalies_df)
        else:
            st.write("No anomalies were detected with the current sensitivity setting.")


if __name__ == "__main__":
    main()