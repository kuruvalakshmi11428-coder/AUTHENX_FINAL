import io

import streamlit as st
import pytesseract
from PIL import Image


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AUTHENX | Identity Risk Screening",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            background-color: #f8fafc;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .section-box {
            background-color: white;
            padding: 20px;
            border-radius: 14px;
            border: 1px solid #e2e8f0;
            margin-bottom: 20px;
        }

        .small-text {
            color: #64748b;
            font-size: 14px;
        }

        .risk-box {
            background-color: #fff7ed;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #fed7aa;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def read_uploaded_image(uploaded_file):
    """
    Safely reads an uploaded image from Streamlit.
    """

    if uploaded_file is None:
        return None

    file_bytes = uploaded_file.getvalue()

    if not file_bytes:
        raise ValueError("The uploaded file is empty.")

    image = Image.open(io.BytesIO(file_bytes))

    # Force image loading and convert to RGB
    image.load()

    return image.convert("RGB")


def extract_text_from_image(image):
    """
    Extracts text from an image using Tesseract OCR.
    """

    if image is None:
        return ""

    extracted_text = pytesseract.image_to_string(image)

    return extracted_text


def calculate_risk_score(text_a, text_b):
    """
    Basic explainable rule-based risk scoring.

    This is only a prototype scoring method.
    """

    score = 0
    reasons = []

    if not text_a.strip():
        score += 25
        reasons.append("Document A text could not be extracted.")

    if not text_b.strip():
        score += 25
        reasons.append("Document B text could not be extracted.")

    if text_a.strip() and text_b.strip():
        score += 10
        reasons.append("Both documents contain readable text.")

        words_a = set(text_a.lower().split())
        words_b = set(text_b.lower().split())

        common_words = words_a.intersection(words_b)

        if len(common_words) < 3:
            score += 30
            reasons.append(
                "Very few common words were found between the documents."
            )
        else:
            reasons.append(
                "Some common words were found between the documents."
            )

    if score >= 60:
        risk_level = "High Risk"
    elif score >= 30:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return score, risk_level, reasons


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.header("AUTHENX Controls")

    st.write("Prototype configuration")

    screening_mode = st.selectbox(
        "Screening Mode",
        [
            "Identity Document Screening",
            "Cross-Document Consistency",
            "Explainable Risk Analysis"
        ]
    )

    st.divider()

    st.write("Supported file types:")
    st.write("- PNG")
    st.write("- JPG")
    st.write("- JPEG")

    st.divider()

    st.info(
        "Use only synthetic or dummy documents for this prototype. "
        "Do not upload real Aadhaar cards or sensitive personal documents."
    )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🛡️ AUTHENX")

st.subheader(
    "Beyond Fake or Real: Explainable Identity Risk Investigation"
)

st.write(
    "AUTHENX analyzes identity documents using OCR, "
    "cross-document comparison, and explainable risk rules."
)

st.caption("SIH26188 | Identity and Document Screening Prototype")

st.warning(
    "Prototype limitation: This version uses OCR and rule-based checks. "
    "It does not claim trained AI tamper detection, face matching, "
    "or certified document authenticity."
)


# ---------------------------------------------------------
# TOP METRICS
# ---------------------------------------------------------

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Documents", "2")

with metric_col2:
    st.metric("OCR Engine", "Tesseract")

with metric_col3:
    st.metric("Analysis Type", "Rule-Based")

with metric_col4:
    st.metric("Output", "Explainable")


st.divider()


# ---------------------------------------------------------
# SCREENING MODE
# ---------------------------------------------------------

st.header("1. Screening Configuration")

st.write(f"Current screening mode: **{screening_mode}**")


# ---------------------------------------------------------
# DOCUMENT UPLOAD SECTION
# ---------------------------------------------------------

st.header("2. Upload Identity Documents")

upload_col1, upload_col2 = st.columns(2)

with upload_col1:
    st.subheader("📄 Document A")

    uploaded_a = st.file_uploader(
        "Upload first document",
        type=["png", "jpg", "jpeg"],
        key="document_a"
    )

with upload_col2:
    st.subheader("📄 Document B")

    uploaded_b = st.file_uploader(
        "Upload second document",
        type=["png", "jpg", "jpeg"],
        key="document_b"
    )


# ---------------------------------------------------------
# IMAGE PREVIEW SECTION
# ---------------------------------------------------------

st.header("3. Evidence Workspace")

image_col1, image_col2 = st.columns(2)

image_a = None
image_b = None

with image_col1:
    if uploaded_a is not None:
        try:
            image_a = read_uploaded_image(uploaded_a)

            st.image(
                image_a,
                caption="Document A Preview",
                use_container_width=True
            )

            st.success("Document A loaded successfully.")

        except Exception as error:
            st.error(f"Could not read Document A: {error}")

    else:
        st.info("Upload Document A to preview it.")


with image_col2:
    if uploaded_b is not None:
        try:
            image_b = read_uploaded_image(uploaded_b)

            st.image(
                image_b,
                caption="Document B Preview",
                use_container_width=True
            )

            st.success("Document B loaded successfully.")

        except Exception as error:
            st.error(f"Could not read Document B: {error}")

    else:
        st.info("Upload Document B to preview it.")


# ---------------------------------------------------------
# OCR SECTION
# ---------------------------------------------------------

st.header("4. OCR Text Extraction")

if "text_a" not in st.session_state:
    st.session_state.text_a = ""

if "text_b" not in st.session_state:
    st.session_state.text_b = ""


if st.button("🔍 Extract Text from Documents", use_container_width=True):

    if image_a is None or image_b is None:
        st.error("Please upload both documents before extracting text.")

    else:
        with st.spinner("Extracting text using OCR..."):

            try:
                st.session_state.text_a = extract_text_from_image(image_a)
                st.session_state.text_b = extract_text_from_image(image_b)

                st.success("OCR extraction completed successfully.")

            except Exception as error:
                st.error(f"OCR extraction failed: {error}")


# ---------------------------------------------------------
# OCR RESULTS
# ---------------------------------------------------------

result_col1, result_col2 = st.columns(2)

with result_col1:
    st.subheader("Extracted Text - Document A")

    if st.session_state.text_a.strip():
        st.text_area(
            "Document A OCR Output",
            st.session_state.text_a,
            height=250
        )
    else:
        st.info("No OCR text available for Document A.")


with result_col2:
    st.subheader("Extracted Text - Document B")

    if st.session_state.text_b.strip():
        st.text_area(
            "Document B OCR Output",
            st.session_state.text_b,
            height=250
        )
    else:
        st.info("No OCR text available for Document B.")


# ---------------------------------------------------------
# RISK ANALYSIS SECTION
# ---------------------------------------------------------

st.header("5. Explainable Risk Analysis")

if st.button("⚖️ Analyze Identity Risk", use_container_width=True):

    if not st.session_state.text_a.strip():
        st.error("Please extract text from Document A first.")

    elif not st.session_state.text_b.strip():
        st.error("Please extract text from Document B first.")

    else:
        risk_score, risk_level, risk_reasons = calculate_risk_score(
            st.session_state.text_a,
            st.session_state.text_b
        )

        st.subheader("Risk Result")

        risk_col1, risk_col2 = st.columns(2)

        with risk_col1:
            st.metric("Risk Score", f"{risk_score}/100")

        with risk_col2:
            st.metric("Risk Level", risk_level)

        if risk_level == "High Risk":
            st.error("High-risk indicators detected.")

        elif risk_level == "Medium Risk":
            st.warning("Manual review is recommended.")

        else:
            st.success("Low-risk indicators detected.")

        st.subheader("Explanation")

        for reason in risk_reasons:
            st.write(f"• {reason}")


# ---------------------------------------------------------
# WORKFLOW SECTION
# ---------------------------------------------------------

st.header("6. AUTHENX Workflow")

workflow_col1, workflow_col2, workflow_col3, workflow_col4 = st.columns(4)

with workflow_col1:
    st.subheader("Step 1")
    st.write("Upload")
    st.caption("Upload two identity document images.")

with workflow_col2:
    st.subheader("Step 2")
    st.write("Extract")
    st.caption("Read document text using OCR.")

with workflow_col3:
    st.subheader("Step 3")
    st.write("Compare")
    st.caption("Compare extracted information.")

with workflow_col4:
    st.subheader("Step 4")
    st.write("Explain")
    st.caption("Display risk score and reasons.")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "AUTHENX is an academic prototype for SIH26188. "
    "It supports explainable screening and should not be treated "
    "as a legally certified identity verification system."
)