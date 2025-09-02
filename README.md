# Reel Traffic vs Non-Reel Traffic Detection

This project provides a real-time AI model that classifies **video traffic (reels/shorts)** vs **non-video traffic (feeds/suggestions)** in a social networking application.

##  Features
- Real-time inference on packet metadata (no payload inspection).
- Works under varying network conditions (congestion, latency, packet loss).
- Lightweight for mobile devices (low CPU & RAM).

## Repo Structure
- `docs/` → All technical documentation in Markdown.
- `src/` → Source code for training + real-time inference.
- `models/` → Hugging Face model links or trained weights.
- `datasets/` → Datasets used/published.
- `requirements.txt` → Python dependencies.
- `setup.py` → Package installer.

##  Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Train baseline model
python src/models/train.py --data sample_packets.csv

# Run real-time detector (demo)
python src/app/demo_service.py --pcap sample.pcap

# Reel Traffic Detection (AI Challenge Project)

##  Project Goal
This project detects whether network traffic belongs to **Reel/Video streams** or **Non-Reel traffic** in real-time using Machine Learning (ML).  
It extracts statistical features from packet captures (pcaps) and performs classification with a trained ML model.

---

## Project Structure
reel-traffic-detection/
│── src/ # Source code
│ ├── data/ # Preprocessing, feature extraction
│ ├── model/ # ML model training & inference
│ └── reel_traffic_detection/ # Core package
│
│── tests/ # Unit & integration tests (pytest)
│── models/ # Saved models and scalers
│── pyproject.toml # Dependencies and pytest config
│── README.md # Documentation (this file)

---

## ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/reel-traffic-detection.git
   cd reel-traffic-detection

Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate    # (Linux/Mac)
venv\Scripts\activate       # (Windows)
Install dependencies:
pip install -r requirements.txt
🧪 Running Tests
The project uses pytest for testing. Run:
pytest -v
You should see all unit tests pass (feature extraction, helpers, real-time inference, etc.).

Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate    # (Linux/Mac)
venv\Scripts\activate       # (Windo

Usage
🔹 Training
python src/pipeline/train.py --config configs/train_config.yaml
🔹 Evaluation
python src/pipeline/evaluate.py --model checkpoints/model_best.pth
🔹 Real-time Inference
python src/pipeline/inference.py --input traffic.pcap
🔹 Video Object Detection (YOLO-based)
python detect.py --source data/sample_video.mp4 --output output_detected.mp4



(venv) (base) karthickkumarasamy@Karthicks-MacBook-Air reel-traffic-detection %
python demo_inference.py --mode yolo --data data/MGR.mp4

: 384x640 8 persons, 3 cups, 29.9ms
Speed: 0.5ms preprocess, 29.9ms inference, 0.8ms postprocess per image at shape (1, 3, 384, 640)

0: 384x640 4 persons, 2 cups, 30.7ms
Speed: 0.5ms preprocess, 30.7ms inference, 0.5ms postprocess per image at shape (1, 3, 384, 640)

0: 384x640 6 persons, 3 cups, 30.4ms
Speed: 0.5ms preprocess, 30.4ms inference, 0.6ms postprocess per image at shape (1, 3, 384, 640)

📊 Detection Summary:
  person: 4623
  tie: 55
  chair: 101
  umbrella: 38
  handbag: 3
  cell phone: 3
  baseball glove: 3
  remote: 3
  dining table: 94
  laptop: 25
  cup: 56
  tv: 2
  book: 2
  train: 6
  bed: 3
  cake: 4
  potted plant: 28
  bus: 29
  car: 5
  parking meter: 2
  truck: 4
  traffic light: 1
  bottle: 8
  bird: 2
  cow: 2
🚦 YOLO Traffic Detection Complete
   person: 4623
   tie: 55
   chair: 101
   umbrella: 38
   handbag: 3
   cell phone: 3
   baseball glove: 3
   remote: 3
   dining table: 94
   laptop: 25
   cup: 56
   tv: 2
   book: 2
   train: 6
   bed: 3
   cake: 4
   potted plant: 28
   bus: 29
   car: 5
   parking meter: 2
   truck: 4
   traffic light: 1
   bottle: 8
   bird: 2
   cow: 2
📂 Output saved to output_detected.mp4


(venv) (base) karthickkumarasamy@Karthicks-MacBook-Air reel-traffic-detection %
python demo_inference.py --mode ml --data datasets/traffic_dataset.csv


🚀 Running ML Inference...
✅ Prediction: Reel/Video (conf=1.00)

📊 Running ML Evaluation...
✅ Accuracy:  1.000
✅ Precision: 1.000
✅ Recall:    1.000
✅ F1 Score:  1.000
📂 Saved predictions to predictions.csv
(venv) (base) karthickkumarasamy@Karthicks-MacBook-Air reel-traffic-detection % 
