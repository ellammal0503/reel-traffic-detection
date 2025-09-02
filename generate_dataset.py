"""
Synthetic Dataset Generator for Reel vs Non-Reel Traffic
--------------------------------------------------------
Usage:
    python generate_dataset.py --out datasets/traffic_dataset.csv --n 200
"""

import argparse
import pandas as pd
import numpy as np
import os

def generate_synthetic_dataset(n_samples=200, seed=42):
    np.random.seed(seed)

    data = []

    for i in range(n_samples):
        if i % 2 == 0:  # Reel/Video traffic
            avg_packet_size = np.random.normal(600, 50)   # larger packets
            std_packet_size = np.random.normal(100, 20)
            avg_inter_arrival = np.random.normal(0.02, 0.005)  # more frequent
            packet_count = np.random.randint(80, 150)
            tcp_fraction = np.random.uniform(0.6, 0.9)
            udp_fraction = 1 - tcp_fraction
            duration = np.random.uniform(3, 8)
            label = 1  # reel/video
        else:  # Non-reel traffic
            avg_packet_size = np.random.normal(300, 40)
            std_packet_size = np.random.normal(50, 10)
            avg_inter_arrival = np.random.normal(0.1, 0.02)  # less frequent
            packet_count = np.random.randint(10, 50)
            tcp_fraction = np.random.uniform(0.2, 0.6)
            udp_fraction = 1 - tcp_fraction
            duration = np.random.uniform(0.5, 3)
            label = 0  # non-reel

        data.append([
            avg_packet_size,
            std_packet_size,
            avg_inter_arrival,
            packet_count,
            tcp_fraction,
            udp_fraction,
            duration,
            label
        ])

    df = pd.DataFrame(data, columns=[
        "avg_packet_size",
        "std_packet_size",
        "avg_inter_arrival",
        "packet_count",
        "tcp_fraction",
        "udp_fraction",
        "duration",
        "label"
    ])

    return df


def main(args):
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df = generate_synthetic_dataset(n_samples=args.n)
    df.to_csv(args.out, index=False)
    print(f"✅ Synthetic dataset saved to {args.out} with {args.n} rows.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="datasets/traffic_dataset.csv",
                        help="Path to save synthetic dataset CSV")
    parser.add_argument("--n", type=int, default=200,
                        help="Number of samples to generate")
    args = parser.parse_args()
    main(args)
