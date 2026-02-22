import os
import shutil

UPLOAD_FOLDER = "uploads"
RL_DATASET = "reinforcement_data"

# create folders
os.makedirs(os.path.join(RL_DATASET, "real"), exist_ok=True)
os.makedirs(os.path.join(RL_DATASET, "fake"), exist_ok=True)


def save_feedback(filename, label):

    src = os.path.join(UPLOAD_FOLDER, filename)

    if label == "real":
        dst = os.path.join(RL_DATASET, "real", filename)
    else:
        dst = os.path.join(RL_DATASET, "fake", filename)

    if os.path.exists(src):
        shutil.copy(src, dst)
        print("✅ Feedback saved:", filename, "→", label)
    else:
        print("⚠️ File not found:", src)
