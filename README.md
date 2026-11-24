# Plant Disease Detection Model

A lightweight CNN model for detecting plant diseases from leaf images. Optimized for training on regular computers.

## 📋 Features

- **Small & Fast**: Only ~1.5M parameters, trains quickly on CPU/GPU
- **128x128 input size**: Efficient without sacrificing accuracy
- **38 disease classes**: Supports PlantVillage dataset
- **Data augmentation**: Built-in image augmentation for better generalization
- **Easy to use**: Simple training and prediction scripts

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install tensorflow numpy pillow
```

### 2. Prepare Your Data

Organize your dataset in this structure:

```
data/
├── train/
│   ├── Tomato_Early_Blight/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── Tomato_Late_Blight/
│   ├── Tomato_Healthy/
│   └── ... (other disease classes)
└── val/
    ├── Tomato_Early_Blight/
    ├── Tomato_Late_Blight/
    └── ... (same structure)
```

**Where to get data:**
- [PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease) (Kaggle)
- [PlantDoc Dataset](https://github.com/pratikkayal/PlantDoc-Dataset)

### 3. Train the Model

```bash
python train.py
```

Training will take 10-30 minutes depending on your hardware and dataset size.

### 4. Test on New Images

```bash
python predict.py path/to/your/image.jpg
```

## 📊 Model Architecture

```
Input (128x128x3)
    ↓
Conv2D(32) + BatchNorm + MaxPool + Dropout
    ↓
Conv2D(64) + BatchNorm + MaxPool + Dropout
    ↓
Conv2D(128) + BatchNorm + MaxPool + Dropout
    ↓
Dense(256) + BatchNorm + Dropout
    ↓
Output (38 classes, softmax)
```

**Total Parameters**: ~1,500,000
**Model Size**: ~18MB

## 🎯 Supported Disease Classes

The model detects 38 different conditions across multiple plants:

- **Apple**: Scab, Black rot, Cedar rust, Healthy
- **Corn**: Cercospora spot, Common rust, Leaf blight, Healthy
- **Grape**: Black rot, Esca, Leaf blight, Healthy
- **Tomato**: 10 different diseases + Healthy
- **Potato**: Early blight, Late blight, Healthy
- And more...

## 🔧 Customization

### Change Image Size

```python
model = PlantDiseaseModel(num_classes=38, img_size=224)  # Larger for better accuracy
```

### Adjust Training Parameters

Edit `train.py`:

```python
BATCH_SIZE = 16  # Reduce if running out of memory
EPOCHS = 30      # More epochs for better training
```

### Use Your Own Classes

If you have different disease classes:

1. Update `NUM_CLASSES` in `train.py`
2. Update `CLASS_NAMES` list in `predict.py`

## 📈 Expected Performance

With proper training on PlantVillage dataset:
- **Training Accuracy**: 95-98%
- **Validation Accuracy**: 90-95%
- **Inference Time**: ~50ms per image (CPU)

## 💡 Tips for Better Results

1. **More data = better results**: Aim for 100+ images per class
2. **Balanced dataset**: Equal images for each disease class
3. **Good quality images**: Clear, well-lit leaf photos
4. **Data augmentation**: Already built-in, helps with small datasets
5. **Train longer**: Increase epochs if validation accuracy keeps improving

## 🌐 Web Integration

To integrate with a web app:

```python
from model import PlantDiseaseModel

# Load model once
model = PlantDiseaseModel()
model.load_model('plant_disease_model.h5')

# Predict from uploaded image
disease, confidence = model.predict_image(uploaded_file, CLASS_NAMES)
```

## 📝 Files

- `model.py` - Core model architecture and training logic
- `train.py` - Training script
- `predict.py` - Prediction/testing script
- `requirements.txt` - Python dependencies

## 🤝 Need Help?

Common issues:

**Out of memory**: Reduce `BATCH_SIZE` in train.py
**Low accuracy**: Train longer, add more data, or increase `img_size`
**Slow training**: Use GPU, reduce image size, or reduce dataset size

## 📄 License

Free to use for educational and commercial projects.
