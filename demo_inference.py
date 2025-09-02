"""
Demo inference script
---------------------
Loads trained model + scaler and runs predictions
"""

import pandas as pd
from src.reel_traffic_detection.models.realtime_inference import RealTimeInferenceML


"""
Demo Inference Script
---------------------
Supports:
  1. ML-based packet feature inference
  2. YOLO-based video inference
"""

import argparse
import pandas as pd
from src.reel_traffic_detection.models.realtime_inference import (
    RealTimeInferenceML,
    RealTimeInferenceYOLO,
)
import argparse
import pandas as pd
import joblib
import torch
import argparse
import pandas as pd
import joblib
import torch

# 🔑 Make sure the class name matches the one in your realtime_inference.py
from src.reel_traffic_detection.models.realtime_inference import RealTimeInferenceML

def run_ml_inference(data_path):
    print("\n🚀 Running ML Inference...")

    # Load your dataset
    import pandas as pd
    df = pd.read_csv(data_path)

    # Initialize with model + scaler
    rti_ml = RealTimeInferenceML(
        model_path="models/trained_model.pkl",
        scaler_path="models/scaler.pkl"
    )

    # Run prediction on first row (or all rows in a loop)
    sample = df.drop(columns=["label"], errors="ignore").iloc[0:1]
    pred, conf = rti_ml.predict(sample)

    print(f"✅ Prediction: {'Reel/Video' if pred==1 else 'Non-Reel'} (conf={conf:.2f})")

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_ml_inference(data_path):
    print("\n📊 Running ML Evaluation...")

    # Load dataset
    df = pd.read_csv(data_path)

    if "label" not in df.columns:
        print("⚠️ No 'label' column found in dataset. Skipping metrics.")
        return

    # Separate features and labels
    y_true = df["label"].values
    X = df.drop(columns=["label"])

    # Initialize inference pipeline
    rti_ml = RealTimeInferenceML(model_path="models/trained_model.pkl",
                                 scaler_path="models/scaler.pkl")

    preds = []
    confs = []

    for _, row in X.iterrows():
        pred, conf = rti_ml.predict(pd.DataFrame([row]))
        preds.append(pred)
        confs.append(conf)

    # Compute metrics
    acc = accuracy_score(y_true, preds)
    prec = precision_score(y_true, preds, zero_division=0)
    rec = recall_score(y_true, preds, zero_division=0)
    f1 = f1_score(y_true, preds, zero_division=0)

    print(f"✅ Accuracy:  {acc:.3f}")
    print(f"✅ Precision: {prec:.3f}")
    print(f"✅ Recall:    {rec:.3f}")
    print(f"✅ F1 Score:  {f1:.3f}")

    # Save results
    results = df.copy()
    results["pred"] = preds
    results["confidence"] = confs
    results.to_csv("predictions.csv", index=False)
    print("📂 Saved predictions to predictions.csv")


def run_yolo_inference(video_path):
    print("\n🚀 Running YOLO Inference...")

    rti_yolo = RealTimeInferenceYOLO("yolov8n.pt")
    results = rti_yolo.run_on_video(video_path, save_output=True)

    # Count objects across all frames
    obj_counts = {}
    for res in results:
        for cls_id in res.boxes.cls.cpu().numpy():
            cls_name = rti_yolo.model.names[int(cls_id)]
            obj_counts[cls_name] = obj_counts.get(cls_name, 0) + 1

    # Print summary
    print("🚦 YOLO Traffic Detection Complete")
    for cls, count in obj_counts.items():
        print(f"   {cls}: {count}")
    print("📂 Output saved to output_detected.mp4")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["ml", "yolo"], required=True, help="Inference mode")
    parser.add_argument("--data", type=str, required=True, help="Path to CSV dataset (for ML) or video (for YOLO)")
    args = parser.parse_args()

    if args.mode == "ml":
        run_ml_inference(args.data)
        evaluate_ml_inference(args.data)   # 👈 add this
    else:
        run_yolo_inference(args.data)
