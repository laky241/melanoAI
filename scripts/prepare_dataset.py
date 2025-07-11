import pandas as pd
import os
import shutil

# Paths
metadata_path = 'data/raw/HAM10000_metadata.csv'
image_dir1 = 'data/raw/HAM10000_images_part_1'
image_dir2 = 'data/raw/HAM10000_images_part_2'
output_dir = 'data/HAM10000'

# Create folders
os.makedirs(os.path.join(output_dir, 'benign'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'malignant'), exist_ok=True)

# Load metadata
df = pd.read_csv(metadata_path)

# Define benign vs malignant mapping
benign_labels = ['nv', 'bkl', 'df', 'vasc']
malignant_labels = ['mel', 'bcc', 'akiec']

# Process each row
for idx, row in df.iterrows():
    img_name = row['image_id'] + '.jpg'
    label = row['dx']
    src_path = os.path.join(image_dir1, img_name)
    if not os.path.exists(src_path):
        src_path = os.path.join(image_dir2, img_name)
    if not os.path.exists(src_path):
        print(f"❌ Image not found: {img_name}")
        continue

    if label in benign_labels:
        dest_folder = 'benign'
    elif label in malignant_labels:
        dest_folder = 'malignant'
    else:
        print(f"⚠️ Unknown label: {label}")
        continue

    dest_path = os.path.join(output_dir, dest_folder, img_name)
    shutil.copy(src_path, dest_path)

print("✅ Dataset organized successfully!")
