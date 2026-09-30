import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from src.gis import create_damage_map


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EvoDamage | Damage Map",
    page_icon="🗺️",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🗺️ Building Damage Map")

st.write(
    "Interactive geographic visualization of building-level "
    "damage assessment results."
)


# ============================================================
# LOAD DATA
# ============================================================

try:

    data = pd.read_csv("sample_data.csv")

except FileNotFoundError:

    st.error(
        "sample_data.csv was not found. "
        "Please place it in the project root directory."
    )

    st.stop()


# ============================================================
# VALIDATE DATA
# ============================================================

required_columns = [
    "building_id",
    "latitude",
    "longitude",
    "damage",
    "confidence"
]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]

if missing_columns:

    st.error(
        f"Missing columns: {', '.join(missing_columns)}"
    )

    st.stop()


# ============================================================
# DAMAGE COUNTS
# ============================================================

total = len(data)

no_damage = len(
    data[data["damage"] == "no-damage"]
)

minor = len(
    data[data["damage"] == "minor-damage"]
)

major = len(
    data[data["damage"] == "major-damage"]
)

destroyed = len(
    data[data["damage"] == "destroyed"]
)


# ============================================================
# SUMMARY
# ============================================================

st.subheader("Assessment Summary")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Buildings",
        total
    )

with col2:
    st.metric(
        "🟢 No Damage",
        no_damage
    )

with col3:
    st.metric(
        "🟡 Minor",
        minor
    )

with col4:
    st.metric(
        "🟠 Major",
        major
    )

with col5:
    st.metric(
        "🔴 Destroyed",
        destroyed
    )


# ============================================================
# MAP LEGEND
# ============================================================

st.divider()

st.subheader("Map Legend")

legend1, legend2, legend3, legend4 = st.columns(4)

with legend1:
    st.success("🟢 No Damage")

with legend2:
    st.warning("🟡 Minor Damage")

with legend3:
    st.error("🟠 Major Damage")

with legend4:
    st.error("🔴 Destroyed")


# ============================================================
# INTERACTIVE MAP
# ============================================================

st.divider()

st.subheader("Interactive Building Damage Map")

damage_map = create_damage_map(data)

st_folium(
    damage_map,
    width=None,
    height=600,
    returned_objects=[]
)


# ============================================================
# DATA TABLE
# ============================================================

st.divider()

st.subheader("Building Assessment Data")

display_data = data.copy()

display_data["damage"] = (
    display_data["damage"]
    .str.replace("-", " ")
    .str.title()
)

display_data["confidence"] = (
    display_data["confidence"] * 100
).round(1).astype(str) + "%"

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)