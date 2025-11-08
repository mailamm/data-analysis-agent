import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np


def detect_revenue_anomalies_iforest(weekly_df, contamination=0.01):
    """
    Detects revenue anomalies in weekly aggregated data using Isolation Forest.

    Args:
        weekly_df (pd.DataFrame): DataFrame with columns ["Date", "Revenue"].
        contamination (float): Expected fraction of outliers (default 0.1).

    Returns:
        pd.DataFrame: DataFrame containing detected anomalies with columns
                      ["Date", "Revenue", "anomaly_score"].
    """
    df = weekly_df.copy().sort_values("Date").reset_index(drop=True)
    X = df[["Revenue"]].values  # feature matrix

    # Fit Isolation Forest
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=200
    )
    model.fit(X)

    # Predict anomalies: -1 = anomaly, 1 = normal
    df["anomaly_flag"] = model.predict(X)
    df["anomaly_score"] = model.decision_function(X)

    anomalies = df[df["anomaly_flag"] == -1]
    return anomalies[["Date", "Revenue", "anomaly_score"]]
