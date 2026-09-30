import streamlit as st

st.title("🔍 Damage Assessment")

st.write(
    "Upload pre-disaster and post-disaster images "
    "to assess building damage using AI."
)

st.divider()

# Image Upload Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Pre-Disaster Image")

    before_image = st.file_uploader(
        "Upload pre-disaster image",
        type=["jpg", "jpeg", "png"],
        key="before_image"
    )

with col2:
    st.subheader("📷 Post-Disaster Image")

    after_image = st.file_uploader(
        "Upload post-disaster image",
        type=["jpg", "jpeg", "png"],
        key="after_image"
    )

# Display uploaded images
if before_image or after_image:
    st.divider()
    st.subheader("Uploaded Images")

    image_col1, image_col2 = st.columns(2)

    with image_col1:
        if before_image:
            st.image(
                before_image,
                caption="Pre-Disaster",
                use_container_width=True
            )

    with image_col2:
        if after_image:
            st.image(
                after_image,
                caption="Post-Disaster",
                use_container_width=True
            )

# Analysis Section
st.divider()

if st.button("🚀 Analyze Damage", type="primary", use_container_width=True):

    if before_image is None or after_image is None:

        st.warning(
            "Please upload both pre-disaster and post-disaster images."
        )

    else:

        st.success("Both images uploaded successfully!")

        st.subheader("🤖 AI Assessment")

        st.info(
            "The AI damage classification model will be connected here."
        )