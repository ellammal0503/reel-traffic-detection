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



class RealTimeInference:
    def __init__(self, model_path: str, scaler_path: str = None):
        """
        Initialize inference pipeline.
        
        Args:
            model_path: Path to trained ML model (pickle or Hugging Face).
            scaler_path: Optional path to saved preprocessor/scaler.
        """
        self.model = joblib.load(model_path)
        
        if scaler_path:
            self.preprocessor = joblib.load(scaler_path)
        else:
            self.preprocessor = Preprocessor()  # fallback
        self.latencies = []

    def predict(self, features: pd.DataFrame):
        """
        Perform inference on a batch of features.
        
        Args:
            features: Pandas DataFrame with traffic features.
            
        Returns:
            tuple(pred_label, confidence_score)
        """
        start = time.time()
        X, _ = self.preprocessor.transform(features)
        probs = self.model.predict_proba(X)[0]
        label = int(np.argmax(probs))  # 0 = non-reel, 1 = reel/video
        confidence = float(np.max(probs))
        latency = time.time() - start
        self.latencies.append(latency)
        return label, confidence

    def average_latency(self):
        """
        Return average inference latency over observed predictions.
        """
        return np.mean(self.latencies) if self.latencies else 0.0


if __name__ == "__main__":
    # Quick test with dummy data
    dummy_features = pd.DataFrame([{
        "avg_packet_size": 500,
        "std_packet_size": 120,
        "avg_inter_arrival": 0.01,
        "packet_count": 100,
        "tcp_fraction": 0.7,
        "udp_fraction": 0.3,
        "duration": 5
    }])
    
    # Assume model + scaler saved previously
    rti = RealTimeInference(model_path="models/trained_model.pkl",
                            scaler_path="models/scaler.pkl")
    
    pred, conf = rti.predict(dummy_features)
    print(f"Prediction: {'Reel/Video' if pred==1 else 'Non-Reel'} (confidence={conf:.2f})")
    print(f"Avg latency: {rti.average_latency():.4f} sec")
