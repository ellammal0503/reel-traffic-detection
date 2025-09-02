import pytest
import pandas as pd
from reel_traffic_detection.data.feature_extractor import FeatureExtractor

# --- Fake packet for mocking ---
class FakePacket:
    def __init__(self, size=100, proto="TCP", time=0):
        self._size = size
        self._time = time
        self._proto = proto

    def haslayer(self, layer):
        if layer.__name__ == self._proto:
            return True
        return False

    def __len__(self):
        return self._size

    @property
    def time(self):
        return self._time

    @property
    def IP(self):
        return self

    @property
    def src(self):
        return "1.1.1.1"

    @property
    def dst(self):
        return "2.2.2.2"

# --- Fixtures ---
@pytest.fixture
def mock_rdpcap(monkeypatch):
    monkeypatch.setattr(
        "reel_traffic_detection.data.feature_extractor.rdpcap",
        lambda x: [FakePacket(time=i) for i in range(5)]
    )

# --- Tests ---
def test_feature_extractor(mock_rdpcap):
    extractor = FeatureExtractor()
    df = extractor.extract_from_pcap("dummy.pcap")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "avg_packet_size" in df.columns
    assert df["packet_count"].iloc[0] == 5

def test_empty_pcap(monkeypatch):
    extractor = FeatureExtractor()
    monkeypatch.setattr(
        "reel_traffic_detection.data.feature_extractor.rdpcap",
        lambda x: []
    )
    df = extractor.extract_from_pcap("dummy.pcap")
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_single_packet(monkeypatch):
    extractor = FeatureExtractor()
    monkeypatch.setattr(
        "reel_traffic_detection.data.feature_extractor.rdpcap",
        lambda x: [FakePacket(time=10)]
    )
    df = extractor.extract_from_pcap("dummy.pcap")
    assert df["duration"].iloc[0] == 0
    assert df["packet_count"].iloc[0] == 1


import pytest
import pandas as pd
from unittest.mock import patch
from reel_traffic_detection.data.feature_extractor import FeatureExtractor

class TimeAnomalyPacket:
    """Packet with irregular time values for testing inter-arrival calculations"""
    def __init__(self, time, size=100, has_ip=True):
        self.time = time
        self._size = size
        self.layers = {}
        if has_ip:
            self.layers["IP"] = type("IP", (), {"src": "1.1.1.1", "dst": "2.2.2.2"})()
        self.layers["TCP"] = True

    def haslayer(self, layer):
        return layer.__name__ in self.layers

    def __getitem__(self, item):
        if item.__name__ in self.layers:
            return self.layers[item.__name__]
        raise KeyError

    def __len__(self):
        return self._size

@pytest.fixture
def mock_time_anomaly_rdpcap():
    # Includes packets with decreasing, repeated, and zero time values
    packets = [
        TimeAnomalyPacket(time=10),
        TimeAnomalyPacket(time=5),   # decreasing time
        TimeAnomalyPacket(time=10),  # repeated time
        TimeAnomalyPacket(time=0),   # zero time
    ]
    with patch("reel_traffic_detection.data.feature_extractor.rdpcap", return_value=packets):
        yield

def test_feature_extractor_time_anomalies(mock_time_anomaly_rdpcap):
    extractor = FeatureExtractor()
    df = extractor.extract_from_pcap("dummy_time_anomaly.pcap")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    # Ensure inter_arrival_time column exists
    assert "avg_inter_arrival" in df.columns
    # Packet count should match
    assert df["packet_count"].iloc[0] == 4

