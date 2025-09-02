# 📑 Data Collection

## 1. Objectives
The goal of data collection is to gather **packet-level metadata** (not payloads) from social networking applications and label it as either:
- **Video/Reel traffic** (short videos, reels, YouTube shorts, etc.)  
- **Non-video traffic** (feeds, scrolling, suggestions, chat, etc.)  

This dataset will support training and validating ML models that classify traffic **in real-time on user equipment (UE)**, helping optimize networks and monitor **Quality of Experience (QoE)**.

---

## 2. Principles
- **Privacy-Preserving**: No packet payloads or decrypted content are collected. Only metadata (timestamps, direction, size, protocol).  
- **Anonymized**: Flow/session identifiers are **hashed with salt** to prevent reversibility.  
- **Platform-Agnostic**: Works across multiple apps (Instagram, YouTube, Facebook, TikTok).  
- **Network-Aware**: Collected under varying conditions (Wi-Fi, 4G, 5G, congested links).  
- **Balanced**: Ensures adequate mix of video and non-video sessions.  
- **Compliant**: Respects data protection laws (e.g., GDPR, DPDP).

---

## 3. Collection Methods

### 3.1 On-Device Collection
- Use a **VPN Service (Android/iOS)** or **TUN interface** to capture packet headers.  
- Optionally collect raw **PCAP files**, then preprocess to CSV.  
- Record per-packet:
  - `ts` → timestamp (seconds)  
  - `dir` → direction (down/up)  
  - `size` → packet size (bytes)  
  - `proto` → transport protocol (TCP/QUIC)  
  - `flow_id` → anonymized 5-tuple (src/dst IP + port, hashed+salted)  

**Example raw log row:**
0.025, down, 1460, quic, flow123
0.030, up, 80, quic, flow123



### 3.2 Network Conditions
- Collect sessions under different environments:
  - High bandwidth (Wi-Fi, 5G)  
  - Limited bandwidth (throttled to 256 kbps, 1 Mbps)  
  - High latency (RTT 150–300 ms)  
  - With packet loss/jitter (0–5%)  

> Use Linux `tc netem` or mobile testbeds to emulate impairments.

### 3.3 Ground Truth Labeling
- **App instrumentation**: test app emits event when video playback starts/stops.  
- **Screen/UI logging**: record when user is on reel/short vs browsing feed.  
- **Heuristic bootstrap**: downstream bursts with segment cadence → video; sporadic bursts → non-video.  
- **Validation**: A subset of sessions is **manually checked** to avoid mislabels.

---

## 4. Data Storage Format

Final dataset stored as **CSV** with fields:

| Column     | Description |
|------------|-------------|
| `ts`       | Timestamp (s) |
| `dir`      | Direction (`up` / `down`) |
| `size`     | Packet size (bytes) |
| `proto`    | Transport protocol (`tcp` / `quic`) |
| `flow_id`  | Anonymized session/flow identifier |
| `label`    | Ground truth (0 = non-video, 1 = video) |

**Example:**
ts,dir,size,proto,flow_id,label
0.01,down,1460,quic,abc123,1
0.02,up,80,quic,abc123,1
0.05,down,1200,tcp,def456,0


> Raw PCAPs may also be archived separately for reproducibility.

---

## 5. Dataset Splits
- **Train (70%)** → sessions across multiple apps.  
- **Validation (15%)** → different days/users, used for tuning.  
- **Test (15%)** → unseen sessions, especially with impairments.  

⚠️ Important:  
- Split **by session/user**, not packet, to prevent leakage.  
- Ensure **class balance** in each split (similar video vs non-video ratio).  

---

## 6. Dataset Publishing
- Publish to **Hugging Face Datasets** or Zenodo.  
- Formats: **CSV (processed)** + optional **PCAP (raw)**.  
- License: **CC-BY 4.0** or similar.  
- Provide **baseline notebooks** (Colab/Jupyter) for quick exploration and replication.

---

## 7. Summary
- **Data source**: Tun/VPN capture of packet metadata (no payloads).  
- **Labeling**: Instrumentation + UI logging + heuristics (validated).  
- **Features**: Timestamps, directions, sizes, protocols, flow IDs.  
- **Conditions**: Clean + impaired networks.  
- **Final format**: CSV, session-based splits, labeled video vs non-video.  
- **Publishing**: Open dataset with baseline analysis notebooks.  

```mermaid
flowchart LR
    A[📱 User Device] --> B[🔒 VPN / TUN Interface]
    B --> C[📡 Packet Capture (PCAP)]
    C --> D[⚙️ Preprocessing Script]
    D --> E[📑 CSV Metadata (ts, dir, size, proto, flow_id)]
    E --> F[🏷️ Labeling (Video / Non-Video)]
    F --> G[📂 Final Dataset (Train/Val/Test)]


---

### 📊 Dataset Collection Flow (ASCII Version – if Mermaid not supported)

```markdown
[ User Device ]
       |
       v
[ VPN / TUN Capture ]
       |
       v
[ Raw PCAP Files ]
       |
       v
[ Preprocessing → CSV ]
       |
       v
[ Labeling (Video / Non-Video) ]
       |
       v
[ Final Dataset: Train / Validation / Test ]


```mermaid
flowchart LR
    A[📑 Dataset (CSV Metadata)] --> B[🔬 Feature Engineering]
    B --> C[🤖 Model Training (Classifier)]
    C --> D[✅ Evaluation & Validation]
    D --> E[📦 Deployed Model]
    E --> F[⚡ Real-time Inference]
    F --> G[📊 Traffic Classification: Video vs Non-Video]


---

### ⚡ End-to-End Workflow (ASCII Version)

```markdown
[ Dataset (CSV) ]
       |
       v
[ Feature Engineering ]
       |
       v
[ Model Training ]
       |
       v
[ Evaluation & Validation ]
       |
       v
[ Deployed Model ]
       |
       v
[ Real-time Inference → Video / Non-Video Classification ]
