# tests/test_realtime_inference.py
import pytest
from unittest.mock import patch, MagicMock
from reel_traffic_detection.models import realtime_inference
from reel_traffic_detection.models.realtime_inference import RealTimeInferenceML
import pandas as pd
import pytest

pytestmark = pytest.mark.unit

'''
def test_load_model():
    #with patch("reel_traffic_detection.model.realtime_inference.SomeModelClass") as MockModel:
    with patch("reel_traffic_detection.models.realtime_inference.SomeModelClass") as MockModel:
        mock_instance = MockModel.return_value
        model = realtime_inference.load_model("fake_model_path")
        assert model == mock_instance
        MockModel.assert_called_once_with("fake_model_path")


def test_run_inference():
    mock_model = MagicMock()
    mock_features = {"speed": 50, "density": 10}
    realtime_inference.run_inference(mock_model, mock_features)
    mock_model.predict.assert_called_once_with(mock_features)
'''
def test_load_model(mocker):
    mock_model = mocker.Mock()
    mock_preprocessor = mocker.Mock()
    mocker.patch("joblib.load", side_effect=[mock_model, mock_preprocessor])

    rti = RealTimeInferenceML("dummy_model.pkl", "dummy_scaler.pkl")

    assert rti.model == mock_model
    assert rti.preprocessor == mock_preprocessor

def test_run_inference(mocker):
    mock_model = mocker.Mock()
    mock_model.predict_proba.return_value = [[0.2, 0.8]]

    mock_preprocessor = mocker.Mock()
    mock_preprocessor.transform.return_value = ([[1, 2, 3]], None)
    # Add expected features
    mock_preprocessor.feature_names_in_ = ["dummy"]

    rti = RealTimeInferenceML.__new__(RealTimeInferenceML)  # bypass __init__
    rti.model = mock_model
    rti.preprocessor = mock_preprocessor
    rti.latencies = []

    label, conf = rti.predict(pd.DataFrame([{"dummy": 1}]))
    assert isinstance(label, int)
    assert isinstance(conf, float)

