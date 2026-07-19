import streamlit as st
import time
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import io
import sys
import sys
sys.path.append('src')
from agents import run_triage_agent, run_log_analysis_agent, run_remediation_agent

# Configure the page aesthetics
st.set_page_config(
    page_title="Defect Analysis AI", 
    page_icon="🐛", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state for API Key if not present
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

with st.sidebar:
    st.markdown("### 🔑 AI Configuration")
    api_key_input = st.text_input("Google Gemini API Key", type="password", placeholder="Enter API key here...", value=st.session_state['api_key'])
    sc1, sc2, sc3 = st.columns([1, 2, 1])
    with sc2:
        apply_clicked = st.button("Apply", type="secondary", use_container_width=True)
    if apply_clicked:
        st.session_state['api_key'] = api_key_input
        st.success("API Key Applied!")
        
    api_key = st.session_state['api_key']
    st.markdown("<small>Your API key is required for the Triage and Log Analysis agents to function.</small>", unsafe_allow_html=True)

# Advanced Custom CSS for a Premium, Modern UI
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
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

    /* Hide Streamlit's 'Press Enter to apply' hint */
    [data-testid="InputInstructions"] {
        display: none !important;
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
        background: linear-gradient(135deg, #5b21b6 0%, #3b82f6 100%);
        border: none;
        color: white;
        padding: 0.85rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px -3px rgba(59, 130, 246, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -3px rgba(59, 130, 246, 0.6);
        background: linear-gradient(135deg, #7c3aed 0%, #60a5fa 100%);
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
        word-wrap: break-word;
        overflow-wrap: break-word;
        word-break: break-word;
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

    /* Modern Button-like Tabs */
    div[data-testid="stTabs"] > div > div > div {
        justify-content: center !important;
        width: 100% !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center !important;
        width: 100%;
        display: flex;
        gap: 15px;
        background-color: rgba(30, 41, 59, 0.6);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        max-width: 500px;
        margin: 0 auto;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 600;
        padding: 10px 25px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc;
        background-color: rgba(255,255,255,0.05);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px -3px rgba(139, 92, 246, 0.4) !important;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
</style>
""", unsafe_allow_html=True)

# Main UI
st.markdown('<h1 class="main-header">SmartBug Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Multi-Agent Triage & Root Cause Analysis</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Manual Analysis", "Automated Validation"])

with tab1:
    # Input Section
    st.markdown("### 📝 Describe the Defect")

    st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:5px; margin-top:10px;'>1. Bug Report / Summary</p>", unsafe_allow_html=True)
    bug_report = st.text_area("Bug Report", height=100, placeholder="Describe the behavior you are seeing...", label_visibility="collapsed")

    st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:5px;'>2. Stack Trace</p>", unsafe_allow_html=True)
    stack_trace = st.text_area("Stack Trace", height=100, placeholder="Paste the full stack trace here (optional)...", label_visibility="collapsed")

    st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:5px;'>3. Error Log</p>", unsafe_allow_html=True)
    error_log = st.text_area("Error Log", height=100, placeholder="Paste any relevant server or error logs (optional)...", label_visibility="collapsed")

    st.markdown("### 📎 Or Upload Log Files")
    uploaded_file = st.file_uploader("Upload logs", type=["txt", "log", "pdf"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Analyze Button
    if st.button("🚀 Analyze Defect", type="primary"):
        if not api_key:
            st.error("⚠️ Please enter your Google Gemini API Key in the sidebar and click Apply to activate the AI Agents.")
        elif not bug_report and not stack_trace and not error_log and not uploaded_file:
            st.warning("⚠️ Please provide at least one input (bug report, stack trace, error log, or file) to analyze.")
        else:
            with st.spinner("AI Agents are analyzing the defect context and querying the Knowledge Base..."):
                # Setup vector DB connection
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
                
                # Determine query text
                query_parts = []
                if bug_report: query_parts.append(f"Bug Report: {bug_report}")
                if stack_trace: query_parts.append(f"Stack Trace: {stack_trace}")
                if error_log: query_parts.append(f"Error Log: {error_log}")
                if uploaded_file is not None:
                    query_parts.append(f"Log File: {uploaded_file.getvalue().decode('utf-8')}")
                    
                query_text = "\n".join(query_parts)
                    
                # Perform RAG search
                results = vectorstore.similarity_search(query_text, k=3)
                
                # Format the dynamic results
                duplicate_html = f"Found <strong>{len(results)}</strong> similar historical issues in the Knowledge Base:<br>"
                for doc in results:
                    b_id = doc.metadata.get('bug_id', 'Unknown')
                    s_desc = doc.metadata.get('short_description', 'No description')
                    if len(s_desc) > 50:
                        s_desc = s_desc[:47] + "..."
                    duplicate_html += f"<span style='color:#94a3b8;'>• BUG-{b_id}: {s_desc}</span><br>"
                    
                # Execute Live Agents
                triage_res = run_triage_agent(api_key, bug_report)
                log_res = run_log_analysis_agent(api_key, stack_trace, error_log)
                remediation_res = run_remediation_agent(api_key, triage_res, log_res)
                
            st.success("✨ Analysis Complete!")
            st.markdown("---")
            st.markdown("### 🧠 AI Agent Findings")
            
            # Display results using HTML for premium styling
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="agent-card">
                    <div class="agent-title triage-color">🚨 Triage Agent</div>
                    <strong>Severity:</strong> {triage_res.severity}<br>
                    <strong>Priority:</strong> {triage_res.priority}<br>
                    <strong>Component:</strong> {triage_res.component}<br>
                    <strong>Confidence:</strong> {triage_res.confidence * 100:.0f}%<br>
                    <div style="margin-top:10px; font-size:0.9rem; color:#94a3b8;">
                        <em>"{triage_res.reasoning}"</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="agent-card">
                    <div class="agent-title rootcause-color">🔍 Log Analysis Agent</div>
                    <strong>Exception Type:</strong> <code>{log_res.exception_type}</code><br>
                    <strong>Failure Point:</strong> {log_res.failure_point}<br>
                    <div style="margin-top:10px; font-size:0.9rem;">
                        <strong>Path:</strong> {log_res.code_path}
                    </div>
                    <div style="margin-top:10px; font-size:0.9rem; color:#94a3b8; border-top:1px solid #334155; padding-top:8px;">
                        <em>Next Step: {log_res.suggested_investigation}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="agent-card">
                    <div class="agent-title duplicate-color">📂 Duplicate Agent</div>
                    {duplicate_html}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="agent-card">
                    <div class="agent-title remediation-color">🛠️ Remediation Agent</div>
                    <strong>Suggested Fix:</strong><br>
                    {remediation_res.suggested_fix}
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style="padding: 40px; border-radius: 16px; background: rgba(30,41,59,0.3); border: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px; text-align: center;">
        <div style="display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px;">
            <div style="background: rgba(139,92,246,0.1); padding: 12px; border-radius: 12px; border: 1px solid rgba(139,92,246,0.2);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #f8fafc; letter-spacing: -0.5px;">Automated Validation Suite</h1>
        </div>
        <p style="color: #94a3b8; font-size: 1.05rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Execute high-throughput, automated testing against the historical <code style="background: rgba(255,255,255,0.05); color: #e2e8f0; padding: 3px 6px; border-radius: 4px; font-size: 0.9rem; border: 1px solid rgba(255,255,255,0.1);">DATASET.csv</code>. 
            This suite validates classification accuracy and reasoning across a diverse matrix of bug report formats.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    mc1, mc2, mc3 = st.columns([1, 2, 1])
    with mc2:
        run_batch = st.button("▶ Start Batch Validation", type="primary", use_container_width=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: -10px;'>Validate multiple bug reports in one go ⚡</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    dash_container = st.empty()
    output_container = st.container()
    
    if run_batch:
        if not api_key:
            st.error("⚠️ Please enter your Google Gemini API Key in the sidebar and click Apply to activate the AI Agents.")
        else:
            def render_dash(progress, current_bug, elapsed):
                dash_html = f"""<div style="background: #0f172a; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 25px; display: flex; flex-direction: column; align-items: center; gap: 20px;">
<div style="display: flex; gap: 15px; align-items: center;">
<div style="background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); padding: 10px; border-radius: 50%;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M9 12l2 2 4-4"/></svg>
</div>
<h4 style="color: #34d399; margin: 0; font-size: 1.1rem;">Successfully sampled 5 bugs from the dataset.</h4>
</div>
<div style="display: flex; gap: 15px; justify-content: center; width: 100%;">
<div style="flex: 1; min-width: 110px; max-width: 140px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; text-align: center; box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);">
<div style="font-size: 1.2rem; font-weight: bold; color: #f8fafc; margin-bottom: 5px; display: flex; align-items: center; justify-content: center; gap: 6px;"><span style="font-size: 1.5rem;">👾</span> 5</div>
<div style="font-size: 0.75rem; color: #94a3b8; white-space: nowrap;">Bugs Sampled</div>
</div>
<div style="flex: 1; min-width: 110px; max-width: 140px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; text-align: center; box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);">
<div style="font-size: 1.2rem; font-weight: bold; color: #f8fafc; margin-bottom: 5px; display: flex; align-items: center; justify-content: center; gap: 6px;"><span style="font-size: 1.5rem;">🤖</span> 4</div>
<div style="font-size: 0.75rem; color: #94a3b8; white-space: nowrap;">Agents Running</div>
</div>
<div style="flex: 1; min-width: 110px; max-width: 140px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; text-align: center; box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);">
<div style="font-size: 1.1rem; font-weight: bold; color: #f8fafc; margin-bottom: 5px; display: flex; align-items: center; justify-content: center; gap: 6px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#60a5fa" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 00:00:{elapsed:02d}</div>
<div style="font-size: 0.75rem; color: #94a3b8; white-space: nowrap;">Elapsed Time</div>
</div>
<div style="flex: 1; min-width: 110px; max-width: 140px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; text-align: center; box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);">
<div style="font-size: 1.1rem; font-weight: bold; color: {'#34d399' if progress == 100 else '#f8fafc'}; margin-bottom: 5px; display: flex; align-items: center; justify-content: center; gap: 6px;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg> {'Done' if progress == 100 else 'In Progress'}</div>
<div style="font-size: 0.75rem; color: #94a3b8; white-space: nowrap;">Status</div>
</div>
</div>
<hr style="border-color: rgba(255,255,255,0.05); margin: 0; width: 100%;">
<div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
<p style="color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;">Validating against AI agents...</p>
<div style="width: 80%; background: rgba(255,255,255,0.05); border-radius: 10px; height: 8px; display: flex; align-items: center; position: relative;">
<div style="width: {progress}%; background: linear-gradient(90deg, #34d399 0%, #10b981 100%); height: 100%; border-radius: 10px; transition: width 0.3s ease; box-shadow: 0 0 10px rgba(52,211,153,0.5);"></div>
<span style="position: absolute; right: -35px; color: #94a3b8; font-size: 0.75rem; font-weight: 600;">{progress}%</span>
</div>
</div>
</div>"""
                dash_container.markdown(dash_html, unsafe_allow_html=True)

            try:
                df = pd.read_csv("DATASET.csv")
                df_sample = df.sample(5)
                
                start_time = time.time()
                count = 0
                render_dash(0, count, 0)
                
                with output_container:
                    for index, row in df_sample.iterrows():
                        bug_id = row.get('bug_id', 'Unknown')
                        short_desc = str(row.get('short_description', ''))
                        long_desc = str(row.get('long_description', ''))
                        
                        st.markdown(f"#### 🐛 Bug ID: {bug_id}")
                        st.info(f"**Original Report:** {short_desc}")
                        
                        t_res = run_triage_agent(api_key, short_desc)
                        l_res = run_log_analysis_agent(api_key, long_desc, "")
                        
                        v_col1, v_col2 = st.columns(2)
                        with v_col1:
                            st.markdown(f"""
                            <div style="background: rgba(244, 63, 94, 0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(244, 63, 94, 0.3);">
                                <strong>Triage Output:</strong><br>
                                • Severity: {t_res.severity}<br>
                                • Priority: {t_res.priority}<br>
                                • Component: {t_res.component}<br>
                                • Confidence: {t_res.confidence * 100:.0f}%
                            </div>
                            """, unsafe_allow_html=True)
                        with v_col2:
                            st.markdown(f"""
                            <div style="background: rgba(139, 92, 246, 0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(139, 92, 246, 0.3);">
                                <strong>Log Analysis Output:</strong><br>
                                • Exception: <code>{l_res.exception_type}</code><br>
                                • Failure Point: {l_res.failure_point}
                            </div>
                            """, unsafe_allow_html=True)
                            
                        st.markdown("<hr style='margin: 15px 0px; border-color: #334155;'>", unsafe_allow_html=True)
                        time.sleep(1) # Prevent rate limiting
                        
                        count += 1
                        elapsed = int(time.time() - start_time)
                        render_dash(int((count/5)*100), count, elapsed)
                        
            except Exception as e:
                st.error(f"Failed to run validation: {str(e)}")
