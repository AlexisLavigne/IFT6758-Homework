import os
from flask import Flask, jsonify, request, abort
from PIL import Image
import requests
from io import BytesIO

from torchvision.models import get_model, get_model_weights

VALID_MODELS = [
    "resnet152",
    "convnext_base",
    "swin_b",
    "vgg16",
]

def load_model(model_name="resnet152"):
    # Initialize model with weights
    weights = get_model_weights(model_name).DEFAULT
    model = get_model(model_name, weights=weights)
    model.eval()
    return model, weights

def download_img(url: str) -> Image:
    # Downloads image to memory.
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def set_global_key(key, value):
    globals()[key] = value


# Initialize app and load global model and weights
app = Flask(__name__)
model, weights = load_model()


@app.route("/hello", methods=["GET"])
def healthcheck():
    return jsonify("Hello!")


@app.route("/models", methods=["GET"])
def get_models():
    """
    Returns the list of available models to use.
    """
    return jsonify(VALID_MODELS)

@app.route("/model/<id>", methods=["PUT"])
def set_model(id):
    if not id in VALID_MODELS:
        abort(500, f"{id} is not part of valid models: {','.join(VALID_MODELS)}")
    model, weights = load_model(id)
    set_global_key("model", model)
    set_global_key("weights", weights)
    app.logger.info(f"Model changed to {id}.")
    return jsonify(model=id)


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Returns predictions
    """
    # Get POST json data
    json = request.get_json()
    app.logger.info(json)

    # Extract url. Return 500 if not included in request.
    url = json.get('url', None)
    if url is None:
        abort(500, "url was not specified in the request.")

    # Get Image from URL
    img = download_img(url)
    preprocess = weights.transforms()
    batch = preprocess(img).unsqueeze(0)

    # Get prediction and return
    prediction = model(batch).squeeze(0).softmax(0)
    class_id = prediction.argmax().item()
    category = weights.meta['categories'][class_id]
    app.logger.info({"category":category})
    return jsonify(category=category)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("SERVING_PORT", 8000))