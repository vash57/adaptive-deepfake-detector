import tensorflow as tf
import numpy as np
from PIL import Image

# -------- Model Config --------
MODEL_PATH = "model.keras"
IMG_SIZE = 224

model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully")


# -------- Prediction Function --------
def predict_image(image_path):

    # image load
    img = Image.open(image_path).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))

    # preprocessing
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    # prediction
    pred = model.predict(img, verbose=0)[0][0]

    # decision
    if pred > 0.5:
        result = "Real Image"
    else:
        result = "AI Generated (Fake)"

    return result, float(pred)
