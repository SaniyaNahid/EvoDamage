import streamlit as st
import json
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="EvoDamage - Model Performance",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

METRICS_FILE = BASE_DIR / "outputs" / "metrics" / "metrics.json"
REPORT_FILE = BASE_DIR / "outputs" / "metrics" / "classification_report.txt"
CONFUSION_MATRIX = BASE_DIR / "outputs" / "plots" / "confusion_matrix.png"


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📊 Model Performance")
st.write(
    "Performance evaluation of the EvoDamage damage classification model."
)

st.info(
    "Prototype evaluation using a synthetic disaster-damage dataset."
)


# --------------------------------------------------
# LOAD METRICS
# --------------------------------------------------

metrics = {}

if METRICS_FILE.exists():

    try:
        with open(METRICS_FILE, "r") as file:
            metrics = json.load(file)

    except Exception as e:
        st.error(f"Unable to read metrics file: {e}")

else:
    st.warning(
        "Metrics file not found. Run src/evaluation.py first."
    )


# --------------------------------------------------
# METRIC CARDS
# --------------------------------------------------

if metrics:

    accuracy = metrics.get("accuracy", 0)
    precision = metrics.get("precision", 0)
    recall = metrics.get("recall", 0)
    f1 = metrics.get("f1_score", 0)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Accuracy",
            f"{accuracy * 100:.2f}%"
        )

    with col2:
        st.metric(
            "Precision",
            f"{precision * 100:.2f}%"
        )

    with col3:
        st.metric(
            "Recall",
            f"{recall * 100:.2f}%"
        )

    with col4:
        st.metric(
            "F1 Score",
            f"{f1 * 100:.2f}%"
        )


# --------------------------------------------------
# MODEL INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("Model Information")

col1, col2 = st.columns(2)

with col1:

    st.write("**Architecture:** ResNet18")
    st.write("**Learning approach:** Transfer Learning")
    st.write("**Framework:** PyTorch")

with col2:

    st.write("**Number of classes:** 4")
    st.write("**Input size:** 224 × 224")
    st.write("**Task:** Building Damage Classification")


# --------------------------------------------------
# DAMAGE CLASSES
# --------------------------------------------------

st.subheader("Damage Classes")

classes = [
    "No Damage",
    "Minor Damage",
    "Major Damage",
    "Destroyed"
]

for i, damage_class in enumerate(classes, start=1):
    st.write(f"**{i}.** {damage_class}")


# --------------------------------------------------
# CONFUSION MATRIX
# --------------------------------------------------

st.divider()

st.subheader("Confusion Matrix")

if CONFUSION_MATRIX.exists():

    st.image(
        str(CONFUSION_MATRIX),
        caption="EvoDamage Damage Classification Confusion Matrix",
        use_container_width=True
    )

else:

    st.warning(
        "Confusion matrix not found. Run src/evaluation.py first."
    )


# --------------------------------------------------
# CLASSIFICATION REPORT
# --------------------------------------------------

st.divider()

st.subheader("Classification Report")

if REPORT_FILE.exists():

    try:

        with open(REPORT_FILE, "r") as file:
            report = file.read()

        st.code(
            report,
            language="text"
        )

    except Exception as e:

        st.error(
            f"Unable to read classification report: {e}"
        )

else:

    st.warning(
        "Classification report not found."
    )


# --------------------------------------------------
# LIMITATION
# --------------------------------------------------

st.divider()

st.subheader("Evaluation Note")

st.write(
    """
    The current evaluation was performed using a synthetic prototype
    dataset created to validate the complete EvoDamage ML pipeline.

    These results should not be interpreted as real-world disaster
    damage accuracy. Real-world deployment would require training and
    validation using real disaster imagery such as the xBD dataset.
    """
)