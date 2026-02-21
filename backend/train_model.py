import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# -------- CONFIG --------
DATASET_PATH = "../dataset"
MODEL_PATH = "model.h5"

IMG_SIZE = 224
BATCH = 16
EPOCHS = 1   # retraining fast rahega

# -------- DATA --------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH,
    class_mode="binary",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH,
    class_mode="binary",
    subset="validation"
)

# -------- LOAD OR CREATE MODEL --------
if os.path.exists(MODEL_PATH):
    print("✅ Loading existing trained model...")
    model = tf.keras.models.load_model(MODEL_PATH)

else:
    print("🆕 Creating new model...")

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224,224,3),
        include_top=False,
        weights="imagenet"
    )

    base_model.trainable = False

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

# -------- TRAIN --------
model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# -------- SAVE --------
model.save(MODEL_PATH)

print("✅ Model updated successfully!")