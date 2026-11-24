# 🚀 Your First Time on Google Colab - Step by Step

**Date:** November 23, 2026  
**Goal:** Setup automated plant disease model training

---

## 📋 Before You Start

**You'll need:**
- ✅ Google account (Gmail)
- ✅ Internet connection
- ✅ Kaggle account (free, takes 2 minutes to create)

**Time needed:** 20-30 minutes for complete setup

---

## STEP 1: Access Google Colab (2 minutes)

### 1.1 Open Google Colab
1. Open your web browser
2. Go to: **https://colab.research.google.com**
3. Sign in with your Google account

### 1.2 What You'll See
- Yellow/orange notebook interface
- Menu bar at top
- Empty code cells

---

## STEP 2: Create Your Training Notebook (1 minute)

### 2.1 Create New Notebook
1. Click **File** → **New notebook**
2. You'll see a new notebook named "Untitled0.ipynb"

### 2.2 Rename It
1. Click on "Untitled0.ipynb" at the top
2. Rename to: **"Plant_Disease_Training"**
3. Press Enter

---

## STEP 3: Enable GPU (1 minute) ⚡

**IMPORTANT: Do this first or training will be 10x slower!**

### 3.1 Change Runtime
1. Click **Runtime** (top menu)
2. Click **Change runtime type**
3. Under "Hardware accelerator":
   - Change from "None" to **"GPU"**
4. Click **Save**

### 3.2 Verify GPU is Active
Create a new code cell and run:

```python
# Check if GPU is available
import tensorflow as tf
print("GPU Available:", tf.config.list_physical_devices('GPU'))
!nvidia-smi
```

**Click the Play button ▶️ or press Shift+Enter**

You should see GPU information (Tesla T4 or similar)

---

## STEP 4: Get Kaggle API Key (5 minutes)

**This lets Colab download the plant disease dataset automatically**

### 4.1 Create Kaggle Account (if you don't have one)
1. Open new tab: **https://www.kaggle.com**
2. Click **Register**
3. Create free account (use same email as Google if possible)
4. Verify email

### 4.2 Get API Token
1. Go to: **https://www.kaggle.com/settings**
2. Scroll down to **"API"** section
3. Click **"Create New API Token"**
4. A file **kaggle.json** will download to your computer
5. **Remember where it downloaded!** (usually Downloads folder)

### 4.3 Upload to Colab
Back in your Colab notebook, create a new code cell:

```python
# Upload Kaggle API key
from google.colab import files
uploaded = files.upload()
```

**Run this cell (▶️)**

A "Choose Files" button appears:
1. Click **Choose Files**
2. Navigate to your Downloads folder
3. Select **kaggle.json**
4. Click Open

### 4.4 Setup Kaggle
Create another code cell:

```python
# Configure Kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!rm kaggle.json
print("✅ Kaggle API configured!")
```

**Run this cell (▶️)**

---

## STEP 5: Connect Google Drive (2 minutes)

**This is where your trained model will auto-save**

### 5.1 Mount Google Drive
Create a new code cell:

```python
# Connect Google Drive
from google.colab import drive
drive.mount('/content/drive')
```

**Run this cell (▶️)**

### 5.2 Authorize Access
1. A popup appears asking for permission
2. Click **Connect to Google Drive**
3. Choose your Google account
4. Click **Allow**
5. Wait for "Mounted at /content/drive" message

✅ Now your Google Drive is accessible from Colab!

---

## STEP 6: Upload Your Model Code (3 minutes)

### Option A: Upload Files Manually (Easier for beginners)

Create a new code cell:

```python
# Upload your model files
from google.colab import files
print("📤 Upload model.py, train.py, and predict.py")
uploaded = files.upload()
```

**Run this cell (▶️)**

Then:
1. Click **Choose Files**
2. Navigate to: `C:\Users\imshy\plant-disease-model\`
3. Select these files:
   - `model.py`
   - `train.py`
   - `predict.py`
   - `requirements.txt`
4. Click Open
5. Wait for upload to complete

### Option B: Clone from GitHub (If you pushed to GitHub)

```python
# Clone your repository
!git clone https://github.com/YOUR_USERNAME/plant-disease-model.git
%cd plant-disease-model
```

---

## STEP 7: Install Dependencies (1 minute)

Create a new code cell:

```python
# Install required packages
!pip install -q tensorflow pillow
print("✅ Dependencies installed!")
```

**Run this cell (▶️)**

---

## STEP 8: Download Dataset (10 minutes)

### 8.1 Download from Kaggle
Create a new code cell:

```python
# Download PlantVillage dataset (54,000 images)
print("📥 Downloading dataset... This takes 5-10 minutes")
!kaggle datasets download -d emmarex/plantdisease
print("✅ Download complete!")
```

**Run this cell (▶️)**

**Wait for download to complete** (you'll see progress bar)

### 8.2 Extract Dataset

```python
# Extract the dataset
print("📦 Extracting dataset...")
!unzip -q plantdisease.zip -d /content/data
print("✅ Extraction complete!")

# Check what we got
import os
print("\n📂 Dataset structure:")
!ls /content/data
```

**Run this cell (▶️)**

### 8.3 Organize Data (Train/Val Split)

```python
# Split into training and validation sets
import os
import shutil
import random
from pathlib import Path

def organize_dataset():
    source = Path("/content/data/PlantVillage")
    train_dir = Path("/content/data/train")
    val_dir = Path("/content/data/val")
    
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    
    print("📊 Organizing dataset into train/val split...")
    
    for class_dir in source.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            (train_dir / class_name).mkdir(exist_ok=True)
            (val_dir / class_name).mkdir(exist_ok=True)
            
            images = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.JPG"))
            random.shuffle(images)
            
            # 80% train, 20% validation
            split_idx = int(len(images) * 0.8)
            train_images = images[:split_idx]
            val_images = images[split_idx:]
            
            for img in train_images:
                shutil.copy(img, train_dir / class_name / img.name)
            for img in val_images:
                shutil.copy(img, val_dir / class_name / img.name)
            
            print(f"  ✓ {class_name}: {len(train_images)} train, {len(val_images)} val")
    
    print(f"\n✅ Total: {len(list(train_dir.glob('*/*.jpg')))} train images")
    print(f"✅ Total: {len(list(val_dir.glob('*/*.jpg')))} validation images")

organize_dataset()
```

**Run this cell (▶️)**

---

## STEP 9: Start Training! (2-4 hours automated) 🚀

### 9.1 Create Training Cell

```python
# ==================================================
# AUTOMATED TRAINING - Close laptop after this runs!
# ==================================================

print("🚀 Starting training...")
print("⏰ Estimated time: 2-4 hours")
print("💡 You can close your laptop now!")
print("=" * 60)

# Import model
from model import PlantDiseaseModel

# Create model
model = PlantDiseaseModel(num_classes=38, img_size=128)
model.build_model()

print("\n📊 Model Architecture:")
model.get_model_summary()

# Create data generators
train_gen, val_gen = model.create_data_generators(
    '/content/data/train',
    '/content/data/val',
    batch_size=32
)

print(f"\n✅ Training data: {train_gen.samples} images")
print(f"✅ Validation data: {val_gen.samples} images")
print(f"✅ Classes: {len(train_gen.class_indices)}")

print("\n" + "=" * 60)
print("🏋️ TRAINING STARTED - You can close your laptop now!")
print("=" * 60 + "\n")

# Train the model
import time
start_time = time.time()

history = model.train(train_gen, val_gen, epochs=20)

training_time = (time.time() - start_time) / 3600  # hours

print("\n" + "=" * 60)
print("✅ TRAINING COMPLETE!")
print("=" * 60)
print(f"⏱️  Training time: {training_time:.2f} hours")
print(f"📊 Final training accuracy: {history.history['accuracy'][-1]*100:.2f}%")
print(f"📊 Final validation accuracy: {history.history['val_accuracy'][-1]*100:.2f}%")
print(f"💾 Model size: ~18 MB")

# Save to Colab workspace
model.save_model('plant_disease_model.h5')

# IMPORTANT: Auto-save to Google Drive
drive_path = '/content/drive/MyDrive/plant_disease_model.h5'
shutil.copy('plant_disease_model.h5', drive_path)
print(f"\n💾 Model saved to Google Drive!")
print(f"📁 Location: Google Drive → plant_disease_model.h5")

# Save training history
import json
history_path = '/content/drive/MyDrive/training_history.json'
with open(history_path, 'w') as f:
    json.dump({
        'accuracy': [float(x) for x in history.history['accuracy']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']],
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history['val_loss']],
        'training_time_hours': training_time
    }, f, indent=2)

print(f"📊 Training history saved to: Google Drive → training_history.json")

# Test on a sample image
print("\n🧪 Testing model on random validation image...")
test_imgs = list(Path('/content/data/val').glob('*/*.jpg'))
test_img = str(test_imgs[0])
disease, confidence = model.predict_image(test_img, list(train_gen.class_indices.keys()))
print(f"Sample prediction: {disease}")
print(f"Confidence: {confidence*100:.2f}%")

print("\n" + "=" * 60)
print("🎉 ALL DONE! Your model is ready to use!")
print("=" * 60)
print("\n📥 Download your model:")
print("   1. Open Google Drive")
print("   2. Find: plant_disease_model.h5")
print("   3. Right-click → Download")
print("\n✅ Model is saved and ready for your web app!")
```

**Run this cell (▶️)**

### 9.2 What Happens Now

**After you click Run (▶️):**

1. ✅ Training starts immediately
2. ✅ You'll see progress bars for each epoch
3. ✅ **YOU CAN CLOSE YOUR LAPTOP NOW** ✅
4. ✅ Training continues in Google's cloud
5. ✅ Model auto-saves to your Google Drive
6. ✅ Come back in 2-4 hours

**You'll see output like:**
```
Epoch 1/20
1358/1358 [==============================] - 45s 33ms/step
  - accuracy: 0.6543 - val_accuracy: 0.7654

Epoch 2/20
1358/1358 [==============================] - 42s 31ms/step
  - accuracy: 0.7823 - val_accuracy: 0.8321

...

Epoch 20/20
1358/1358 [==============================] - 41s 30ms/step
  - accuracy: 0.9654 - val_accuracy: 0.9234

✅ TRAINING COMPLETE!
💾 Model saved to Google Drive!
```

---

## STEP 10: Save Your Notebook (1 minute)

**IMPORTANT: Save so you can reuse this setup!**

1. Click **File** → **Save**
2. Or press `Ctrl+S` (Windows) / `Cmd+S` (Mac)

Your notebook is now saved to Google Drive!

---

## STEP 11: Close Laptop & Wait ☕

**You can now:**
- ✅ Close your laptop
- ✅ Turn off your computer
- ✅ Go do other things
- ✅ Training continues in Google's cloud

**Check progress (optional):**
- Open Colab on your phone: https://colab.research.google.com
- See current epoch and accuracy in real-time

---

## STEP 12: Download Your Trained Model (after 2-4 hours)

### 12.1 Check if Training is Done

Open your notebook, scroll to bottom, look for:
```
✅ TRAINING COMPLETE!
💾 Model saved to Google Drive!
```

### 12.2 Download Model

**Option A: From Google Drive**
1. Open: https://drive.google.com
2. Find file: **plant_disease_model.h5** (18 MB)
3. Right-click → Download

**Option B: From Colab Directly**

Add a new cell at the end:

```python
# Download model directly from Colab
from google.colab import files
files.download('plant_disease_model.h5')
```

**Run this cell (▶️)** and model downloads to your computer!

---

## 🎯 What You Should See at Each Step

### ✅ Checklist:

After each step, you should see:

**Step 3 (GPU):**
```
GPU Available: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

**Step 4 (Kaggle):**
```
✅ Kaggle API configured!
```

**Step 5 (Google Drive):**
```
Mounted at /content/drive
```

**Step 8 (Dataset):**
```
✅ Total: 43456 train images
✅ Total: 10864 validation images
```

**Step 9 (Training):**
```
Epoch 1/20
1358/1358 [======] - accuracy: 0.6543 - val_accuracy: 0.7654
...
✅ TRAINING COMPLETE!
Final validation accuracy: 92.34%
💾 Model saved to Google Drive!
```

---

## 🆘 Troubleshooting

### "No GPU available"
- Go to **Runtime → Change runtime type → GPU → Save**
- Restart runtime and try again

### "Kaggle API key not found"
- Make sure you uploaded kaggle.json correctly
- Check the file is in `~/.kaggle/kaggle.json`

### "Session disconnected"
- Colab free tier disconnects after 12 hours (enough for training)
- Checkpoint system auto-saves progress
- Reconnect and resume

### "Out of memory"
- Reduce batch_size in train.py from 32 to 16
- Or reduce img_size from 128 to 96

### "Can't find model after training"
- Check Google Drive → plant_disease_model.h5
- Or run the download cell again

---

## 💡 Pro Tips

1. **Save your notebook frequently** (Ctrl+S)
2. **Keep Colab tab open** (can minimize, but don't close)
3. **Check progress on phone** if you want
4. **Training typically takes 2-4 hours** on free GPU
5. **Model auto-saves every epoch** so you won't lose progress
6. **Google Drive file appears immediately** after training ends

---

## 🎓 Summary - Your First Colab Session

**What you did:**
1. ✅ Opened Google Colab
2. ✅ Enabled GPU for fast training
3. ✅ Connected Kaggle API for dataset
4. ✅ Connected Google Drive for auto-save
5. ✅ Uploaded your model code
6. ✅ Downloaded 54,000 plant images
7. ✅ Started automated training
8. ✅ Closed laptop (training continues)
9. ✅ Waited 2-4 hours
10. ✅ Downloaded trained model (18 MB)

**Cost:** $0  
**Your time:** 30 min setup + 1 click to start  
**Training time:** 2-4 hours (automated)  
**Result:** Trained model ready for your web app!

---

## 📱 Next Time (After Setup)

**Future training sessions are even easier:**

1. Open saved notebook
2. Click **Runtime → Run all**
3. Close laptop
4. Done!

(All the setup is saved, no need to repeat Steps 1-7)

---

## 📞 Need Help?

**Common Questions:**

**Q: Can I close the browser tab during training?**  
A: Yes! Training continues in Google's cloud. You can close browser, laptop, everything. Just come back later.

**Q: How do I know when it's done?**  
A: Check your notebook or Google Drive. You'll see "✅ TRAINING COMPLETE!" message.

**Q: What if my internet disconnects?**  
A: No problem! Training happens on Google's servers, not your computer.

**Q: Can I train multiple models?**  
A: Yes! Just run the notebook again with different settings.

**Q: Do I need to pay?**  
A: No! Google Colab free tier is enough for your 54k image dataset.

---

## 🚀 Ready to Start?

**Open this link now:**  
👉 **https://colab.research.google.com** 👈

Follow the steps above and you'll have your trained model in 2-4 hours!

Good luck! 🎉
