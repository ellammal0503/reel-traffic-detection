# 🎥 Real-time Detection of Reel vs Non-Reel Traffic in SNS Applications  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)  
[![PyTorch](https://img.shields.io/badge/ML-PyTorch-orange)](https://pytorch.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Tests](https://img.shields.io/badge/tests-pytest-success)](https://docs.pytest.org/)  

---

## 📌 Overview
Social networking services (SNS) like **Instagram, YouTube, TikTok, Facebook** transmit a mix of:  
- 🎬 **Video / Reel traffic** (short videos, continuous streaming)  
- 📰 **Non-video traffic** (feeds, images, text updates, ads)  

Since both share the same **network pipeline**, distinguishing them in **real time** is challenging.  

This project develops an **AI-powered classifier** that detects **video vs non-video flows** in real time, enabling:  
✅ Dynamic **resource allocation**  
✅ Improved **Quality of Experience (QoE)**  
✅ Robustness under **congestion, packet loss, and encryption**  

---

## 📂 Repository Structure
```bash
├── configs/              # ⚙️ YAML configs for training/eval/deployment
├── docs/                 # 📑 Technical documentation
│   ├── 01_problem_statement.md
│   ├── 02_data_collection.md
│   ├── 03_feature_engineering.md
│   ├── 04_model_design.md
│   ├── 05_training_pipeline.md
│   ├── 06_evaluation.md
│   ├── 07_deployment.md
│   ├── 08_robustness.md
│   └── 09_future_work.md
│
├── src/                  # 💻 Source code
│   ├── data/             # Data preprocessing scripts
│   ├── models/           # Model training + inference
│   ├── pipeline/         # Training / evaluation / deployment
│   └── robustness/       # Stress + adversarial testing
│
├── datasets/             # 📊 Dataset loaders or references
├── models/               # 🤖 Trained models (links or IDs)
├── notebooks/            # 📓 Jupyter experiments / EDA
├── tests/                # ✅ Unit and integration tests
├── requirements.txt      # Dependencies
├── pyproject.toml        # Project configuration
└── README.md             # Project overview


#Installation

# Clone the repository
git clone https://github.com/yourusername/reel-traffic-detection.git
cd reel-traffic-detection

# Create virtual environment
python3 -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt

# (Optional) Install in editable mode
pip install -e .



Train a model
python src/pipeline/train.py --config configs/train_config.yaml
🔹 Evaluate on test set
python src/pipeline/evaluate.py --config configs/eval_config.yaml
🔹 Run inference on traffic data
python src/pipeline/infer.py --input data/sample.pcap
🧪 Testing
Run unit and integration tests with pytest:
pytest tests/
📜 License
This project is licensed under the terms of the MIT License.
🤝 Contributing
Contributions are welcome!
Fork the repo
Create a feature branch
Submit a Pull Request 🚀
Please check CONTRIBUTING.md for details.
📌 Future Work
🔄 Support more advanced architectures (transformers, attention).
📲 On-device deployment (TensorFlow Lite / ONNX Runtime).
🌍 Integration with real-world network monitoring tools.
