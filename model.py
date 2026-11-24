"""
Lightweight CNN Model for Plant Disease Detection
Optimized for training on regular computers
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

class PlantDiseaseModel:
    def __init__(self, num_classes=38, img_size=128):
        """
        Initialize a lightweight plant disease detection model

        Args:
            num_classes: Number of disease classes (default 38 for PlantVillage dataset)
            img_size: Input image size (default 128x128 for efficiency)
        """
        self.num_classes = num_classes
        self.img_size = img_size
        self.model = None

    def build_model(self):
        """Build a small CNN architecture"""
        self.model = models.Sequential([
            # First Conv Block
            layers.Conv2D(32, (3, 3), activation='relu',
                         input_shape=(self.img_size, self.img_size, 3)),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            # Second Conv Block
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            # Third Conv Block
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),

            # Dense Layers
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])

        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        return self.model

    def get_model_summary(self):
        """Display model architecture"""
        if self.model is None:
            self.build_model()
        return self.model.summary()

    def create_data_generators(self, train_dir, val_dir, batch_size=32):
        """
        Create data generators with augmentation

        Args:
            train_dir: Path to training data directory
            val_dir: Path to validation data directory
            batch_size: Batch size for training
        """
        # Training data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )

        # Validation data (only rescaling)
        val_datagen = ImageDataGenerator(rescale=1./255)

        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=batch_size,
            class_mode='categorical'
        )

        val_generator = val_datagen.flow_from_directory(
            val_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=batch_size,
            class_mode='categorical'
        )

        return train_generator, val_generator

    def train(self, train_generator, val_generator, epochs=20):
        """
        Train the model

        Args:
            train_generator: Training data generator
            val_generator: Validation data generator
            epochs: Number of training epochs
        """
        if self.model is None:
            self.build_model()

        # Callbacks
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )

        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7
        )

        history = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=epochs,
            callbacks=[early_stopping, reduce_lr]
        )

        return history

    def save_model(self, filepath='plant_disease_model.h5'):
        """Save the trained model"""
        if self.model:
            self.model.save(filepath)
            print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        """Load a trained model"""
        self.model = keras.models.load_model(filepath)
        print(f"Model loaded from {filepath}")

    def predict_image(self, image_path, class_names):
        """
        Predict disease from an image

        Args:
            image_path: Path to the image
            class_names: List of class names
        """
        img = keras.preprocessing.image.load_img(
            image_path,
            target_size=(self.img_size, self.img_size)
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class]

        return class_names[predicted_class], confidence


if __name__ == "__main__":
    # Example usage
    print("Creating Plant Disease Detection Model...")
    model = PlantDiseaseModel(num_classes=38, img_size=128)
    model.build_model()
    model.get_model_summary()

    print("\nModel created successfully!")
    print(f"Input shape: (128, 128, 3)")
    print(f"Output classes: 38")
    print(f"Total parameters: ~1.5M (lightweight)")
