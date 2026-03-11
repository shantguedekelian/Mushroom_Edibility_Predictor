import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, render_template, jsonify, send_file
import torch
from torchvision import transforms
from PIL import Image
import random
import os
import json

from model_definition import get_model

# -------------------------
# Config
# -------------------------

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

DATA_DIR = "data/mushrooms/test"  # use test split for game

device = torch.device("cpu")

# -------------------------
# Transforms (NO augmentation)
# -------------------------

inference_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
])

# -------------------------
# Load Model
# -------------------------

model = get_model(num_classes=2)
model.load_state_dict(torch.load("model.pth", map_location=device))
model.to(device)
model.eval()

# Load class names
with open("class_names.json") as f:
    class_names = json.load(f)

# -------------------------
# Flask App
# -------------------------

app = Flask(__name__)

# -------------------------
# Helper Functions
# -------------------------

def get_random_image():
    all_images = []

    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                full_path = os.path.join(root, file)

                # Label is the folder right under /test/
                relative_path = os.path.relpath(full_path, DATA_DIR)
                label = relative_path.split(os.sep)[0]

                all_images.append((full_path, label))

    if not all_images:
        raise Exception("No images found in test directory")

    return random.choice(all_images)




def predict_image(img_path):
    image = Image.open(img_path).convert("RGB")
    image = inference_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        pred_idx = outputs.argmax(dim=1).item()

    return class_names[pred_idx]

# -------------------------
# Routes
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_image")
def get_image():
    img_path, true_label = get_random_image()
    model_prediction = predict_image(img_path)

    return jsonify({
    "image_path": f"/image/{img_path}",
    "model_prediction": model_prediction,
    "true_label": true_label
})


# @app.route('/data/<path:filename>')
# def serve_image(filename):
#     return send_file(os.path.join("data", filename))


@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_file(filename)

# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

