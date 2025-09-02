# 🚀 Deployment Strategy

## 1. Objectives
The deployment goal is to ensure **real-time inference** of Reel (video) vs Non-Reel traffic:
- Low latency (< 5 ms on-device).  
- Lightweight footprint for mobile/UE deployment.  
- Scalable server-side support for monitoring and retraining.  

---

## 2. Deployment Targets
We design a **two-tier deployment** approach:

### 2.1 User Equipment (UE / Mobile Device)
- **Lightweight model (LightGBM or Logistic Regression)**.  
- Packaged as **ONNX** or **TensorFlow Lite** for Android/iOS apps.  
- Runs locally on device to classify flows in real-time.  
- Output → `video` or `non-video` label per 1s window.  
- Used for **adaptive QoS decisions** (buffering, pre-fetching, bitrate adaptation).  

### 2.2 Edge / Server Backend
- **Deep model (CNN+GRU)** deployed for heavy inference.  
- Handles large-scale monitoring and batch analysis.  
- Provides **feedback loop** for retraining UE models.  
- Deployment as:
  - **REST API** (FastAPI / Flask).  
  - **gRPC service** for low-latency streaming inference.  
  - Containerized with **Docker + Kubernetes** for scaling.  

---

## 3. Deployment Pipeline

### Step 1: Model Export
- Convert trained models to portable formats:
  - UE model → `model.onnx` / `model.tflite`.  
  - Server model → `model.pt` / `model.onnx`.  

### Step 2: Packaging
- Wrap inference code in:
  - **Android/iOS SDK** for mobile integration.  
  - **Python/Go API** for server integration.  
- Store artefacts in `models/` directory with versioning.  

### Step 3: Integration
- **UE**: Embed into SNS application’s network stack → classify flows before rendering.  
- **Server**: Integrate with traffic monitoring tools (e.g., Wireshark plugins, NetFlow analyzers).  

### Step 4: Monitoring
- Collect inference logs:
  - Confidence scores.  
  - Latency per request.  
  - Misclassifications (ground-truth if available).  
- Send anonymized feedback to backend for retraining.  

---

## 4. Deployment Architecture

  ┌───────────────────────┐
  │  User Equipment (UE)  │
  │  - ONNX/TFLite model  │
  │  - <5ms inference     │
  │  - Real-time QoS      │
  └─────────┬─────────────┘
            │
    Inference logs (lightweight)
            │
  ┌─────────▼─────────────┐
  │  Edge / Cloud Server  │
  │  - CNN+GRU model      │
  │  - REST/gRPC APIs     │
  │  - Continuous retrain │
  └─────────┬─────────────┘
            │
  ┌─────────▼─────────────┐
  │   Monitoring & Drift  │
  │   - MLflow/W&B        │
  │   - Alerts & updates  │
  └───────────────────────┘

---

## 5. Tools & Frameworks
- **ONNX Runtime** → lightweight inference on UE.  
- **TensorFlow Lite** → mobile-friendly ML deployment.  
- **FastAPI / Flask** → REST API serving.  
- **gRPC** → real-time streaming support.  
- **Docker + Kubernetes** → scalable cloud deployment.  
- **MLflow / Weights & Biases** → model versioning & monitoring.  

---

## 6. Deployment Validation
- Test with **live network traces**.  
- Measure:
  - UE inference latency.  
  - Battery & memory consumption.  
  - End-to-end QoS improvement (buffering reduction, faster loading).  
- Conduct **A/B testing** with real users (pilot rollout).  

---

## 7. Continuous Deployment (CD)
- Integrate CI/CD pipeline (GitHub Actions / GitLab CI).  
- Automated steps:
  1. Run unit + integration tests.  
  2. Build Docker images / mobile SDKs.  
  3. Deploy to staging.  
  4. Run load & latency tests.  
  5. Deploy to production with version tag.  

---

## 8. Summary
- **Two-tier deployment** → lightweight UE model + deep server model.  
- Portable model formats (ONNX, TFLite) ensure cross-platform support.  
- Continuous monitoring enables retraining under new traffic patterns.  
- Deployment pipeline ensures robustness, scalability, and adaptability.  
