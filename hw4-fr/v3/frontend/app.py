import os
from io import BytesIO
from PIL import Image
import validators
import streamlit as st
import requests

# Streamlit app for Animal Classification
HOST = os.environ.get("SERVING_HOST", "0.0.0.0")
PORT = os.environ.get("SERVING_PORT", "8080")
API_GATEWAY = os.environ.get("API_GATEWAY", "")

if API_GATEWAY != "":
    BASE_URL = API_GATEWAY
else:
    BASE_URL = f"{HOST}:{PORT}"

def valid_img_extension(url: str) -> bool:
    """
    Determines if image is a valid image extension.
    """
    return url.split(".")[-1].lower() in [
        "jpg",
        "jpeg",
        "png",
    ]

def get_predictions(model_id: str, image_url: str):
    """
    Send image url to backend to get prediction.
    """
    return requests.post(f"{BASE_URL}/model/{model_id}/predict", json=dict(url=image_url))


def get_model_list():
    """
    Returns the list of valid models
    """
    # Code to get the list of valid models.


st.title("Animal Classification")
st.write("Load an image from a URL for classification.")

with st.container():
    valid_models = get_model_list().json()
    st.selectbox("Select model to use", valid_models, key="model_name")

url = st.text_input("Image URL", key="url")
img: Image

with st.container():
    if url != "":
        # Validate URL
        valid_url = validators.url(url)
        valid_img = valid_img_extension(url)
        if not valid_url:
            st.error("The URL provided is not valid.")
            st.stop()
        if not valid_img:
            st.error("The URL provided is not a valid image.")
            st.stop()

        # Try to download the image.
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
        except:
            st.error("There was an error uploading the image.")
            st.stop()

        # Display image
        st.image(img, caption="Uploaded photo.")

        # Send image to backend to get prediction
        with st.spinner("Please wait..."):
            result = get_predictions(url, st.session_state.model_name)

        if result.status_code == 200:
            st.write(f"I think this is an image of a {result.json()['category']}.")
        else:
            st.error("There was an error receiving predictions")

st.markdown("")