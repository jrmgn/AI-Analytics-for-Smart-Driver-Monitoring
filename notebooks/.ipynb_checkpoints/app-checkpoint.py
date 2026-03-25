import streamlit as st
import pandas as pd
from textblob import TextBlob
import cv2
import pytesseract
import numpy as np
import re

# Configure Tesseract Path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Smart Fleet Analytics", layout="wide")
st.title("🚖 Smart Driver Monitoring & Safety System")

# --- TAB NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Driver Analytics", "💬 Feedback Sentiment", "🛡️ Forgery Detection"])

# --- TAB 1: TELEMETRY ---
with tab1:
    st.header("Driver Performance Overview")
    try:
        df = pd.read_csv(r"C:\Users\JERMAGNE\data\data\driver_stats_summary.csv")
        st.dataframe(df.style.highlight_max(axis=0, subset=['risk_score'], color='pink'))
        st.bar_chart(df.set_index('driver_id')['avg_rating'])
    except:
        st.warning("Please run your previous notebooks to generate driver_stats_summary.csv first!")

# --- TAB 2: SENTIMENT ---
with tab2:
    st.header("Passenger Feedback Analyzer")
    user_input = st.text_area("Enter passenger comments:", placeholder="e.g., The driver was speeding...")
    
    if st.button("Analyze Sentiment"):
        if user_input.strip() == "":
            st.warning("Please enter some text first!")
        else:
            # Get the numerical polarity score
            score = TextBlob(user_input).sentiment.polarity
            
            # Logic: Using a 'Neutral' buffer between -0.1 and 0.1
            if score > 0.3:
                st.success(f"Result: POSITIVE (Score: {score:.2f})")
            elif score < -0.1:
                st.error(f"Result: NEGATIVE (Score: {score:.2f})")
            else:
                # Now a 0.20 score will fall here
                st.info(f"Result: NEUTRAL / NEEDS REVIEW (Score: {score:.2f})")

# --- TAB 3: OCR ---
with tab3:
    st.header("License Verification")
    uploaded_image = st.file_uploader("Upload License Scan", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_image:
        # Convert the file to an image
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        st.image(img, channels="BGR", width=400)
        
        # 1. Extract Text using OCR
        # We use --psm 6 which assumes a single uniform block of text
        text = pytesseract.image_to_string(img, config=r'--oem 3 --psm 6').upper()
        
        # 2. Define Validation Rules
        # Pattern looks for 3 chars, a separator, then 4 digits (e.g., ABC-1234)
        id_pattern = r'[A-Z0-9]{3}.{1,2}\d{4}'
        has_id = re.search(id_pattern, text)
        
        # Check for specific company/document keywords
        has_header = "DRIVER" in text and "LICENSE" in text
        
        # 3. Final Validation Logic
        if has_id and has_header:
            st.success("✅ License Format Validated")
            st.info(f"Detected ID: {has_id.group()}")
        elif has_id and not has_header:
            st.warning("⚠️ ID Pattern found, but 'DRIVER LICENSE' header is missing. Please check document type.")
        else:
            st.error("❌ Potential Forgery Detected: No valid License ID format found.")
            
        # Optional: Show what the AI "sees" for debugging
        with st.expander("View Raw OCR Text"):
            st.write(text)