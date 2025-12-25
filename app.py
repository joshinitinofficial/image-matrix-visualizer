import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("Image as Matrix – Interactive Visualizer")

st.markdown("""
This app shows how **images are matrices**.
You can:
- View original image
- Inspect a **real sub-matrix**
- Edit matrix values
- Instantly see image changes
""")

# ===============================
# Upload Image
# ===============================
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)

    h, w, _ = img_array.shape

    # ===============================
    # Show Original Image
    # ===============================
    st.subheader("Original Image")
    st.image(img, use_container_width=True)
    st.write("Image Shape:", img_array.shape)

    st.divider()

    # ===============================
    # Matrix Window Selection
    # ===============================
    st.subheader("Select Matrix Window (Real Image Values)")

    col1, col2 = st.columns(2)

    with col1:
        row = st.number_input(
            "Start Row",
            min_value=0,
            max_value=h - 5,
            value=0
        )

    with col2:
        col = st.number_input(
            "Start Column",
            min_value=0,
            max_value=w - 5,
            value=0
        )

    # ===============================
    # Convert to Grayscale Matrix
    # ===============================
    gray = np.mean(img_array, axis=2).astype(np.uint8)

    sample_matrix = gray[row:row + 5, col:col + 5]

    st.markdown("### Sample Matrix (5×5 – Grayscale)")
    st.write("Each value = pixel intensity (0–255)")

    # ===============================
    # Editable Matrix
    # ===============================
    edited_matrix = st.data_editor(
        sample_matrix,
        use_container_width=True,
        key="matrix_editor"
    )

    # ===============================
    # Apply Edited Matrix Back
    # ===============================
    modified_gray = gray.copy()
    modified_gray[row:row + 5, col:col + 5] = np.clip(
        edited_matrix, 0, 255
    )

    st.divider()

    # ===============================
    # Slider Based Global Operation
    # ===============================
    st.subheader("Global Matrix Operation")

    value = st.slider(
        "Brightness Value (Matrix Addition)",
        min_value=-100,
        max_value=100,
        value=0
    )

    modified_gray = np.clip(modified_gray + value, 0, 255)

    st.divider()

    # ===============================
    # Show Results
    # ===============================
    colA, colB = st.columns(2)

    with colA:
        st.subheader("Modified Image")
        st.image(modified_gray, clamp=True)

    with colB:
        st.subheader("Difference (Matrix Effect)")
        diff = modified_gray.astype(int) - gray.astype(int)
        st.image(diff, clamp=True)

    st.divider()

    st.markdown("""
    ### Teaching Notes
    - Image = matrix of numbers
    - Editing matrix ⇒ image changes
    - Slider = matrix addition
    - Sub-matrix = real part of image
    """)
