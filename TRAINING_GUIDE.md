# 🎓 How to Train Your Plant Disease Model

## Step-by-Step Training Guide

### STEP 1: Install Python & Dependencies

First, make sure you have Python installed (3.8 or higher).

```bash
# Navigate to the project folder
cd plant-disease-model

# Install required packages
pip install -r requirements.txt
```

**What this installs:**
- TensorFlow (the AI framework)
- NumPy (for calculations)
- Pillow (for image processing)

---

### STEP 2: Get Training Data

You need images of diseased and healthy plants. Two options:

#### Option A: Download PlantVillage Dataset (Recommended)

**PlantVillage is FREE and has 54,000+ images of 38 plant diseases**

**Method 1 - Automatic (easiest):**
```bash
# Install Kaggle
pip install kaggle

# Setup Kaggle API:
# 1. Go to https://www.kaggle.com/settings
# 2. Click "Create New API Token" (downloads kaggle.json)
# 3. Place kaggle.json in:
#    Windows: C:\Users\YourName\.kaggle\kaggle.json
#    Mac/Linux: ~/.kaggle/kaggle.json

# Run the download script
python download_dataset.py
```

**Method 2 - Manual:**
1. Go to https://www.kaggle.com/datasets/emmarex/plantdisease
2. Click "Download" (you'll need a free Kaggle account)
3. Extract the ZIP file
4. Organize files like this:

```
plant-disease-model/
└── data/
    ├── train/
    │   ├── Tomato___Early_blight/
    │   │   ├── image1.jpg
    │   │   ├── image2.jpg
    │   │   └── ...
    │   ├── Tomato___Late_blight/
    │   ├── Tomato___healthy/
    │   └── ... (38 folders total)
    └── val/
        ├── Tomato___Early_blight/
        ├── Tomato___Late_blight/
        └── ... (same 38 folders)
```

**Split rule**: 80% images in `train/`, 20% in `val/`

#### Option B: Use Your Own Images

Collect your own plant photos:
- **At least 100 images per disease type**
- Good lighting, clear leaf photos
- Create folders for each disease

```
data/
├── train/
│   ├── tomato_blight/
│   ├── tomato_healthy/
│   ├── potato_disease/
│   └── ...
└── val/
    └── (same folders, 20% of images)
```

---

### STEP 3: Configure Training Settings

Open `train.py` and adjust these if needed:

```python
# In train.py, you can change:

NUM_CLASSES = 38      # Change to match your number of disease types
IMG_SIZE = 128        # Keep at 128 for speed, or use 224 for better accuracy
BATCH_SIZE = 32       # Lower to 16 if you get "out of memory" errors
EPOCHS = 20           # More epochs = better training (try 30-50)

TRAIN_DIR = 'data/train'  # Path to your training images
VAL_DIR = 'data/val'      # Path to your validation images
```

---

### STEP 4: Start Training!

```bash
python train.py
```

**What you'll see:**
```
==============================================================
Plant Disease Detection - Training Script
==============================================================

📦 Creating model...
   Image size: 128x128
   Classes: 38

🏗️  Model Architecture:
Model: "sequential"
_________________________________________________________________
...

📊 Loading data from:
   Train: data/train
   Val: data/val

✅ Found 43456 training images
✅ Found 10864 validation images
✅ Detected 38 classes

🚀 Starting training for 20 epochs...

Epoch 1/20
1358/1358 [==============================] - 45s 33ms/step
  - loss: 1.2345 - accuracy: 0.6543 - val_loss: 0.8765 - val_accuracy: 0.7654

Epoch 2/20
...
```

**Training will take:**
- **CPU only**: 20-40 minutes
- **With GPU**: 5-15 minutes

**Tip**: Leave it running and go grab coffee! ☕

---

### STEP 5: Training Complete!

When finished, you'll see:

```
✅ Training completed!
   Final accuracy: 0.9654
   Final val_accuracy: 0.9234

💾 Model saved as 'plant_disease_model.h5'
```

Your trained model is now saved as `plant_disease_model.h5` (about 18MB)

---

### STEP 6: Test Your Model

```bash
# Test on a single image
python predict.py path/to/leaf_image.jpg
```

**Example output:**
```
🔍 Loading model...
📸 Analyzing image: tomato_leaf.jpg

============================================================
PREDICTION RESULTS
============================================================
Disease: Tomato___Early_blight
Confidence: 94.32%
============================================================

🌱 Plant: Tomato
🦠 Condition: Early blight
⚠️  Disease detected - consider appropriate treatment
```

---

## 🎯 Training Tips

### If accuracy is low (<80%):
- ✅ Train for more epochs (30-50 instead of 20)
- ✅ Use larger images (224 instead of 128)
- ✅ Add more training data
- ✅ Make sure images are clear and well-lit

### If you get "Out of Memory" error:
- ✅ Reduce `BATCH_SIZE` from 32 to 16 or 8
- ✅ Reduce `IMG_SIZE` from 128 to 96
- ✅ Close other programs

### If training is too slow:
- ✅ Use smaller `IMG_SIZE` (96 instead of 128)
- ✅ Reduce dataset size (use fewer images)
- ✅ Consider using Google Colab (free GPU)

---

## 🚀 Use Your Trained Model in a Web App

Once trained, integrate into Flask/FastAPI:

```python
from model import PlantDiseaseModel

# Load once when app starts
model = PlantDiseaseModel()
model.load_model('plant_disease_model.h5')

# When user uploads image
@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    disease, confidence = model.predict_image(file, CLASS_NAMES)
    return {'disease': disease, 'confidence': float(confidence)}
```

---

## 📊 Expected Results

With PlantVillage dataset:
- **Training Accuracy**: 95-98%
- **Validation Accuracy**: 90-95%
- **Prediction Time**: ~50ms per image

---

## ❓ Troubleshooting

**Q: Where do I run these commands?**
A: In your terminal/command prompt, inside the `plant-disease-model` folder

**Q: Do I need a GPU?**
A: No! Works on CPU, just slower. GPU recommended if training on 50k+ images

**Q: Can I stop training and resume later?**
A: The model automatically saves the best version. You can stop with Ctrl+C

**Q: How do I know if it's working?**
A: Watch the `val_accuracy` - if it's increasing, it's learning!

---

## 🎓 Next Steps

1. ✅ Train the basic model first
2. ✅ Test it on a few images
3. ✅ If accuracy is good, integrate into your web app
4. ✅ If accuracy is low, retrain with more data/epochs

**Need help?** Check the logs and error messages - they usually tell you what's wrong!
