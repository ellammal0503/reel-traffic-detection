"""
Helper Utilities
----------------
Common helper functions for logging, model saving/loading, 
synthetic traffic generation, and timing.
"""

import os
import joblib
import json
import random
import time
import numpy as np
import pandas as pd


def save_model(model, path: str):
    """
    Save a trained model to disk.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"[INFO] Model saved at {path}")


def load_model(path: str):
    """
    Load a trained model from disk.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
    return joblib.load(path)


def save_json(data: dict, path: str):
    """
    Save dictionary as JSON.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[INFO] JSON saved at {path}")


def load_json(path: str) -> dict:
    """
    Load JSON into dictionary.
    """
    with open(path, "r") as f:
        return json.load(f)


def generate_synthetic_traffic(n_samples=100, video_ratio=0.5):
    """
    Generate synthetic traffic data for testing.
    
    Args:
        n_samples (int): number of samples to generate
        video_ratio (float): proportion of reel/video samples
    
    Returns:
        Pandas DataFrame with features + labels
    """
    data = []
    for _ in range(n_samples):
        is_video = 1 if random.random() < video_ratio else 0
        if is_video:
            # Reel/Video traffic tends to have higher packet count, smaller inter-arrival times
            avg_packet_size = random.randint(400, 1200)
            std_packet_size = random.randint(80, 200)
            avg_inter_arrival = round(random.uniform(0.005, 0.02), 4)
            packet_count = random.randint(80, 300)
            duration = random.uniform(5, 20)
            tcp_fraction = round(random.uniform(0.6, 0.9), 2)
            udp_fraction = 1 - tcp_fraction
        else:
            # Non-reel traffic = browsing, feeds → fewer packets, longer inter-arrival
            avg_packet_size = random.randint(100, 600)
            std_packet_size = random.randint(20, 100)
            avg_inter_arrival = round(random.uniform(0.05, 0.2), 4)
            packet_count = random.randint(10, 80)
            duration = random.uniform(1, 10)
            tcp_fraction = round(random.uniform(0.4, 0.8), 2)
            udp_fraction = 1 - tcp_fraction

        data.append({
            "avg_packet_size": avg_packet_size,
            "std_packet_size": std_packet_size,
            "avg_inter_arrival": avg_inter_arrival,
            "packet_count": packet_count,
            "tcp_fraction": tcp_fraction,
            "udp_fraction": udp_fraction,
            "duration": duration,
            "traffic_type": is_video
        })

    return pd.DataFrame(data)


def measure_latency(func, *args, **kwargs):
    """
    Measure execution time of a function.
    """
    start = time.time()
    result = func(*args, **kwargs)
    latency = time.time() - start
    return result, latency


if __name__ == "__main__":
    # Demo: generate fake traffic
    df = generate_synthetic_traffic(5)
    print("[DEBUG] Sample synthetic traffic:\n", df.head())

    # Demo: latency check
    _, latency = measure_latency(sum, [1, 2, 3])
    print(f"[DEBUG] Sum latency = {latency:.6f} sec")
