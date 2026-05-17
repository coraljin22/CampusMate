import streamlit as st
from ultralytics import YOLO
from PIL import Image
import pandas as pd
import tempfile
import os

st.set_page_config(page_title="Accessibility Audit Tool", layout="wide")

st.title("AI Public Transport Accessibility Audit Tool")

model = YOLO("yolov8n.pt")

rules = {
    "bus": "Public transport vehicle detected.",
    "train": "Train detected.",
    "person": "People detected. Check if pathway is clear.",
    "bench": "Seating available.",
    "chair": "Seating available.",
    "traffic light": "Traffic signal detected.",
    "stop sign": "Signage detected.",
    "bicycle": "Possible pathway obstacle.",
    "car": "Possible access obstruction.",
    "truck": "Possible access obstruction."
}

barriers = ["bicycle", "car", "truck"]

file = st.file_uploader(
    "Upload an image of a bus stop, tram stop, or train platform",
    type=["jpg", "jpeg", "png"]
)

if file:
    image = Image.open(file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)
        path = tmp.name

    result = model(path)[0]
    annotated = result.plot()

    st.subheader("AI Detection Result")
    st.image(annotated, use_container_width=True)

    detected = []

    for box in result.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        name = result.names[cls]

        if conf >= 0.35:
            detected.append({
                "Detected Object": name,
                "Confidence": round(conf, 2),
                "Accessibility Meaning": rules.get(
                    name,
                    "Manual review required."
                )
            })

    st.subheader("Detection Table")

    if detected:
        df = pd.DataFrame(detected)
        st.dataframe(df, use_container_width=True)

        st.subheader("Accessibility Report")

        st.markdown("### Accessibility Features")
        for item in detected:
            obj = item["Detected Object"]
            if obj in rules and obj not in barriers:
                st.write(f"- {obj}: {rules[obj]}")

        st.markdown("### Potential Barriers")
        found_barrier = False
        for item in detected:
            obj = item["Detected Object"]
            if obj in barriers:
                st.write(f"- {obj}: {rules[obj]}")
                found_barrier = True

        if not found_barrier:
            st.write("- No major visible barrier detected.")

        st.markdown("### Manual Check Required")
        st.write("- Ramp availability and gradient")
        st.write("- Tactile ground surface indicators")
        st.write("- Platform edge safety")
        st.write("- Clear path width")
        st.write("- Handrails")
        st.write("- Signage readability")

    else:
        st.warning("No objects detected.")

    os.remove(path)