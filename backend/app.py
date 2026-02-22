import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.model_utils import predict_image
from backend.reinforcement import save_feedback

app = Flask(__name__)
CORS(app)

# -------- FOLDERS --------
UPLOAD_FOLDER = "uploads"   # IMPORTANT (no ../)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------- LEARNING COUNTER --------
LEARN_COUNT_FILE = "backend/learn_count.txt"

if not os.path.exists(LEARN_COUNT_FILE):
    with open(LEARN_COUNT_FILE, "w") as f:
        f.write("0")


# -------- HEALTH CHECK (VERY IMPORTANT FOR RENDER) --------
@app.route("/")
def home():
    return {"status": "Deepfake Detector API Running ✅"}


# -------- PREDICT API --------
@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["file"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    result, score = predict_image(filepath)

    return jsonify({
        "result": result,
        "score": float(score),
        "filename": file.filename
    })


# -------- FEEDBACK API --------
@app.route("/feedback", methods=["POST"])
def feedback():

    data = request.json
    filename = data["filename"]
    label = data["label"]

    save_feedback(filename, label)

    with open(LEARN_COUNT_FILE, "r") as f:
        count = int(f.read())

    count += 1

    with open(LEARN_COUNT_FILE, "w") as f:
        f.write(str(count))

    return jsonify({"status": "feedback saved"})


# -------- GET LEARNING COUNT --------
@app.route("/learn-count")
def learn_count():
    with open(LEARN_COUNT_FILE, "r") as f:
        count = f.read()
    return {"count": count}


# -------- AUTO RETRAIN --------
@app.route("/retrain")
def retrain():
    subprocess.Popen(["python", "backend/retrain_reinforcement.py"])
    return {"status": "training started"}


# -------- RUN SERVER (LOCAL ONLY) --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
