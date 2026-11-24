"""
Script to download PlantVillage dataset from Kaggle
Requires Kaggle API credentials
"""

import os
import zipfile
import shutil

def setup_dataset():
    """Download and organize PlantVillage dataset"""

    print("=" * 60)
    print("PlantVillage Dataset Setup")
    print("=" * 60)

    # Check if kaggle is installed
    try:
        import kaggle
        print("✅ Kaggle API found")
    except ImportError:
        print("\n❌ Kaggle API not installed")
        print("\nInstall it with:")
        print("   pip install kaggle")
        print("\nThen setup your API credentials:")
        print("   1. Go to https://www.kaggle.com/settings")
        print("   2. Create API token (downloads kaggle.json)")
        print("   3. Place it in ~/.kaggle/kaggle.json")
        return

    # Download dataset
    print("\n📥 Downloading PlantVillage dataset...")
    print("   This may take a few minutes...")

    try:
        os.system("kaggle datasets download -d emmarex/plantdisease")

        if os.path.exists("plantdisease.zip"):
            print("✅ Download complete!")

            # Extract
            print("\n📦 Extracting files...")
            with zipfile.ZipFile("plantdisease.zip", 'r') as zip_ref:
                zip_ref.extractall("temp_data")

            print("✅ Extraction complete!")

            # Organize into train/val split
            print("\n📁 Organizing data...")
            organize_data()

            # Cleanup
            os.remove("plantdisease.zip")
            shutil.rmtree("temp_data")

            print("\n✅ Dataset ready!")
            print("   Location: data/train and data/val")

        else:
            print("❌ Download failed")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nManual download:")
        print("   1. Go to: https://www.kaggle.com/datasets/emmarex/plantdisease")
        print("   2. Download the dataset")
        print("   3. Extract to 'data' folder")

def organize_data():
    """Split dataset into train/val"""
    from pathlib import Path
    import random

    source = Path("temp_data/PlantVillage")
    train_dir = Path("data/train")
    val_dir = Path("data/val")

    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)

    # 80-20 split
    for class_dir in source.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name

            # Create class directories
            (train_dir / class_name).mkdir(exist_ok=True)
            (val_dir / class_name).mkdir(exist_ok=True)

            # Get all images
            images = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.JPG"))
            random.shuffle(images)

            # Split
            split_idx = int(len(images) * 0.8)
            train_images = images[:split_idx]
            val_images = images[split_idx:]

            # Copy files
            for img in train_images:
                shutil.copy(img, train_dir / class_name / img.name)

            for img in val_images:
                shutil.copy(img, val_dir / class_name / img.name)

            print(f"   {class_name}: {len(train_images)} train, {len(val_images)} val")

if __name__ == "__main__":
    setup_dataset()
