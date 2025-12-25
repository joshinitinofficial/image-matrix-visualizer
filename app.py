import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Image as Matrix – Visualization Tool")

st.markdown("""
This tool demonstrates how **matrix operations change an image**.
The image is treated as a **full matrix**.  
Only a **small sample sub-matrix** is shown for understanding.
""")

# -----------------------------
# Upload Image
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload an image", type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)

    st.subheader("Original Image")
    st.image(img, use_container_width=True)

    st.write("Image Matrix Shape:", img_array.shape)

    # -----------------------------
    # Sample Matrix Window
    # -----------------------------
    st.subheader("Sample Matrix (Real Sub-Matrix from Image)")

    row = st.number_input("Start Row", min_value=0, max_value=img_array.shape[0]-5, value=0)
    col = st.number_input("Start Column", min_value=0, max_value=img_array.shape[1]-5, value=0)

    sample_matrix = img_array[row:row+5, col:col+5]
    st.write(sample_matrix)

    # -----------------------------
    # Matrix Operation Input
    # -----------------------------
    st.subheader("Matrix Operation Input")

    value = st.slider(
        "Value (controls matrix operation)",
        min_value=-100,
        max_value=100,
        value=30
    )

    operation = st.selectbox(
        "Choose Operation",
        ["Brightness (Addition)", "Inversion", "Grayscale"]
    )

    # -----------------------------
    # Apply Matrix Operation
    # -----------------------------
    modified = img_array.copy()

    if operation == "Brightness (Addition)":
        modified = np.clip(modified + value, 0, 255)

    elif operation == "Inversion":
        modified = 255 - modified

    elif operation == "Grayscale":
        modified = np.mean(modified, axis=2).astype(np.uint8)

    # -----------------------------
    # Display Result
    # -----------------------------
    st.subheader("Resulting Image After Matrix Operation")

    if modified.ndim == 2:
        st.image(modified, clamp=True)
    else:
        st.image(modified.astype(np.uint8))

    st.markdown("""
    **Teaching Notes**
    - Image = Matrix
    - Brightness → Matrix Addition
    - Inversion → Matrix Subtraction
    - Grayscale → Mean Operation
    """)
