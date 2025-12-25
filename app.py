import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("Image ↔ Matrix Visualization (Educational Tool)")

st.markdown("""
Each image form is generated using a **different matrix operation**  
and therefore has its **own valid control parameter**.
Presented by Ms. Khyati (Assistant Professor, Parul University)
""")

# ==========================
# Upload Image
# ==========================
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_rgb = np.array(img)

    # Base grayscale matrix (true 2D matrix)
    base_gray = np.mean(img_rgb, axis=2).astype(np.uint8)
    h, w = base_gray.shape

    # ==========================
    # Matrix Window
    # ==========================
    st.subheader("Matrix Window (Real Sub-Matrix)")

    c1, c2 = st.columns(2)
    with c1:
        row = st.number_input("Start Row", 0, h - 5, 0)
    with c2:
        col = st.number_input("Start Column", 0, w - 5, 0)

    base_matrix = base_gray[row:row+5, col:col+5]

    st.divider()

    # ==========================
    # OPERATION CONTROLS
    # ==========================
    st.subheader("Operation Controls")

    b_col, i_col, t_col = st.columns(3)

    with b_col:
        brightness_val = st.slider(
            "Brightness Increase (Matrix + value)",
            min_value=0,
            max_value=100,
            value=30
        )

    with i_col:
        invert_strength = st.slider(
            "Inversion Strength (%)",
            min_value=0,
            max_value=100,
            value=100
        )

    with t_col:
        threshold_val = st.slider(
            "Threshold Level (0–255)",
            min_value=0,
            max_value=255,
            value=128
        )

    alpha = invert_strength / 100.0

    # ==========================
    # IMAGE GENERATION
    # ==========================
    bright = np.clip(base_gray + brightness_val, 0, 255).astype(np.uint8)

    invert = np.clip(
        (1 - alpha) * base_gray + alpha * (255 - base_gray),
        0, 255
    ).astype(np.uint8)

    threshold = np.where(base_gray > threshold_val, 255, 0).astype(np.uint8)

    # Corresponding matrices
    bright_matrix = bright[row:row+5, col:col+5]
    invert_matrix = invert[row:row+5, col:col+5]
    thresh_matrix = threshold[row:row+5, col:col+5]

    # ==========================
    # DISPLAY
    # ==========================
    st.subheader("Images and Their Matrices")

    tabs = st.tabs([
        "Original",
        "Brightness",
        "Inversion",
        "Threshold"
    ])

    with tabs[0]:
        c1, c2 = st.columns(2)
        c1.image(base_gray, caption="Original Image", clamp=True)
        c2.dataframe(base_matrix)

    with tabs[1]:
        c1, c2 = st.columns(2)
        c1.image(bright, caption="Brightness Image", clamp=True)
        c2.dataframe(bright_matrix)

    with tabs[2]:
        c1, c2 = st.columns(2)
        c1.image(invert, caption="Inversion Image", clamp=True)
        c2.dataframe(invert_matrix)

    with tabs[3]:
        c1, c2 = st.columns(2)
        c1.image(threshold, caption="Threshold Image", clamp=True)
        c2.dataframe(thresh_matrix)

    st.divider()

    st.markdown("""
    ### Teaching Notes
    - Brightness → matrix addition
    - Inversion → linear combination of matrix and its complement
    - Threshold → conditional operation
    - All controls stay within valid pixel limits
    
    """)
