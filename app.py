import streamlit as st
import time

# Configure the page aesthetics
st.set_page_config(
    page_title="Defect Analysis AI", 
    page_icon="🐛", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Advanced Custom CSS for a Premium, Modern UI
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main Hero Header */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0px;
        padding-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }

    /* Input Areas Styling (Glassmorphism feel) */
    .stTextArea textarea {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        padding: 15px !important;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
    }

    /* File Uploader */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px dashed #475569 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #3b82f6 !important;
        background-color: rgba(30, 41, 59, 0.8) !important;
    }

    /* Primary Button Animation */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border: none;
        color: white;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        color: white !important;
    }
    .stButton>button:active {
        transform: translateY(0px);
    }

    /* Result Cards */
    .agent-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .agent-card:hover {
        transform: translateY(-2px);
        border-color: #475569;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    .agent-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .triage-color { color: #f43f5e; }
    .duplicate-color { color: #f59e0b; }
    .rootcause-color { color: #8b5cf6; }
    .remediation-color { color: #10b981; }
    
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown('<h1 class="main-header">SmartBug Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Multi-Agent Triage & Root Cause Analysis</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input Section
st.markdown("### 📝 Describe the Defect")
bug_description = st.text_area(
    "Bug Description", 
    height=150, 
    placeholder="Paste your bug report, stack trace, or error log here...",
    label_visibility="collapsed"
)

st.markdown("### 📎 Or Upload Log Files")
uploaded_file = st.file_uploader("Upload logs", type=["txt", "log", "pdf"], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Analyze Button
if st.button("🚀 Analyze Defect", type="primary"):
    if not bug_description and not uploaded_file:
        st.warning("⚠️ Please provide a bug description or upload a log file to analyze.")
    else:
        with st.spinner("AI Agents are analyzing the defect context..."):
            # Mock delay
            time.sleep(2)
            
        st.success("✨ Analysis Complete!")
        st.markdown("---")
        st.markdown("### 🧠 AI Agent Findings")
        
        # Display mock results using HTML for premium styling
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="agent-card">
                <div class="agent-title triage-color">🚨 Triage Agent</div>
                <strong>Severity:</strong> High<br>
                <strong>Component:</strong> Database Layer<br>
                <strong>Priority:</strong> P1
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="agent-card">
                <div class="agent-title rootcause-color">🔍 Root Cause Agent</div>
                The stack trace indicates a <code>NullReferenceException</code> occurred during the asynchronous data fetching cycle in the main worker thread.
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="agent-card">
                <div class="agent-title duplicate-color">📂 Duplicate Agent</div>
                Found <strong>3</strong> similar historical issues in the Knowledge Base:<br>
                <span style="color:#94a3b8;">• BUG-492: Fix db fetch crash</span><br>
                <span style="color:#94a3b8;">• BUG-112: Null exception in async worker</span><br>
                <span style="color:#94a3b8;">• BUG-88: Missing validation</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="agent-card">
                <div class="agent-title remediation-color">🛠️ Remediation Agent</div>
                <strong>Suggested Fix:</strong><br>
                Add an explicit null check before accessing the <code>.length</code> property on line 42 of <code>DataFetcher.java</code>.
            </div>
            """, unsafe_allow_html=True)
