"""
Preprocessor for Reel vs Non-Reel Traffic
----------------------------------------
This module preprocesses extracted traffic features for
training and inference.

Usage:
    from src.data.preprocessor import Preprocessor
    
    pre = Preprocessor()
    X, y = pre.transform(df, label_column="traffic_type")
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class Preprocessor:
    def __init__(self):
        """
        Initialize preprocessing components.
        """
        self.scaler = StandardScaler()
        self.fitted = False

    def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fill or drop missing values.
        """
        return df.fillna(0)

    def fit(self, df: pd.DataFrame, label_column: str = None):
        """
        Fit the scaler on training data.
        """
        df = self._handle_missing(df)
        features = df.drop(columns=[label_column]) if label_column else df
        self.scaler.fit(features)
        self.fitted = True
        return self

    def transform(self, df: pd.DataFrame, label_column: str = None):
        """
        Transform dataset: scale numerical features & return arrays.
        """
        df = self._handle_missing(df)

        if label_column and label_column in df.columns:
            y = df[label_column].values
            X = df.drop(columns=[label_column])
        else:
            y = None
            X = df

        if not self.fitted:
            raise RuntimeError("Preprocessor must be fitted before transform!")

        X_scaled = self.scaler.transform(X)
        return X_scaled, y

    def fit_transform(self, df: pd.DataFrame, label_column: str = None):
        """
        Fit and transform in one step.
        """
        self.fit(df, label_column)
        return self.transform(df, label_column)


if __name__ == "__main__":
    # Example usage
    sample_data = pd.DataFrame([
        {
            "avg_packet_size": 500,
            "std_packet_size": 120,
            "avg_inter_arrival": 0.01,
            "packet_count": 100,
            "tcp_fraction": 0.7,
            "udp_fraction": 0.3,
            "duration": 5,
            "traffic_type": 1  # 1 = reel/video, 0 = non-video
        },
        {
            "avg_packet_size": 300,
            "std_packet_size": 80,
            "avg_inter_arrival": 0.05,
            "packet_count": 50,
            "tcp_fraction": 0.5,
            "udp_fraction": 0.5,
            "duration": 3,
            "traffic_type": 0
        }
    ])

    pre = Preprocessor()
    X, y = pre.fit_transform(sample_data, label_column="traffic_type")
    print("Features (X):", X)
    print("Labels (y):", y)
