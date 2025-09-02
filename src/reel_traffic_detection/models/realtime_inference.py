"""
Real-time Inference for Reel vs Non-Reel Traffic
------------------------------------------------
This module performs real-time classification of network traffic
into reel/video vs non-reel categories using a trained ML model.

Usage:
    from src.model.realtime_inference import RealTimeInference
    import pandas as pd
    
    rti = RealTimeInference(model_path="models/trained_model.pkl")
    sample_features = pd.DataFrame([{
        "avg_packet_size": 450,
        "std_packet_size": 110,
        "avg_inter_arrival": 0.02,
        "packet_count": 80,
        "tcp_fraction": 0.6,
        "udp_fraction": 0.4,
        "duration": 4
    }])
    prediction, confidence = rti.predict(sample_features)
"""

import joblib
import time
import numpy as np
import pandas as pd
#from src.data.preprocessor import Preprocessor
from src.reel_traffic_detection.data.preprocess import Preprocessor

# src/model/realtime_inference.py

"""
Real-time Inference
-------------------
This module provides two modes of inference:

1. RealTimeInferenceML
   - Classifies reel vs non-reel traffic using tabular features and a trained ML model.

2. RealTimeInferenceYOLO
   - Detects vehicles/traffic in video streams using a pretrained YOLO model.
"""

import joblib
import time
import numpy as np
import pandas as pd
from pathlib import Path

# For YOLO
from ultralytics import YOLO
import cv2

# Import your preprocessor
from src.reel_traffic_detection.data.preprocess import Preprocessor


# ================================
# 1. Packet Feature ML Inference
# ================================
class RealTimeInferenceML:
    def __init__(self, model_path: str, scaler_path: str = None):
        """
        Initialize inference pipeline.
        
        Args:
            model_path: Path to trained ML model (pickle or Hugging Face).
            scaler_path: Optional path to saved preprocessor/scaler.
        """
        # Always load model (will raise error if missing)
        self.model = joblib.load(model_path)

        # Load preprocessor if provided, else fallback
        if scaler_path:
            self.preprocessor = joblib.load(scaler_path)
        else:
            self.preprocessor = Preprocessor()

        self.latencies = []


    def predict(self, features: pd.DataFrame):
        """
        Perform inference on a batch of features.
        Auto-aligns features with training-time feature names.
    
        Args:
            features: Pandas DataFrame with traffic features.
        
        Returns:
            tuple(pred_label, confidence_score)
        """
        start = time.time()
        # Auto-clean features before transform
        if "label" in features.columns:
            features = features.drop(columns=["label"])

        if hasattr(self.preprocessor, "feature_names_in_"):
            expected_features = list(self.preprocessor.feature_names_in_)
            # Keep only expected features
            features = features[[col for col in expected_features if col in features.columns]]

        X = self.preprocessor.transform(features)

        probs = self.model.predict_proba(X)[0]
        label = int(np.argmax(probs))  # 0 = non-reel, 1 = reel/video
        confidence = float(np.max(probs))

        latency = time.time() - start
        self.latencies.append(latency)
        return label, confidence


    def average_latency(self):
        return np.mean(self.latencies) if self.latencies else 0.0


# ================================
# 2. YOLO Video Traffic Inference
# ================================
class RealTimeInferenceYOLO:
    def __init__(self, model_name: str = "yolov8n.pt"):
        """
        Initialize YOLO-based traffic detection.
        Args:
            model_name: pretrained YOLO model (e.g., 'yolov8n.pt', 'yolov8s.pt')
        """
        self.model = YOLO(model_name)

    def run_on_video(self, video_path: str, save_output: bool = False):
        """
        Run YOLO inference on a video file.
        Args:
            video_path: Path to video file
            save_output: If True, saves annotated video
        Returns:
            results: list of detection outputs
        """
        cap = cv2.VideoCapture(video_path)
        results = []
        out = None

        if save_output:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter("output_detected.mp4", fourcc,
                                  cap.get(cv2.CAP_PROP_FPS),
                                  (int(cap.get(3)), int(cap.get(4))))

        # Dictionary to count detections
        detection_counts = {}

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLO prediction
            preds = self.model(frame)[0]
            results.append(preds)

            # Count detections
            for box in preds.boxes:
                cls_id = int(box.cls[0])
                cls_name = self.model.names[cls_id]
                detection_counts[cls_name] = detection_counts.get(cls_name, 0) + 1

            # Draw results on frame
            annotated = preds.plot()

            if save_output:
                out.write(annotated)

            # (Optional: display live)
            cv2.imshow("Traffic Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()

        # Print summary
        print("\n📊 Detection Summary:")
        for cls_name, count in detection_counts.items():
            print(f"  {cls_name}: {count}")

        return results


# ================================
# Quick Test
# ================================
if __name__ == "__main__":
    # --- Test ML-based inference ---
    dummy_features = pd.DataFrame([{
        "avg_packet_size": 500,
        "std_packet_size": 120,
        "avg_inter_arrival": 0.01,
        "packet_count": 100,
        "tcp_fraction": 0.7,
        "udp_fraction": 0.3,
        "duration": 5
    }])

    rti_ml = RealTimeInferenceML(model_path="models/trained_model.pkl",
                                 scaler_path="models/scaler.pkl")
    pred, conf = rti_ml.predict(dummy_features)
    print(f"[ML] Prediction: {'Reel/Video' if pred==1 else 'Non-Reel'} (conf={conf:.2f})")

    # --- Test YOLO inference on video ---
    # rti_yolo = RealTimeInferenceYOLO("yolov8n.pt")
    # rti_yolo.run_on_video("data/sample_traffic.mp4", save_output=True)
