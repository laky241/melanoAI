# load_model_test.py
from tensorflow.keras.models import load_model

model_path = "model/skin_cancer_model.h5"  # ✅ FIXED PATH
model = load_model(model_path)

print("✅ Model loaded successfully!")
print("📐 Input shape:", model.input_shape)
print("📤 Output shape:", model.output_shape)
