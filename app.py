import streamlit as st
from pypdf import PdfReader, PdfWriter
from pdf2docx import Converter
from docx2pdf import convert
import os
import time

# --- 1. PAGE CONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="Mohana K - PDF Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. BEAUTY APP UI CUSTOMIZATION (MOBILE RESPONSIVE CSS) ---
st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #FFF5F5 0%, #FFD6D6 100%);
    }
    
    /* Metrics Dashboard Cards */
    div[data-testid="stMetricValue"] {
        background-color: white;
        padding: 15px 25px;
        border-radius: 20px;
        border: 1px solid #FFBABA;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        color: #FF4D4D !important;
        font-weight: bold;
    }
    
    /* Sidebar Aesthetics */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.9);
    }
    
    /* App-Like Gradient Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        border: none;
        height: 3.8em;
        background: linear-gradient(45deg, #FF758C, #FF7EB3);
        color: white;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 117, 140, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 117, 140, 0.6);
        color: white;
    }

    /* Mobile Header Centering */
    h1 {
        text-align: center;
        color: #FF4D4D;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def save_temp_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("# 🎀 Mohana K")
    st.markdown("Computer Science & Engineering")
    st.markdown("---")
    tool = st.radio("Choose Feature", 
        ["✨ Compress", "🔗 Merge", "✂️ Split", "📝 PDF to Word", "📘 Word to PDF"])
    st.markdown("---")
    st.caption("🔒 100% Offline & Private")

# --- 5. APP FEATURES ---

# MAIN TITLE
st.markdown("<h1>Mohana K PDF Pro</h1>", unsafe_allow_html=True)

# FEATURE: COMPRESS WITH MB METRICS
if tool == "✨ Compress":
    st.write("Optimize file size locally on your device.")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file:
        orig_mb = len(file.getvalue()) / (1024 * 1024)
        if st.button("Start Optimization"):
            with st.status("🪄 Compressing...") as status:
                reader = PdfReader(file)
                writer = PdfWriter()
                for page in reader.pages:
                    page.compress_content_streams()
                    writer.add_page(page)
                out_path = "optimized.pdf"
                with open(out_path, "wb") as f:
                    writer.write(f)
                status.update(label="Complete!", state="complete")
            
            final_mb = os.path.getsize(out_path) / (1024 * 1024)
            savings = ((orig_mb - final_mb) / orig_mb) * 100
            
            # Metric Dashboard
            st.markdown("### 📊 Space Savings")
            m1, m2, m3 = st.columns(3)
            m1.metric("Before", f"{orig_mb:.2f} MB")
            m2.metric("After", f"{final_mb:.2f} MB", f"-{savings:.1f}%")
            m3.metric("Saved", f"{orig_mb - final_mb:.2f} MB")
            
            with open(out_path, "rb") as f:
                st.download_button("📥 Download Optimized PDF", f, file_name="optimized.pdf")
            os.remove(out_path)

# FEATURE: MERGE
elif tool == "🔗 Merge":
    st.write("Combine multiple documents into one.")
    files = st.file_uploader("Select PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Merge Now") and files:
        if len(files) >= 2:
            writer = PdfWriter()
            for f in files: writer.append(f)
            out = "merged.pdf"
            writer.write(out)
            with open(out, "rb") as f:
                st.download_button("📥 Download Merged PDF", f, file_name="merged.pdf")
            os.remove(out)
        else:
            st.warning("Please upload at least 2 files.")

# FEATURE: SPLIT
elif tool == "✂️ Split":
    st.write("Extract specific pages from a document.")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file:
        reader = PdfReader(file)
        total = len(reader.pages)
        st.write(f"Total Pages: {total}")
        s, e = st.columns(2)
        start = s.number_input("Start Page", 1, total, 1)
        end = e.number_input("End Page", 1, total, total)
        if st.button("Extract Pages"):
            writer = PdfWriter()
            for i in range(start-1, end): writer.add_page(reader.pages[i])
            out = "split.pdf"
            writer.write(out)
            with open(out, "rb") as f:
                st.download_button("📥 Download Extracted PDF", f, file_name="split.pdf")
            os.remove(out)

# FEATURE: PDF TO WORD
elif tool == "📝 PDF to Word":
    st.write("Convert PDF back to editable DOCX.")
    file = st.file_uploader("Upload PDF", type="pdf")
    if st.button("Convert Now") and file:
        temp = save_temp_file(file)
        docx = temp.replace(".pdf", ".docx")
        with st.spinner("Analyzing layout..."):
            cv = Converter(temp)
            cv.convert(docx)
            cv.close()
        with open(docx, "rb") as f:
            st.download_button("📥 Download Word File", f, file_name=docx)
        os.remove(temp); os.remove(docx)

# FEATURE: WORD TO PDF (CLEAN - NO WATERMARK)
elif tool == "📘 Word to PDF":
    st.write("High-fidelity conversion using local system engine.")
    file = st.file_uploader("Upload Word (.docx)", type="docx")
    if st.button("Convert to PDF"):
        if file:
            temp_word = save_temp_file(file)
            pdf_out = temp_word.replace(".docx", ".pdf")
            try:
                with st.spinner("🚀 Processing..."):
                    # docx2pdf uses local MS Word engine to avoid watermarks
                    convert(temp_word, pdf_out)
                with open(pdf_out, "rb") as f:
                    st.download_button("📥 Download Clean PDF", f, file_name="converted.pdf")
                os.remove(temp_word); os.remove(pdf_out)
            except Exception as e:
                st.error("Please ensure Microsoft Word is installed for this feature.")