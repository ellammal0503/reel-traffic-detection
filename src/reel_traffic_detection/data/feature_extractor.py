"""
Feature Extractor for Reel vs Non-Reel Traffic
---------------------------------------------
This module processes raw network traffic and extracts features
for classification into video (reel) vs non-video traffic.

Usage:
    from src.data.feature_extractor import FeatureExtractor
    
    extractor = FeatureExtractor()
    features = extractor.extract_from_pcap("data/sample.pcap")
"""

import numpy as np
import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FeatureExtractor")


class FeatureExtractor:
    def __init__(self):
        """
        Initialize feature extractor with configurable params if needed.
        """
        pass

    def _extract_packet_features(self, packet):
        """
        Extract raw packet-level features (size, protocol, direction).
        """
        size = len(packet)
        proto = (
            "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "OTHER"
        )
        return {
            "packet_size": size,
            "protocol": proto,
            "src": packet[IP].src if packet.haslayer(IP) else None,
            "dst": packet[IP].dst if packet.haslayer(IP) else None,
            "time": packet.time,
        }

    def extract_from_pcap(self, filepath: str) -> pd.DataFrame:
        """
        Extract flow-level features from PCAP file.
        Returns a Pandas DataFrame of aggregated features.
        """
        packets = rdpcap(filepath)
        logger.info(f"Loaded {len(packets)} packets from {filepath}")

        packet_records = []
        for pkt in packets:
            try:
                features = self._extract_packet_features(pkt)
                packet_records.append(features)
            except Exception:
                continue

        df = pd.DataFrame(packet_records)

        if df.empty:
            logger.warning("No valid packets parsed!")
            return df

        # Compute derived features
        df["inter_arrival_time"] = df["time"].diff().fillna(0)
        df["is_tcp"] = (df["protocol"] == "TCP").astype(int)
        df["is_udp"] = (df["protocol"] == "UDP").astype(int)

        # Aggregate flow-level stats
        summary = {
            "avg_packet_size": df["packet_size"].mean(),
            "std_packet_size": df["packet_size"].std(),
            "min_packet_size": df["packet_size"].min(),
            "max_packet_size": df["packet_size"].max(),
            "avg_inter_arrival": df["inter_arrival_time"].mean(),
            "packet_count": len(df),
            "tcp_fraction": df["is_tcp"].mean(),
            "udp_fraction": df["is_udp"].mean(),
            "duration": df["time"].iloc[-1] - df["time"].iloc[0]
            if len(df) > 1
            else 0,
        }

        return pd.DataFrame([summary])


if __name__ == "__main__":
    # Example run for quick testing
    extractor = FeatureExtractor()
    features = extractor.extract_from_pcap("data/sample.pcap")
    print(features)
