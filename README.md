# 🧠 MelanoAI — Skin Lesion Classification with Grad-CAM Explainability

**MelanoAI** is a deep learning-powered web application designed for preliminary classification of skin lesion images into three categories: `benign`, `malignant`, and `invalid` (non-skin images). It features a clean Streamlit UI, model explainability via Grad-CAM, and an integrated logging system.

> ⚠️ **Disclaimer**  
> This is the first version of MelanoAI. The current model is **not clinically validated** and may produce **unreliable predictions**. It should **not** be used for any medical diagnosis or decision-making.  
> **Use for research, demonstration, and educational purposes only.**

---

## 🚀 Features

- 🖼️ Upload and classify skin lesion images (`benign`, `malignant`, `invalid`)
- 📈 Model confidence display
- 🔥 Grad-CAM heatmap overlay for interpretability
- 🧾 Prediction logging system (CSV)
- 🔐 Optional user authentication with SQLite
- 📄 Downloadable prediction report (PDF)
- 📦 Modular architecture, ready for production-scale improvements

---

## 🧪 Model Overview

- Model: **Custom CNN** with optional MobileNetV2 backbone
- Input Shape: `(224, 224, 3)`
- Classes: `benign`, `malignant`, `invalid`
- Trained on: [HAM10000 dataset](https://www.kaggle.com/kmader/skin-cancer-mnist-ham10000) + 1000 curated invalid images
- Training strategy:
  - Data Augmentation
  - Class Balancing
  - EarlyStopping
  - Grad-CAM support via final convolutional layers

---

## 🧠 Known Limitations

- **High false positive rate** for `malignant` on invalid images
- **Misclassification of real benign cases** as malignant
- **Overfitting risk** due to limited data diversity
- Grad-CAM may not always align with clinically relevant regions
- Currently lacks robustness for real-world generalization

> This version is primarily for **demonstration and portfolio use** — real medical deployment would require extensive retraining, augmentation, testing, and regulatory compliance.

---

## 📦 Installation

### 1. Clone the repo:

git clone https://github.com/your-username/MelanoAI.git
cd MelanoAI

2. Create a virtual environment:

python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

### 3. Install dependencies:

pip install -r requirements.txt

## Run the App

streamlit run app/main.py
