import streamlit as st
from PIL import Image
import os
import torch.backends.cudnn as cudnn

# Import functions/variables from YOLOv5 utils
# Adjust according to the actual module paths and available functions
try:
    from utils.general import colors, save_one_box
except ImportError:
    colors, save_one_box = None, None

try:
    from utils.torch_utils import time_sync
except ImportError:
    time_sync = None

try:
    from utils.plots import Annotator
except ImportError:
    Annotator = None

st.title("YOLOv5 Detection Inference")

# Option to upload an image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    st.write("")
    st.write("Running YOLOv5...")

    # Save the uploaded image
    image_path = "uploaded_image.jpg"
    image.save(image_path)

    # Run YOLOv5 detection on the uploaded image
    os.system(f"python yolov5_script.py --source {image_path} --view-img")

    # Display the detected image
    detected_image_path = "runs/detect/exp/uploaded_image.jpg"
    if os.path.exists(detected_image_path):
        detected_image = Image.open(detected_image_path)
        st.image(detected_image, caption="Detected Image.", use_column_width=True)
