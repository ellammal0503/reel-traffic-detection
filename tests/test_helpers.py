import os
import json
import pandas as pd
import pytest
from reel_traffic_detection.utils import helpers

# --- Synthetic Traffic ---
def test_generate_synthetic_traffic_deterministic():
    df = helpers.generate_synthetic_traffic(n_samples=10, video_ratio=0.7)
    assert len(df) == 10
    assert "traffic_type" in df.columns
    assert df["traffic_type"].isin([0,1]).all()

# --- JSON helpers ---
def test_save_and_load_json(tmp_path):
    data = {"a": 1, "b": 2}
    file_path = tmp_path / "test.json"
    helpers.save_json(data, str(file_path))
    loaded = helpers.load_json(str(file_path))
    assert loaded == data

# --- Model helpers ---
def test_save_and_load_model(tmp_path):
    model = {"weights": [1,2,3]}
    file_path = tmp_path / "model.pkl"
    helpers.save_model(model, str(file_path))
    loaded = helpers.load_model(str(file_path))
    assert loaded == model

def test_load_model_file_not_exist():
    with pytest.raises(FileNotFoundError):
        helpers.load_model("nonexistent_model.pkl")

# --- Measure latency ---
def test_measure_latency():
    def dummy_fn(x):
        return x * 2
    result, latency = helpers.measure_latency(dummy_fn, 5)
    assert result == 10
    assert latency >= 0
