import joblib
import pandas as pd
import argparse

# Load trained model
clf = joblib.load("video_classifier.pkl")

def run_demo(pcap_file):
    # Placeholder: Convert pcap -> features
    print(f"Processing {pcap_file}...")
    df = pd.read_csv("demo_features.csv")  # Replace with real extractor
    preds = clf.predict(df)
    for i, p in enumerate(preds):
        print(f"Window {i}: {'VIDEO' if p==1 else 'NON-VIDEO'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pcap", type=str, required=True, help="PCAP file to analyze")
    args = parser.parse_args()
    run_demo(args.pcap)
