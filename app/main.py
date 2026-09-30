import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EvoDamage | Disaster Intelligence",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LIGHT PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background-color: #f8fafc;
        color: #172033;
    }

    .main {
        background-color: #f8fafc;
    }

    /* ========================================================
       HIDE DEFAULT STREAMLIT PAGE NAVIGATION
       ======================================================== */

    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    [data-testid="stSidebar"] h1 {
        color: #0f172a !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #334155 !important;
    }

    [data-testid="stSidebar"] p {
        color: #64748b;
    }

    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        color: #0f172a !important;
        font-weight: 750 !important;
        letter-spacing: -0.4px;
    }

    h2 {
        color: #172033 !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #334155 !important;
        font-weight: 650 !important;
    }

    /* ========================================================
       BODY TEXT
       ======================================================== */

    p {
        color: #475569;
    }

    /* ========================================================
       METRIC CARDS
       ======================================================== */

    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 750 !important;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color: #2563eb;
        color: #ffffff;
        border: 1px solid #2563eb;
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
        border-color: #1d4ed8;
        color: #ffffff;
    }

    /* ========================================================
       INFO / SUCCESS / WARNING
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #e2e8f0;
    }

    /* ========================================================
       TABLES
       ======================================================== */

    [data-testid="stDataFrame"] {
        background-color: #ffffff;
        border-radius: 10px;
    }

    /* ========================================================
       SIDEBAR NAVIGATION LINKS
       ======================================================== */

    [data-testid="stSidebar"] a {
        color: #334155 !important;
        text-decoration: none !important;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {
        color: #94a3b8;
        font-size: 13px;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚨 EvoDamage")

    st.caption("AI Disaster Intelligence Platform")

    st.divider()

    st.subheader("🧭 Navigation")

    st.page_link(
        "main.py",
        label="Dashboard",
        icon="📊",
    )

    st.page_link(
        "pages/assessment.py",
        label="Damage Assessment",
        icon="🔍",
    )

    st.page_link(
        "pages/damage_map.py",
        label="Damage Map",
        icon="🗺️",
    )

    st.page_link(
        "pages/priority.py",
        label="Priority Analysis",
        icon="🚨",
    )

    st.page_link(
        "pages/performance.py",
        label="Model Performance",
        icon="📈",
    )

    st.divider()

    st.subheader("⚡ System Status")

    st.success("AI Pipeline Ready")
    st.success("GIS Module Ready")
    st.success("Priority Engine Ready")

    st.divider()

    st.caption("EvoDamage Prototype")
    st.caption("AI • Computer Vision • GIS")


# ============================================================
# MAIN HEADER
# ============================================================

st.info("🚨 AI-POWERED DISASTER ASSESSMENT")

st.title("EvoDamage")

st.subheader(
    "AI-Based Building Damage Assessment & Rescue Prioritization"
)

st.write(
    "A computer vision and geospatial intelligence platform for "
    "rapid preliminary assessment of building damage after disasters."
)


# ============================================================
# DASHBOARD OVERVIEW
# ============================================================

st.divider()

st.header("📊 Dashboard Overview")

st.write(
    "Monitor building damage, geographic impact and priority "
    "assessment from a single dashboard."
)


# ============================================================
# KEY METRICS
# ============================================================

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.metric(
        label="🏢 Buildings Analyzed",
        value="10",
    )

with metric2:

    st.metric(
        label="🔴 Major / Destroyed",
        value="5",
    )

with metric3:

    st.metric(
        label="🚨 Priority Zones",
        value="3",
    )

with metric4:

    st.metric(
        label="⚡ AI Pipeline",
        value="Ready",
    )


# ============================================================
# DAMAGE CLASSIFICATION
# ============================================================

st.divider()

st.header("🏚️ Damage Classification")

st.write(
    "The AI pipeline categorizes buildings according to "
    "their predicted level of damage."
)

damage1, damage2, damage3, damage4 = st.columns(4)

with damage1:

    st.metric(
        label="🟢 No Damage",
        value="2",
    )

with damage2:

    st.metric(
        label="🟡 Minor Damage",
        value="3",
    )

with damage3:

    st.metric(
        label="🟠 Major Damage",
        value="2",
    )

with damage4:

    st.metric(
        label="🔴 Destroyed",
        value="3",
    )


# ============================================================
# AI PIPELINE
# ============================================================

st.divider()

st.header("🤖 AI Assessment Pipeline")

st.write(
    "The system connects image analysis, machine learning, "
    "geospatial visualization and priority assessment."
)

pipeline1, pipeline2, pipeline3, pipeline4, pipeline5 = st.columns(5)

with pipeline1:

    st.subheader("01")

    st.write("📷 Image Input")

    st.caption(
        "Pre- and post-disaster imagery"
    )

with pipeline2:

    st.subheader("02")

    st.write("⚙️ Preprocessing")

    st.caption(
        "Image preparation and normalization"
    )

with pipeline3:

    st.subheader("03")

    st.write("🧠 AI Classification")

    st.caption(
        "Building damage prediction"
    )

with pipeline4:

    st.subheader("04")

    st.write("🗺️ GIS Mapping")

    st.caption(
        "Geographic visualization"
    )

with pipeline5:

    st.subheader("05")

    st.write("🚨 Priority Analysis")

    st.caption(
        "Affected-area assessment"
    )


# ============================================================
# PLATFORM CAPABILITIES
# ============================================================

st.divider()

st.header("🧠 Platform Capabilities")

capability1, capability2 = st.columns(2)

with capability1:

    st.subheader("Computer Vision")

    st.write(
        """
        • Building damage classification

        • Damage severity prediction

        • Prediction confidence

        • Image-based assessment

        • Model performance evaluation
        """
    )

with capability2:

    st.subheader("Geospatial Intelligence")

    st.write(
        """
        • Building-level coordinates

        • Interactive damage map

        • Geographic visualization

        • Damage concentration analysis

        • Priority zone identification
        """
    )


# ============================================================
# PRIORITY ASSESSMENT
# ============================================================

st.divider()

st.header("🚨 Priority Assessment")

priority_left, priority_right = st.columns([2, 1])

with priority_left:

    st.write(
        "EvoDamage combines damage severity and geographic "
        "concentration to highlight areas that may require "
        "closer inspection during preliminary disaster assessment."
    )

    st.progress(
        0.75,
        text="Priority analysis pipeline ready",
    )

with priority_right:

    st.metric(
        label="High Priority Zones",
        value="3",
    )

    st.metric(
        label="Assessment Status",
        value="Ready",
    )


# ============================================================
# QUICK ACCESS
# ============================================================

st.divider()

st.header("⚡ Quick Access")

quick1, quick2, quick3 = st.columns(3)

with quick1:

    if st.button(
        "🔍 Damage Assessment",
        use_container_width=True,
    ):

        st.switch_page(
            "pages/assessment.py"
        )


with quick2:

    if st.button(
        "🗺️ Damage Map",
        use_container_width=True,
    ):

        st.switch_page(
            "pages/damage_map.py"
        )


with quick3:

    if st.button(
        "🚨 Priority Analysis",
        use_container_width=True,
    ):

        st.switch_page(
            "pages/priority.py"
        )


# ============================================================
# PROTOTYPE NOTICE
# ============================================================

st.divider()

st.warning(
    "Prototype notice: EvoDamage provides preliminary disaster "
    "assessment and decision-support information. Results should "
    "be validated by qualified personnel before operational use."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<p class="footer-text">'
    'EvoDamage | AI • Computer Vision • GIS • Priority Analysis'
    '</p>',
    unsafe_allow_html=True,
)