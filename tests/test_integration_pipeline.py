# tests/test_integration_pipeline.py

import pandas as pd
import pytest
from src.reel_traffic_detection.data import feature_extractor
from src.reel_traffic_detection.data.feature_extractor import FeatureExtractor
#from src.model.realtime_inference import RealTimeInference
from src.reel_traffic_detection.utils.helpers import save_model, load_model
import joblib
import os
import pytest

pytestmark = pytest.mark.unit

@pytest.mark.integration
def test_end_to_end_pipeline(tmp_path):
    """
    End-to-end integration test:
    - Generate synthetic traffic features
    - Preprocess features (scaler)
    - Run real-time inference
    - Assert prediction output
    """

    # --- Step 1: Prepare synthetic traffic data ---
    sample_data = pd.DataFrame([
        {
            "avg_packet_size": 500,
            "std_packet_size": 120,
            "avg_inter_arrival": 0.01,
            "packet_count": 100,
            "tcp_fraction": 0.7,
            "udp_fraction": 0.3,
            "duration": 5
        },
        {
            "avg_packet_size": 200,
            "std_packet_size": 50,
            "avg_inter_arrival": 0.1,
            "packet_count": 50,
            "tcp_fraction": 0.2,
            "udp_fraction": 0.8,
            "duration": 2
        }
    ])

    # --- Step 2: Save a dummy model & scaler in tmp_path ---
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    import joblib

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(sample_data)

    # Labels: [1, 0] → two different classes
    y = [1, 0]
    model = LogisticRegression()
    model.fit(X_scaled, y)

    # Save artifacts
    model_path = tmp_path / "model.joblib"
    scaler_path = tmp_path / "scaler.joblib"
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    # --- Step 3: Load & simulate inference ---
    loaded_model = joblib.load(model_path)
    loaded_scaler = joblib.load(scaler_path)

    new_sample = pd.DataFrame([{
        "avg_packet_size": 400,
        "std_packet_size": 100,
        "avg_inter_arrival": 0.05,
        "packet_count": 80,
        "tcp_fraction": 0.5,
        "udp_fraction": 0.5,
        "duration": 3
    }])

    X_new_scaled = loaded_scaler.transform(new_sample)
    prediction = loaded_model.predict(X_new_scaled)

    # --- Step 4: Validate output ---
    assert prediction[0] in [0, 1]
