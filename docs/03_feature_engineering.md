# 🎛️ Feature Engineering

## 1. Objectives
The raw packet logs (timestamp, size, direction, protocol, flow ID) must be transformed into **numerical features** that capture the statistical differences between **video/reel traffic** and **non-video traffic**.  

Feature engineering is critical to:
- Achieve **real-time classification** (low latency, low CPU).  
- Ensure **robustness** under varying network conditions (congestion, packet loss, RTT changes).  
- Maintain **privacy** (no payload inspection, metadata only).  

---

## 2. Windowing Strategy
Traffic is processed in **sliding windows** of fixed duration.  
- **Window size**: 1 second (captures burst patterns).  
- **Hop size**: 250 ms (overlap improves responsiveness).  
- Features are computed per window, then fed to the model.  

This allows near real-time updates every 250 ms while keeping context.

---

## 3. Core Features

### 3.1 Byte & Packet Counts
- `down_bytes` → total downstream bytes in window  
- `up_bytes` → total upstream bytes in window  
- `total_pkts` → total packets (up + down)  

These distinguish heavy downstream video streams from lighter feed traffic.

---

### 3.2 Rates
- `down_rate` = downstream bytes / window duration  
- `up_rate` = upstream bytes / window duration  
- `d_u_byte_ratio` = (down_bytes + 1) / (up_bytes + 1)  

Video → high, steady downstream; low upstream (except ACKs).  
Feeds → more balanced traffic (especially small requests upstream).  

---

### 3.3 Packet Size Distribution
- `down_pkts_large_pct` = % of downstream packets > 800B  
- `down_pkts_small_pct` = % of downstream packets < 200B  

Video → dominated by large MTU-sized packets.  
Feeds → many small control packets.  

---

### 3.4 Timing Features
- `mean_iat_down` = mean inter-arrival time (downstream packets)  
- `std_iat_down` = standard deviation of inter-arrival times  
- `p95_iat_down` = 95th percentile of inter-arrival times  

Video → low mean & variance (steady packet flow).  
Non-video → bursty, irregular timing.  

---

### 3.5 Burstiness
- `burstiness = std(rate) / mean(rate)` within window.  

Captures variability — video is smoother, feeds more spiky.  

---

### 3.6 Transport Protocol Indicators
- `proto_quic` = 1 if QUIC packets present, else 0  
- `proto_tcp` = 1 if TCP packets present, else 0  

Some apps deliver reels via QUIC/HTTP3, others over TCP/DASH.  

---

### 3.7 Temporal Cadence (Contextual)
Over the **last 10–20 seconds**, apply FFT or autocorrelation to downstream byte series to extract **segment request cadence** (e.g., 2–6s cycle typical of DASH/HLS video).  

Feature:  
- `cadence_score` = normalized FFT peak strength in 0.2–0.6 Hz band.  

---

## 4. Feature Table

| Category      | Feature                | Description |
|---------------|------------------------|-------------|
| Volume        | `down_bytes`, `up_bytes`, `total_pkts` | Basic counts |
| Rate          | `down_rate`, `up_rate`, `d_u_byte_ratio` | Traffic intensity |
| Size Dist.    | `down_pkts_large_pct`, `down_pkts_small_pct` | MTU vs control packets |
| Timing        | `mean_iat_down`, `std_iat_down`, `p95_iat_down` | Packet spacing |
| Burstiness    | `burstiness`           | Variability |
| Protocol      | `proto_quic`, `proto_tcp` | Transport layer |
| Cadence       | `cadence_score`        | Video segment periodicity |

---

## 5. Normalization
- **Scale numeric features** (bytes, rates, IATs) → `StandardScaler` or min-max normalization.  
- **Binary features** (proto flags) kept as-is.  

---

## 6. Real-Time Constraints
- Feature computation must finish in **≤5 ms per window** on mid-tier UE hardware.  
- Maintain rolling buffers for inter-arrival times and 10–20s history for cadence.  

---

## 7. Summary
- Features derived only from **metadata** (safe & privacy-friendly).  
- Focus on **volume, rate, timing, burstiness, protocol mix, cadence**.  
- Window-based + rolling features make classification stable in **real-time**.  
- Balanced between **accuracy** and **computational efficiency** for on-device deployment.  
