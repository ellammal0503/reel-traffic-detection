# 📊 Model Evaluation

## 1. Objectives
The evaluation framework ensures that our model is not only **accurate** but also **robust, lightweight, and reliable** under real-time conditions.  
We focus on **both ML metrics** and **system-level KPIs** relevant to SNS applications.

---

## 2. Evaluation Dataset
- **Test Split**: 15% of total dataset (flow-level split to avoid leakage).  
- **Class Balance**: Equal representation of Video (Reel) and Non-Video flows.  
- **Conditions Tested**:
  - High bandwidth (low congestion).  
  - Medium bandwidth with jitter.  
  - Low bandwidth / packet loss (edge cases).  

---

## 3. Metrics

### 3.1 Classification Metrics
- **Accuracy** – Overall correct predictions.  
- **Precision** – Fraction of predicted video flows that are actually video.  
- **Recall** – Fraction of actual video flows detected correctly.  
- **F1-Score** – Harmonic mean of precision and recall.  
- **ROC-AUC** – Area under the ROC curve (robustness to thresholds).  

---

### 3.2 System Performance Metrics
- **Inference Latency (ms)** – Average prediction time per 1s window.  
- **Throughput (flows/sec)** – Number of flow windows processed per second.  
- **Model Size (MB)** – Important for UE/mobile deployment.  
- **Energy Efficiency** – Battery usage impact (approximated).  

---

### 3.3 Robustness Tests
- **Network Congestion**: Simulated 20%–40% packet loss.  
- **Coverage Variations**: Variable RTT and jitter.  
- **App Updates**: Traffic patterns may change with new app releases.  

---

## 4. Baseline Results (Expected)
*(To be filled after first experiments, placeholder values shown below)*  

| Model       | Accuracy | Precision | Recall | F1 | ROC-AUC | Latency (ms) | Model Size (MB) |
|-------------|----------|-----------|--------|----|---------|--------------|-----------------|
| LogisticReg | 82%      | 80%       | 79%    | 79%| 0.85    | 0.3          | 0.05            |
| LightGBM    | 91%      | 90%       | 91%    | 90%| 0.95    | 1.5          | 3.2             |
| CNN + GRU   | 94%      | 92%       | 94%    | 93%| 0.97    | 7.2          | 14.5            |

---

## 5. Error Analysis
- **False Positives (Non-video misclassified as Video)**  
  - Usually caused by image-heavy feeds (large packets).  
- **False Negatives (Video misclassified as Non-video)**  
  - Often seen in very short clips or reels with low bitrate.  
- **Edge Cases**  
  - Adaptive bitrate streaming (ABR) where packet bursts look like non-video.  

---

## 6. Visualization
- Confusion Matrix (Video vs Non-Video).  
- ROC Curve (per model).  
- Precision-Recall Curve.  
- Latency Distribution Histogram.  

*(To be auto-generated in `src/evaluation/plots.py`)*  

---

## 7. Deployment Readiness Criteria
A model is considered **deployment-ready** if:  
- Accuracy ≥ 90% on unseen data.  
- Latency ≤ 5 ms per inference on UE.  
- Model Size ≤ 5 MB (for mobile).  
- Robustness maintained under ≥ 30% packet loss.  

---

## 8. Continuous Evaluation
- Deploy a monitoring agent in UE/server pipeline.  
- Track metrics drift over time (e.g., drop in precision/recall).  
- Trigger retraining when drift > 5% over rolling 30-day window.  

---

## 9. Summary
- Evaluation goes beyond accuracy → includes **latency, size, and robustness**.  
- **LightGBM** is chosen for UE deployment due to best trade-off.  
- **CNN+GRU** serves server-side for deeper insights and retraining.  
- Continuous monitoring ensures adaptability to evolving SNS traffic.  
