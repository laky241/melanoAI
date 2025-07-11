import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.preprocessing import preprocess_image


from utils.preprocessing import preprocess_image

img = preprocess_image("data/test_image.jpg")
print("Preprocessed image shape:", img.shape)
