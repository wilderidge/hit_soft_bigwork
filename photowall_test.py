import streamlit as st
import os
from PIL import Image
import base64

# Create a directory to save uploaded images
UPLOAD_DIR = "uploaded_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def get_image_list():
    images = []
    for file_name in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if os.path.isfile(file_path):
            images.append(file_name)
    return images

def display_images(image_list):
    html_content = """
    <html>
    <head>
    <style>
    .image-container {
        position: relative;
        width: 100%;
        height: 800px;
        border: 1px solid #ccc;
    }
    .image-item {
        position: absolute;
        cursor: move;
        resize: both;
        overflow: hidden;
    }
    </style>
    </head>
    <body>
    <div class="image-container" id="imageContainer">
    """
    for image_name in image_list:
        file_path = os.path.join(UPLOAD_DIR, image_name)
        with open(file_path, "rb") as img_file:
            base64_img = base64.b64encode(img_file.read()).decode("utf-8")
        html_content += f"""
        <img src="data:image/jpeg;base64,{base64_img}" class="image-item" width="200" draggable="true" ondragstart="drag(event)" id="{image_name}">
        """
    html_content += """
    </div>
    <script>
    function drag(event) {
        event.dataTransfer.setData("text", event.target.id);
    }
    document.addEventListener('DOMContentLoaded', function() {
        var container = document.getElementById('imageContainer');
        container.ondragover = function(event) {
            event.preventDefault();
        };
        container.ondrop = function(event) {
            event.preventDefault();
            var data = event.dataTransfer.getData("text");
            var elem = document.getElementById(data);
            elem.style.left = event.clientX - elem.width / 2 + 'px';
            elem.style.top = event.clientY - elem.height / 2 + 'px';
        };

        const images = document.querySelectorAll('.image-item');
        images.forEach(img => {
            img.style.transform = 'rotate(0deg)';

            img.onwheel = function(event) {
                const currentRotation = parseFloat(img.style.transform.replace('rotate(', '').replace('deg)', '')) || 0;
                const newRotation = currentRotation + (event.deltaY > 0 ? 15 : -15);
                img.style.transform = `rotate(${newRotation}deg)`;
            };
        });
    });
    </script>
    </body>
    </html>
    """
    return html_content

st.title("照片墙")

# File uploader
uploaded_file = st.file_uploader("上传照片", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    save_uploaded_file(uploaded_file)

# Display images
image_list = get_image_list()
if image_list:
    st.markdown("## 照片墙")
    st.components.v1.html(display_images(image_list), height=900)
