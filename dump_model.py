# dump_model.py
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load your saved model
model = load_model("model/skin_cancer_model.keras")

# Print a summary of its layers
model.summary()
