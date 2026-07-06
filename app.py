import streamlit as st
import time

# Configure the page aesthetics
st.set_page_config(
    page_title="Defect Analysis AI", 
    page_icon="🐛", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for a slightly more premium feel within Streamlit
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .main-header {
        text-align: center;
        background: -webkit-linear-gradient(#60a5fa, #4ade80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #9ca3af;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">Defect Analysis AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Submit bug reports, stack traces, or error logs for multi-agent analysis.</p>', unsafe_allow_html=True)

st.divider()

st.subheader("1. Describe the Bug")
bug_description = st.text_area(
    "Bug Description & Stack Trace", 
    height=200, 
    placeholder="Paste your bug report, stack trace, or error log here...",
    label_visibility="collapsed"
)

st.subheader("2. Or Upload a Log File")
uploaded_file = st.file_uploader("Upload .txt, .log, or .pdf files", type=["txt", "log", "pdf"], label_visibility="collapsed")

st.divider()

if st.button("Analyze Defect", type="primary"):
    if not bug_description and not uploaded_file:
        st.warning("⚠️ Please provide a bug description or upload a log file to analyze.")
    else:
        with st.spinner("Multi-Agent Orchestrator is analyzing the defect..."):
            # Mock delay to simulate agent processing and RAG retrieval
            time.sleep(2.5)
            st.success("✅ Analysis Complete!")
            
            # This is mock data for the prototype presentation
            st.markdown("### 🤖 Agent Findings")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Triage Agent**\n\nSeverity: High\n\nComponent: Database Layer")
            with col2:
                st.warning("**Duplicate Agent**\n\nFound 3 similar historical issues in the Vector DB.")
                
            st.error("**Root Cause Agent**\n\nThe stack trace indicates a Null Reference Exception occurred during the data fetching cycle.")
            st.success("**Remediation Agent**\n\nSuggested Fix: Add a null check before accessing the `.length` property on line 42.")
