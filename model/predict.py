import numpy as np
from tensorflow.keras.models import load_model
from utils.preprocessing import preprocess_image
import os
from datetime import datetime
import json

# Load model
model = load_model("model/skin_cancer_model.keras")

# Load model metadata
with open("model_metadata.json", "r") as f:
    metadata = json.load(f)
model_version = metadata.get("version", "1.0")

# Class labels — should match your training labels
class_names = ["benign", "malignant", "invalid"]

# Confidence threshold to reject uncertain predictions
REJECTION_THRESHOLD = 0.80

def predict_image(img_path):
    """
    Predicts class from image path.
    Returns: label (str), confidence (float), raw_preds (np.array)
    """
    x = preprocess_image(img_path, target_size=(224, 224))  # (1, 224, 224, 3)
    preds = model.predict(x)[0]  # shape: (3,) for 3 classes

    idx = int(np.argmax(preds))
    confidence = float(preds[idx])

    # Reject low-confidence predictions
    if confidence < REJECTION_THRESHOLD:
        label = "unknown"
        print(f"[INFO] Rejected prediction — confidence too low: {confidence:.2f}")
    elif idx >= len(class_names):
        label = "unknown"
        confidence = 0.0
        print(f"[ERROR] Invalid prediction index: {idx} — probs: {preds}")
    else:
        label = class_names[idx]

    # ✅ Logging
    log_line = f"{os.path.abspath(img_path)},{label},{confidence:.4f},{datetime.now()},{model_version}\n"
    os.makedirs("logs", exist_ok=True)
    with open("logs/prediction_logs.csv", "a") as f:
        f.write(log_line)

    return label, confidence, preds
