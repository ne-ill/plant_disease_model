"""
Training Script for Plant Disease Detection Model
Run this script to train your model on plant disease data
"""

from model import PlantDiseaseModel
import os

def main():
    print("=" * 60)
    print("Plant Disease Detection - Training Script")
    print("=" * 60)

    # Configuration
    NUM_CLASSES = 38  # Adjust based on your dataset
    IMG_SIZE = 128    # Small size for faster training
    BATCH_SIZE = 32
    EPOCHS = 20

    # Paths (adjust these to your dataset location)
    TRAIN_DIR = 'data/train'
    VAL_DIR = 'data/val'

    # Check if data directories exist
    if not os.path.exists(TRAIN_DIR):
        print(f"\n❌ Training directory not found: {TRAIN_DIR}")
        print("\nPlease organize your data as follows:")
        print("data/")
        print("├── train/")
        print("│   ├── Tomato_Early_Blight/")
        print("│   ├── Tomato_Late_Blight/")
        print("│   ├── Tomato_Healthy/")
        print("│   └── ... (other disease classes)")
        print("└── val/")
        print("    ├── Tomato_Early_Blight/")
        print("    └── ... (same structure)")
        return

    # Initialize model
    print(f"\n📦 Creating model...")
    print(f"   Image size: {IMG_SIZE}x{IMG_SIZE}")
    print(f"   Classes: {NUM_CLASSES}")

    model = PlantDiseaseModel(num_classes=NUM_CLASSES, img_size=IMG_SIZE)
    model.build_model()

    # Show model architecture
    print("\n🏗️  Model Architecture:")
    model.get_model_summary()

    # Create data generators
    print(f"\n📊 Loading data from:")
    print(f"   Train: {TRAIN_DIR}")
    print(f"   Val: {VAL_DIR}")

    train_gen, val_gen = model.create_data_generators(
        TRAIN_DIR,
        VAL_DIR,
        batch_size=BATCH_SIZE
    )

    print(f"\n✅ Found {train_gen.samples} training images")
    print(f"✅ Found {val_gen.samples} validation images")
    print(f"✅ Detected {len(train_gen.class_indices)} classes")

    # Train the model
    print(f"\n🚀 Starting training for {EPOCHS} epochs...")
    print("   This may take a while depending on your hardware")
    print("   Press Ctrl+C to stop training\n")

    try:
        history = model.train(train_gen, val_gen, epochs=EPOCHS)

        print("\n✅ Training completed!")
        print(f"   Final accuracy: {history.history['accuracy'][-1]:.4f}")
        print(f"   Final val_accuracy: {history.history['val_accuracy'][-1]:.4f}")

        # Save the model
        model.save_model('plant_disease_model.h5')
        print("\n💾 Model saved as 'plant_disease_model.h5'")

    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        save = input("Save current model? (y/n): ")
        if save.lower() == 'y':
            model.save_model('plant_disease_model_interrupted.h5')
            print("💾 Model saved as 'plant_disease_model_interrupted.h5'")

if __name__ == "__main__":
    main()
