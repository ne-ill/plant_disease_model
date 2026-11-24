# 🤖 Automated Cloud Training Setup

## ✅ YES! You Can Train While Your Laptop is Closed

Cloud training runs on **remote servers**, not your laptop. Once you start training, you can:
- ✅ Close your laptop
- ✅ Turn off your computer
- ✅ Go to sleep
- ✅ Come back later to download the trained model

---

## 🎯 Best Automation Options

### **Option 1: Google Colab with Automation Script (RECOMMENDED)**

**Setup once, runs automatically every time**

#### Step 1: Create Automated Colab Notebook

```python
# ==================================================
# AUTOMATED PLANT DISEASE TRAINING
# Setup once, run anytime, close laptop
# ==================================================

# 1. Enable GPU first!
# Runtime → Change runtime type → GPU → Save

# 2. Install dependencies
!pip install -q tensorflow pillow kaggle

# 3. Setup Kaggle API (one-time)
from google.colab import files
import os

# Upload kaggle.json (only first time)
# Get it from: https://www.kaggle.com/settings → Create API Token
if not os.path.exists('/root/.kaggle/kaggle.json'):
    print("📤 Upload your kaggle.json file:")
    uploaded = files.upload()
    !mkdir -p ~/.kaggle
    !mv kaggle.json ~/.kaggle/
    !chmod 600 ~/.kaggle/kaggle.json
    print("✅ Kaggle configured!")

# 4. Mount Google Drive (saves model automatically)
from google.colab import drive
drive.mount('/content/drive')

# 5. Download model code from GitHub (or upload once)
!git clone https://github.com/YOUR_USERNAME/plant-disease-model.git
# OR upload your files manually first time

# 6. Download PlantVillage Dataset (54k images, free)
print("📥 Downloading dataset...")
!kaggle datasets download -d emmarex/plantdisease -p /content/data
!unzip -q /content/data/plantdisease.zip -d /content/data
print("✅ Dataset ready!")

# 7. Organize data (80/20 split)
import os
import shutil
import random
from pathlib import Path

def organize_dataset():
    """Split dataset into train/val automatically"""
    source = Path("/content/data/PlantVillage")
    train_dir = Path("/content/data/train")
    val_dir = Path("/content/data/val")
    
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    
    for class_dir in source.iterdir():
        if class_dir.is_dir():
            class_name = class_dir.name
            (train_dir / class_name).mkdir(exist_ok=True)
            (val_dir / class_name).mkdir(exist_ok=True)
            
            images = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.JPG"))
            random.shuffle(images)
            
            split_idx = int(len(images) * 0.8)
            train_images = images[:split_idx]
            val_images = images[split_idx:]
            
            for img in train_images:
                shutil.copy(img, train_dir / class_name / img.name)
            for img in val_images:
                shutil.copy(img, val_dir / class_name / img.name)
    
    print(f"✅ Organized: {len(list(train_dir.glob('*/*.jpg')))} train, {len(list(val_dir.glob('*/*.jpg')))} val")

organize_dataset()

# 8. Train the model (AUTOMATED - Close laptop now!)
print("🚀 Starting training... You can close your laptop now!")
print("⏰ Estimated time: 2-4 hours")
print("💾 Model will auto-save to Google Drive")

import sys
sys.path.append('/content/plant-disease-model')

from model import PlantDiseaseModel

# Configure
model = PlantDiseaseModel(num_classes=38, img_size=128)
model.build_model()

# Create generators
train_gen, val_gen = model.create_data_generators(
    '/content/data/train',
    '/content/data/val',
    batch_size=32
)

# Train
history = model.train(train_gen, val_gen, epochs=20)

# 9. Auto-save to Google Drive
model.save_model('/content/drive/MyDrive/plant_disease_model.h5')
print("✅ TRAINING COMPLETE!")
print("💾 Model saved to: Google Drive/plant_disease_model.h5")

# 10. Save training logs
import json
with open('/content/drive/MyDrive/training_history.json', 'w') as f:
    json.dump(history.history, f)

# 11. Test model
print("\n🧪 Testing model on sample image...")
test_img = list(Path('/content/data/val').glob('*/*.jpg'))[0]
disease, confidence = model.predict_image(str(test_img), train_gen.class_indices.keys())
print(f"Test prediction: {disease} ({confidence*100:.2f}% confidence)")

# 12. Send notification (optional - needs setup)
# from google.colab import auth
# Send email or Slack notification that training is done

print("\n" + "="*60)
print("✅ ALL DONE! Your model is ready.")
print("📥 Download from: Google Drive → plant_disease_model.h5")
print("="*60)
```

**Save this notebook as:** `automated_training.ipynb`

**To use it:**
1. Open https://colab.research.google.com
2. Upload this notebook (one-time)
3. Click "Runtime → Run all"
4. **Close your laptop** ✅
5. Come back in 2-4 hours
6. Download trained model from Google Drive

---

### **Option 2: Kaggle Notebooks (Fully Automated)**

**Even simpler - dataset is already there!**

#### Create Kaggle Notebook:

```python
# ==================================================
# KAGGLE AUTOMATED TRAINING
# Dataset built-in, runs in background
# ==================================================

# 1. Add PlantVillage dataset
# In Kaggle: Add Data → Search "plantdisease" → Add

# 2. Enable GPU
# Settings → Accelerator → GPU → Save

# 3. Training Script (paste this)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Dataset is at /kaggle/input/plantdisease/
print("📂 Available data:", os.listdir('/kaggle/input'))

# Your model code here (same as model.py)
class PlantDiseaseModel:
    # ... (paste your model code)
    pass

# Train
model = PlantDiseaseModel(num_classes=38, img_size=128)
model.build_model()

train_gen, val_gen = model.create_data_generators(
    '/kaggle/input/plantdisease/train',
    '/kaggle/input/plantdisease/val',
    batch_size=32
)

print("🚀 Training started! Close browser, come back later.")
history = model.train(train_gen, val_gen, epochs=20)

# Save model
model.save_model('/kaggle/working/plant_disease_model.h5')
print("✅ Done! Download model from Output → plant_disease_model.h5")
```

**To use:**
1. Go to https://www.kaggle.com
2. Create new notebook
3. Add PlantVillage dataset
4. Enable GPU
5. Paste code above
6. Click "Run All"
7. **Close browser** ✅
8. Check back later, download model from Output tab

---

### **Option 3: Automated Script with AWS/Cloud (Most Professional)**

**Setup:**

```python
# ==================================================
# FULLY AUTOMATED AWS TRAINING
# Runs scheduled, no manual intervention
# ==================================================

import boto3
import sagemaker
from sagemaker.tensorflow import TensorFlow

# Configure once
sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::YOUR_ACCOUNT:role/SageMakerRole"

# Point to your data on S3
training_data = "s3://your-bucket/plantvillage-data/"

# Define training job
estimator = TensorFlow(
    entry_point='train.py',
    role=role,
    instance_count=1,
    instance_type='ml.g4dn.xlarge',  # GPU instance
    framework_version='2.13',
    py_version='py310',
    hyperparameters={
        'epochs': 20,
        'batch-size': 32
    }
)

# Start training (runs in cloud, laptop not needed)
estimator.fit({'training': training_data})

# Model auto-saves to S3
print("✅ Training running on AWS. Close laptop now!")
```

**Cost:** ~$1-2 per training run

---

## 🔄 Complete Automation Workflow

### **Full "Set and Forget" Setup:**

```python
# ==================================================
# ULTIMATE AUTOMATION
# Give source ONCE, trains automatically forever
# ==================================================

from google.colab import drive
import schedule
import time

# 1. Mount Google Drive (one-time setup)
drive.mount('/content/drive')

# 2. Configuration file (edit once)
CONFIG = {
    'dataset_source': 'kaggle:emmarex/plantdisease',
    'save_location': '/content/drive/MyDrive/trained_models/',
    'num_classes': 38,
    'epochs': 20,
    'batch_size': 32,
    'img_size': 128,
    'notify_email': 'your-email@gmail.com'  # Optional
}

# 3. Training function
def automated_training():
    """Runs complete training pipeline"""
    
    print(f"🚀 Starting automated training at {time.ctime()}")
    
    # Download dataset
    if CONFIG['dataset_source'].startswith('kaggle:'):
        dataset_name = CONFIG['dataset_source'].replace('kaggle:', '')
        !kaggle datasets download -d {dataset_name}
        !unzip -q plantdisease.zip
    
    # Import model
    from model import PlantDiseaseModel
    
    # Train
    model = PlantDiseaseModel(
        num_classes=CONFIG['num_classes'],
        img_size=CONFIG['img_size']
    )
    model.build_model()
    
    train_gen, val_gen = model.create_data_generators(
        'data/train',
        'data/val',
        batch_size=CONFIG['batch_size']
    )
    
    history = model.train(train_gen, val_gen, epochs=CONFIG['epochs'])
    
    # Save with timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"{CONFIG['save_location']}/model_{timestamp}.h5"
    model.save_model(model_path)
    
    print(f"✅ Training complete! Model saved to: {model_path}")
    
    # Optional: Send notification
    # send_email_notification(CONFIG['notify_email'], model_path)

# 4. Run training
automated_training()

# 5. Optional: Schedule periodic retraining
# schedule.every().week.do(automated_training)
# 
# while True:
#     schedule.run_pending()
#     time.sleep(3600)  # Check every hour
```

**Save this as:** `automated_pipeline.py`

**Run once, forget forever!**

---

## 📱 Get Notified When Training is Done

### **Option A: Email Notification (Colab)**

```python
# Add at end of training script
def send_notification(to_email, subject, message):
    """Send email when training completes"""
    import smtplib
    from email.mime.text import MIMEText
    
    # Use Gmail (create app password first)
    sender = "your-email@gmail.com"
    password = "your-app-password"
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# After training completes
send_notification(
    "your-phone-email@carrier.com",  # Email-to-SMS gateway
    "Training Complete!",
    f"Your plant disease model is ready! Accuracy: {history.history['val_accuracy'][-1]*100:.2f}%"
)
```

### **Option B: Telegram Bot (Simple)**

```python
# Setup once
!pip install python-telegram-bot

import telegram

# Create bot at https://t.me/BotFather
bot = telegram.Bot(token='YOUR_BOT_TOKEN')
chat_id = 'YOUR_CHAT_ID'

# After training
bot.send_message(
    chat_id=chat_id,
    text=f"🎉 Training complete!\n📊 Accuracy: {val_acc:.2f}%\n⏱️ Time: {training_time}"
)
```

### **Option C: Webhook/IFTTT**

```python
import requests

# After training
requests.post(
    'https://maker.ifttt.com/trigger/training_done/with/key/YOUR_KEY',
    json={'value1': 'Model training complete!'}
)
```

---

## 📊 Monitoring While Away

### **Check Progress Without Opening Laptop:**

**1. Colab Mobile View:**
- Open https://colab.research.google.com on phone
- See real-time training progress
- Current epoch, accuracy, loss

**2. TensorBoard (Advanced):**
```python
# Add to training script
%load_ext tensorboard
%tensorboard --logdir logs

# Share public URL
from google.colab import output
output.serve_kernel_port_as_window(6006)
```

Access from phone browser to see live training graphs

**3. Status File:**
```python
# Updates every epoch
import json
with open('/content/drive/MyDrive/training_status.json', 'w') as f:
    json.dump({
        'epoch': current_epoch,
        'accuracy': current_accuracy,
        'estimated_time_remaining': time_left
    }, f)
```

Check Google Drive on phone for status updates

---

## ⚙️ Complete Automation Setup (Step-by-Step)

### **Day 1: Setup (15 minutes)**

1. **Open Google Colab:** https://colab.research.google.com
2. **Create new notebook:** File → New notebook
3. **Enable GPU:** Runtime → Change runtime type → GPU → Save
4. **Paste automation script** (from Option 1 above)
5. **Upload kaggle.json** (get from https://www.kaggle.com/settings)
6. **Connect Google Drive:** Run drive.mount() cell
7. **Save notebook:** File → Save a copy to Drive

### **Every Training Session (1 click)**

1. Open saved notebook in Colab
2. Click **Runtime → Run all**
3. **Close laptop** ✅
4. Wait 2-4 hours
5. Open Google Drive on phone/laptop
6. Download trained model

---

## 💾 Storage Management

### **During Training:**
```
Cloud (Colab/Kaggle):  7-8 GB
Your Laptop:            0 GB (not used)
```

### **After Training:**
```
Cloud:                  Can delete everything
Google Drive:           18 MB (trained model only)
Your Laptop:            18 MB (when you download)
```

### **Auto-Cleanup Script:**
```python
# Add at end of training
import shutil

print("🧹 Cleaning up temporary files...")

# Delete dataset (save space)
shutil.rmtree('/content/data')

# Keep only final model in Drive
# Everything else is in cloud, deleted when session ends

print("✅ Cleanup complete! Only model remains in Drive.")
```

---

## 🎯 My Recommended Automation Setup

**For you (easiest, free, fully automated):**

### **Use Google Colab with this workflow:**

```
1. Setup (once):
   - Create automated Colab notebook
   - Configure Kaggle API
   - Mount Google Drive
   
2. Every time you want to train:
   - Open notebook
   - Click "Run all"
   - Close laptop
   - Wait 2-4 hours
   - Download model from Google Drive

3. No laptop needed during training
4. Auto-saves to Google Drive
5. Can check progress on phone
6. Get notification when done (optional)
```

**Cost:** $0 (free tier)  
**Setup time:** 15 minutes (one-time)  
**Training time:** 2-4 hours (automated)  
**Your involvement:** 1 click to start, 1 click to download

---

## 📋 Automation Checklist

✅ **Before starting training:**
- [ ] Colab notebook created and saved
- [ ] GPU enabled in runtime settings
- [ ] Kaggle API configured (kaggle.json uploaded)
- [ ] Google Drive mounted for auto-save
- [ ] Model code uploaded/cloned
- [ ] Notification method setup (optional)

✅ **During training:**
- [ ] Close laptop (training continues in cloud)
- [ ] Model auto-saves checkpoints
- [ ] Google Drive syncs trained model
- [ ] Can check progress on phone

✅ **After training:**
- [ ] Download model from Google Drive
- [ ] Cleanup temporary files
- [ ] Test model locally

---

## 🆘 Troubleshooting Automation

| Issue | Solution |
|---|---|
| "Session disconnected" | Use Colab Pro for longer sessions, or Kaggle (9-hour limit) |
| "Lost training progress" | Checkpoint auto-save works, model saved every improved epoch |
| "Can't find saved model" | Check Google Drive → plant_disease_model.h5 |
| "Training didn't start" | Check GPU enabled, all cells ran without errors |
| "Need longer than 12 hours" | Split training: save checkpoint, resume next day |

---

## 🎓 Summary

**YES, you can:**
✅ Give dataset source once  
✅ Start training with 1 click  
✅ Close laptop immediately  
✅ Training runs in cloud (2-4 hours)  
✅ Auto-saves to Google Drive  
✅ Get notified when done  
✅ Download trained model (18 MB)  
✅ Your laptop: 0 GB used, 0 hours running  

**Setup once, use forever!**

Ready to set up automation? I can help you create the automated notebook!
