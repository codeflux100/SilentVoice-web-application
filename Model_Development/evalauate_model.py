import cv2
import numpy as np
import tensorflow as tf
import os
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
# Path to your Test Data folder (The one you created in Step 1)
test_data_path = "C:/Users/acer/Desktop/PROJECT1.2/Test_dataset" 

# Path to your model and labels
model_path = "C:/Users/acer/Desktop/converted_keras1/keras_model.h5"
labels_path = "C:/Users/acer/Desktop/converted_keras1/labels.txt"

# Image size (Must match what you used in Datacollection.py)
img_size = 224  # Teachable Machine usually exports 224x224. Check if yours is 300 or 224.
# Note: Your Datacollection uses 300, but Keras models often expect 224. 
# If you get a shape error, change this to 300.

# ---------------------

def load_labels(path):
    with open(path, 'r') as f:
        class_names = f.read().splitlines()
    # Extract just the label names (remove numbers if present)
    class_names = [c.split(' ')[1:] for c in class_names]
    class_names = [" ".join(c) for c in class_names]
    return class_names

def evaluate():
    # 1. Load Model and Labels
    print("Loading model...")
    model = tf.keras.models.load_model(model_path, compile=False)
    class_names = load_labels(labels_path)
    print(f"Classes: {class_names}")

    y_true = []
    y_pred = []

    # 2. Iterate through Test Data
    for label_name in os.listdir(test_data_path):
        folder_path = os.path.join(test_data_path, label_name)
        
        if not os.path.isdir(folder_path):
            continue

        # Find the index for this class
        if label_name not in class_names:
            print(f"Warning: Folder '{label_name}' not found in labels file. Skipping.")
            continue
        
        label_index = class_names.index(label_name)
        
        print(f"Processing class: {label_name}...")

        for img_file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_file)
            
            # Read and preprocess image
            img = cv2.imread(img_path)
            if img is None:
                continue
            
            # Resize to model input size
            img = cv2.resize(img, (img_size, img_size))
            
            # Normalize (Standard for Teachable Machine models)
            img = (img.astype(np.float32) / 127.0) - 1
            
            # Reshape for model (1, 224, 224, 3)
            img = np.expand_dims(img, axis=0)

            # Predict
            prediction = model.predict(img, verbose=0)
            predicted_index = np.argmax(prediction)

            y_true.append(label_index)
            y_pred.append(predicted_index)

    # 3. Calculate Metrics
    print("\n" + "="*30)
    print("EVALUATION RESULTS")
    print("="*30)
    
    # Accuracy
    accuracy = np.mean(np.array(y_true) == np.array(y_pred))
    print(f"Overall Accuracy: {accuracy * 100:.2f}%")

    # Detailed Report (Precision, Recall, F1-Score)
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Plot Confusion Matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()

if __name__ == "__main__":
    evaluate()