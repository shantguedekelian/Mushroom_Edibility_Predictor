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
    classes = os.listdir(DATA_DIR)
    chosen_class = random.choice(classes)

    class_folder = os.path.join(DATA_DIR, chosen_class)
    img_name = random.choice(os.listdir(class_folder))

    img_path = os.path.join(class_folder, img_name)

    return img_path, chosen_class


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
        "image_path": img_path,
        "true_label": true_label,
        "model_prediction": model_prediction
    })


@app.route('/data/<path:filename>')
def serve_image(filename):
    return send_file(os.path.join("data", filename))

# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)

