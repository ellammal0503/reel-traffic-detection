# 🔄 Training Pipeline

## 1. Objectives
The training pipeline must:
- Ingest raw traffic logs or synthetic datasets.  
- Perform preprocessing & feature extraction (real-time compatible).  
- Train baseline and advanced models.  
- Evaluate models on multiple metrics.  
- Package models for deployment (UE and server-side).  

---

## 2. Pipeline Stages

### Stage 1: Data Ingestion
- Input sources:
  - Public network traces (e.g., MAWI, ISP traffic datasets).  
  - Synthetic data from traffic simulators (see `02_data_collection.md`).  
- Format: CSV/Parquet with fields:  
  `timestamp, flow_id, direction, packet_size, protocol`  

---

### Stage 2: Preprocessing
- Drop malformed packets.  
- Normalize timestamps (relative per flow).  
- Assign **sliding windows** (1s with 250ms hop).  
- Label windows as **Video/Reel** or **Non-Video** (from ground truth).  

---

### Stage 3: Feature Engineering
- Extract metadata features (see `03_feature_engineering.md`):  
  - Byte/packet counts  
  - Rates and ratios  
  - Packet size distributions  
  - Timing features  
  - Burstiness  
  - Protocol flags  
  - Temporal cadence  

- Store feature vectors as `.npy` or `.csv` for training.  

---

### Stage 4: Dataset Splitting
- **Train/Validation/Test split** = 70/15/15 (flow-level, not packet-level, to avoid leakage).  
- Ensure balanced class distribution (Video vs Non-Video).  
- Optionally, apply stratified sampling.  

---

### Stage 5: Model Training
#### Mode A: Lightweight UE Model (LightGBM)
- Input: 12–15 engineered features.  
- Hyperparameters:
  - `num_leaves=31`, `max_depth=6`  
  - `learning_rate=0.05`  
  - `n_estimators=200`  
- Loss: Binary cross-entropy.  

#### Mode B: Temporal Deep Model (CNN + GRU)
- Input: 20s rolling sequences of features.  
- Architectu
