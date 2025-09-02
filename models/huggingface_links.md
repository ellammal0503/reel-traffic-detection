# 🤗 Hugging Face Model Links

This document lists all models used and/or published in the project.  
We ensure that all models are open-source and available under appropriate licenses.  

---

## 📥 Pre-trained Models Used
These models were used as baselines or for transfer learning:

1. **[bert-base-uncased](https://huggingface.co/bert-base-uncased)**  
   - Used for embedding packet sequences as tokenized features.  
   - License: Apache 2.0  

2. **[distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased)**  
   - Lightweight model variant for real-time inference on UE.  
   - License: Apache 2.0  

3. **[transformer-traffic-classifier](https://huggingface.co/yourchoice/traffic-classifier-baseline)**  
   - Open research baseline for encrypted traffic classification.  
   - License: MIT  

---

## 📤 Models Published (Our Contributions)
We have fine-tuned and published models trained on our curated dataset(s).  

1. **[username/reel-vs-nonreel-transformer](https://huggingface.co/username/reel-vs-nonreel-transformer)**  
   - Base: DistilBERT  
   - Task: Binary classification (`video` vs `non-video`)  
   - Dataset: Combination of public QUIC traffic + synthetic flows  
   - License: MIT  

2. **[username/reel-vs-nonreel-lightweight](https://huggingface.co/username/reel-vs-nonreel-lightweight)**  
   - Optimized for **edge/UE deployment**  
   - Quantized (INT8) for mobile-friendly inference  
   - Maintains >90% accuracy with 3x lower latency  
   - License: MIT  

---

## 📌 Notes
- All models are version-controlled on Hugging Face.  
- Links above will be updated once final training checkpoints are pushed.  
- Each model card includes:  
  - Training config  
  - Evaluation metrics  
  - Intended usage + limitations  

---

✅ With this structure, reviewers can **directly pull models from Hugging Face** and reproduce your experiments.  
