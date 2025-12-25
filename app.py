import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("Image ↔ Matrix Visualization (Educational Tool)")

st.markdown("""
This app shows **multiple images** and their **respective matrices**.
Changing the input parameter updates **all images and matrices**.
""")

# ==========================
# Upload Image
# ==========================
uploaded_file = st.file_uploader(
    "Upload an image", type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_rgb = np.array(img)

    # Base grayscale matrix (true 2D matrix)
    base_gray = np.mean(img_rgb, axis=2).astype(np.uint8)

    h, w = base_gray.shape

    # ==========================
    # Matrix Window Selection
    # ==========================
    st.subheader("Matrix Window (Real Sub-Matrix)")

    col1, col2 = st.columns(2)

    with col1:
        row = st.number_input(
            "Start Row", 0, h - 5, 0
        )
    with col2:
        col = st.number_input(
            "Start Column", 0, w - 5, 0
        )

    base_matrix = base_gray[row:row+5, col:col+5]

    # ==========================
    # Global Control Parameter
    # ==========================
    st.subheader("Control Parameter (Matrix Operation)")
    value = st.slider(
        "Value (used in all operations)",
        min_value=-100,
        max_value=100,
        value=30
    )

    # ==========================
    # Generate Derived Images
    # ==========================
    bright = np.clip(base_gray + value, 0, 255).astype(np.uint8)
    invert = 255 - base_gray
    threshold = np.where(base_gray > 128, 255, 0).astype(np.uint8)

    bright_matrix = bright[row:row+5, col:col+5]
    invert_matrix = invert[row:row+5, col:col+5]
    thresh_matrix = threshold[row:row+5, col:col+5]

    # ==========================
    # DISPLAY SECTION
    # ==========================
    st.divider()

    st.subheader("Images and Their Matrices")

    tabs = st.tabs([
        "Original",
        "Brightness",
        "Inversion",
        "Threshold"
    ])

    # ---------- ORIGINAL ----------
    with tabs[0]:
        c1, c2 = st.columns(2)
        c1.image(base_gray, caption="Original Image", clamp=True)
        c2.markdown("### Matrix")
        c2.dataframe(base_matrix)

    # ---------- BRIGHTNESS ----------
    with tabs[1]:
        c1, c2 = st.columns(2)
        c1.image(bright, caption="Brightness Image", clamp=True)
        c2.markdown("### Matrix")
        c2.dataframe(bright_matrix)

    # ---------- INVERSION ----------
    with tabs[2]:
        c1, c2 = st.columns(2)
        c1.image(invert, caption="Inverted Image", clamp=True)
        c2.markdown("### Matrix")
        c2.dataframe(invert_matrix)

    # ---------- THRESHOLD ----------
    with tabs[3]:
        c1, c2 = st.columns(2)
        c1.image(threshold, caption="Threshold Image", clamp=True)
        c2.markdown("### Matrix")
        c2.dataframe(thresh_matrix)

    st.divider()

    st.markdown("""
    ### Teaching Summary
    - Image = Matrix
    - One input → many transformations
    - Each image has its own matrix
    - Matrices shown are **real sub-matrices**
    """)
