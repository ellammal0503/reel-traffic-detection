# 🎬 reel-traffic-detection  

**AI-based system to detect video and non-video traffic in social networking apps in real-time**  

---

##  Description  
This repository contains the implementation of an **AI model for real-time classification of social networking traffic** into **Reel/Video vs Non-Video**.  
The project is part of the **Samsung EnnovateX 2025 AI Challenge**.  

SNS apps (e.g., Instagram, Facebook, YouTube) transmit both **short videos/reels** and **non-video traffic (feeds, suggestions, browsing)** through the same data pipeline.  
Our system enables **user equipment (UE)** to:  

-  Detect **Reel/Video vs Non-Video traffic in real-time**  
-  Optimize device/network performance under **congestion & varying coverage**  
-  Achieve **high classification accuracy** using hybrid ML/DL models  

---

##  Features  
- **YOLOv8** for video frame/traffic pattern detection  
- **MLP (Multi-Layer Perceptron)** for feature-based classification  
- **Real-time inference pipeline** (`demo_inference.py`)  
- **Evaluation metrics**: Accuracy, Precision, Recall, F1  
- **Unit tests with Pytest** for reproducibility  

---

##  Problem Statement — *#9: Real-time Detection of Reel vs Non-Reel Traffic*  
SNS applications (such as Facebook and YouTube) transmit both video (short videos, reels, etc.) and non-video traffic (feeds, suggestions, etc.) through the same data pipeline.  

The challenge is to **develop an AI model** to differentiate **Reel/Video vs Non-Video traffic** in real-time, enabling **UE to optimize performance dynamically**, while ensuring **accuracy under varying network congestion and coverage conditions**.  

---

## 👥 Team  
- **Team Name**: Solo Team  
- **Team Member**: Karthick Kumarasamy  
## 🎥 Demo Video  
📺 https://youtu.be/89NLqLwhEgU

---

## 📂 Repository Structure  
```bash
reel-traffic-detection/
│── datasets/                # Sample traffic datasets
│── models/                  # Trained YOLOv8 & MLP models
│── outputs/                 # Prediction results & demo videos
│── src/                     # Core source code
│   ├── feature_extractor.py
│   ├── train_model.py       # Training scripts (YOLOv8 + MLP)
│   ├── realtime_inference.py
│   └── helpers.py
│── tests/                   # Unit & integration tests
│── demo_inference.py        # Script for demo inference
│── requirements.txt         # Runtime dependencies
│── requirements-dev.txt     # Dev dependencies (testing, linting)
│── README.md                # Project documentation



## ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ellammal0503/reel-traffic-detection.git
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
