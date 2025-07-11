import os
import shutil
import random

def split_dataset(source_dir, train_dir, val_dir, split_ratio=0.8):
    classes = os.listdir(source_dir)
    for cls in classes:
        src_cls = os.path.join(source_dir, cls)
        train_cls = os.path.join(train_dir, cls)
        val_cls = os.path.join(val_dir, cls)

        os.makedirs(train_cls, exist_ok=True)
        os.makedirs(val_cls, exist_ok=True)

        files = [f for f in os.listdir(src_cls) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
        random.shuffle(files)

        split_idx = int(len(files) * split_ratio)
        train_files = files[:split_idx]
        val_files = files[split_idx:]

        for f in train_files:
            shutil.copy(os.path.join(src_cls, f), os.path.join(train_cls, f))
        for f in val_files:
            shutil.copy(os.path.join(src_cls, f), os.path.join(val_cls, f))

    print("✅ Dataset split into train/val successfully.")

# Run it
if __name__ == "__main__":
    original_data_dir = "data/train"
    train_dir = "data/train_split"
    val_dir = "data/val"

    split_dataset(original_data_dir, train_dir, val_dir)
