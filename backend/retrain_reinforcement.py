import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ---------- CONFIG ----------
MODEL_PATH = "model.h5"
RL_DATASET = "../reinforcement_data"

IMG_SIZE = 224
BATCH_SIZE = 4
EPOCHS = 1   # fast learning

# ---------- CHECK DATA ----------
if not os.path.exists(RL_DATASET):
    print("❌ reinforcement_data folder not found")
    exit()

total_images = sum([
    len(files) for r, d, files in os.walk(RL_DATASET)
])

if total_images == 0:
    print("⚠️ No reinforcement images yet.")
    exit()

print(f"✅ Found {total_images} reinforcement images")

# ---------- DATA LOADER ----------
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8,1.2]
)

train_data = datagen.flow_from_directory(
    RL_DATASET,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary"
)

# ---------- LOAD EXISTING MODEL ----------
print("🧠 Loading existing model...")
model = tf.keras.models.load_model(MODEL_PATH)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# ---------- TRAIN ----------
print("⚡ Reinforcement training started...")

model.fit(
    train_data,
    epochs=EPOCHS
)

# ---------- SAVE UPDATED MODEL ----------
model.save(MODEL_PATH)

print("✅ Model updated & saved into model.h5")