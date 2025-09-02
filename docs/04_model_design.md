# 🧠 Model Design

## 1. Objectives
The model must:
- **Classify** real-time traffic windows as **Reel/Video traffic** or **Non-Reel/Non-Video traffic**.  
- **Operate on-device (UE side)** with minimal latency.  
- Be **robust to network conditions** (congestion, packet loss, RTT).  
- Remain **lightweight** for mobile/edge deployment.  

---

## 2. Input Features
Features are derived from traffic metadata (see `03_feature_engineering.md`):
- Volume: `down_bytes`, `up_bytes`, `total_pkts`  
- Rates: `down_rate`, `up_rate`, `d_u_byte_ratio`  
- Size distribution: `down_pkts_large_pct`, `down_pkts_small_pct`  
- Timing: `mean_iat_down`, `std_iat_down`, `p95_iat_down`  
- Burstiness: `burstiness`  
- Protocol flags: `proto_quic`, `proto_tcp`  
- Temporal cadence: `cadence_score`  

Input vector dimension ≈ 12–15 per sliding window.  

---

## 3. Model Candidates

### 3.1 Lightweight ML Models
- **Logistic Regression / SVM**  
  - Pros: Very fast, interpretable.  
  - Cons: May underperform for bursty traffic.  

- **Random Forest / Gradient Boosted Trees (LightGBM/XGBoost)**  
  - Pros: Handle non-linearities & feature interactions.  
  - Cons: Larger model size; need pruning for UE.  

### 3.2 Deep Learning Models
- **Shallow MLP (2–3 dense layers)**  
  - Pros: Captures feature interactions.  
  - Cons: Needs careful tuning for low latency.  

- **Temporal CNN / RNN (LSTM/GRU)**  
  - Pros: Capture packet arrival dynamics over time windows.  
  - Cons: Higher compute cost, but can be pruned/quantized.  

---

## 4. Proposed Hybrid Architecture
Given trade-offs, we propose **two deployment modes**:

### Mode A (Lightweight, On-Device ML)
- Input: 12–15 engineered features per 1s window.  
- Model: **Gradient Boosted Decision Trees (LightGBM)** with depth ≤ 6.  
- Output: Binary classification {Video, Non-Video}.  
- Latency: < 2 ms per inference.  
- Accuracy Target: >90%.  

### Mode B (Temporal Deep Learning for Server-Side Analysis)
- Input: 20-second rolling window of features.  
- Model: **1D CNN + GRU** for temporal dependencies.  
- Use case: Offline / edge server for model improvement & drift detection.  

---

## 5. Training Setup
- **Loss function:** Binary Cross-Entropy.  
- **Optimizer:** Adam (for neural nets), default for LightGBM.  
- **Metrics:** Accuracy, Precision, Recall, F1-score, ROC-AUC.  
- **Regularization:**  
  - Early stopping on validation set.  
  - Dropout (for neural nets).  
  - Max depth and feature subsampling (for GBDTs).  

---

## 6. Real-Time Inference Pipeline
1. Collect packet logs → Extract features (1s sliding window).  
2. Normalize features → Pass through trained model.  
3. Predict class (Reel vs Non-Reel).  
4. UE adapts (e.g., video buffer optimization, QoS tuning).  

---

## 7. Deployment Strategy
- **UE-side:** Export model to ONNX or TensorFlow Lite for mobile inference.  
- **Server-side:** Use PyTorch/LightGBM model for batch training and monitoring.  
- **Continuous Learning:** Retrain periodically with new data (concept drift adaptation).  

---

## 8. Summary
- **Two-tier design**: Lightweight GBDT for real-time UE-side inference, CNN+GRU for server-side refinement.  
- Features are metadata-based, ensuring **privacy & efficiency**.  
- Deployment pipeline supports **dynamic adaptation** in SNS apps under varying network conditions.  
