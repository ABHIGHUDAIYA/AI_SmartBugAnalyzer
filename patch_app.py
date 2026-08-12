import os

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Insert add_to_kb callback
callback_code = '''
def add_to_kb(query_text, new_bug_id, short_desc, new_resolution):
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
        vectorstore.add_texts(
            texts=[query_text],
            metadatas=[{
                "bug_id": new_bug_id,
                "short_description": short_desc,
                "resolution_metadata": new_resolution
            }]
        )
        import streamlit as st
        st.session_state['kb_success_msg'] = f"Successfully added BUG {new_bug_id} to the Chroma Knowledge Base! Future agents will now learn from this resolution."
    except Exception as e:
        import streamlit as st
        st.session_state['kb_error_msg'] = str(e)

# Main UI
'''
content = content.replace("# Main UI\n", callback_code)

# 2. Add kb_success_msg check at top of UI
kb_check_code = '''st.markdown('<p class="sub-header">AI-Powered Multi-Agent Triage & Root Cause Analysis</p>', unsafe_allow_html=True)

if 'kb_success_msg' in st.session_state:
    st.success(st.session_state['kb_success_msg'])
    del st.session_state['kb_success_msg']
if 'kb_error_msg' in st.session_state:
    st.error(st.session_state['kb_error_msg'])
    del st.session_state['kb_error_msg']
'''
content = content.replace("st.markdown('<p class=\"sub-header\">AI-Powered Multi-Agent Triage & Root Cause Analysis</p>', unsafe_allow_html=True)", kb_check_code)

# 3. Add tab3
content = content.replace('tab1, tab2 = st.tabs(["Manual Analysis", "Automated Validation"])', 'tab1, tab2, tab3 = st.tabs(["Manual Analysis", "Automated Validation", "Defect Pattern Analytics"])')

# 4. Add the KB button logic at the bottom of tab1
kb_button_code = '''            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 30px 0px; border-color: #334155;'>", unsafe_allow_html=True)
            st.markdown("### 🌱 Knowledge Base Growth")
            st.info("If you have verified that the Remediation Agent's fix successfully resolves this bug, add it back to the knowledge base to improve future AI retrieval accuracy!")
            
            import time
            new_bug_id = f"KB-ADDED-{int(time.time())}"
            short_desc = bug_report[:100] + "..." if bug_report else "Uploaded log analysis"
            new_resolution = f"Root Cause Hypothesis: {root_cause_res.cause_hypothesis}\\nResolution: {remediation_res.suggested_fix}"
            
            st.button("✅ Verify Fix & Add to Knowledge Base", type="primary", use_container_width=True, on_click=add_to_kb, args=(query_text, new_bug_id, short_desc, new_resolution))

with tab2:'''
content = content.replace('            </div>\n            """, unsafe_allow_html=True)\n\nwith tab2:', kb_button_code)

# 5. Append tab3 content to the very end
tab3_content = '''
with tab3:
    st.markdown("""
    <div style="padding: 40px; border-radius: 16px; background: rgba(30,41,59,0.3); border: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px; text-align: center;">
        <div style="display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px;">
            <div style="background: rgba(59,130,246,0.1); padding: 12px; border-radius: 12px; border: 1px solid rgba(59,130,246,0.2);">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg>
            </div>
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #f8fafc; letter-spacing: -0.5px;">Defect Pattern Analytics</h1>
        </div>
        <p style="color: #94a3b8; font-size: 1.05rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">
            Discover macro trends, recurring themes, and system vulnerabilities across the historical <strong>DATASET.csv</strong>. 
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        import pandas as pd
        @st.cache_data
        def load_analytics_data():
            df = pd.read_csv("DATASET.csv", usecols=['bug_id', 'component_name', 'severity_category', 'resolution_category', 'creation_date'])
            df['creation_date'] = pd.to_datetime(df['creation_date'], errors='coerce')
            return df

        df_analytics = load_analytics_data()
        
        st.markdown("### 📊 High-Frequency Affected Components")
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>The subsystems most prone to defects across the historical database.</p>", unsafe_allow_html=True)
        top_components = df_analytics['component_name'].value_counts().head(10)
        st.bar_chart(top_components, color="#3b82f6")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🚨 Severity Distribution")
            st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>Distribution of critical vs normal bugs.</p>", unsafe_allow_html=True)
            severity_counts = df_analytics['severity_category'].value_counts()
            st.bar_chart(severity_counts, color="#f43f5e")
            
        with c2:
            st.markdown("### 🛠️ Resolution Trends")
            st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>How historical bugs were eventually categorized.</p>", unsafe_allow_html=True)
            resolution_counts = df_analytics['resolution_category'].value_counts()
            st.bar_chart(resolution_counts, color="#10b981")
            
        st.markdown("### 📈 Defect Volume Over Time (2000 - Present)")
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>Yearly distribution of bug reports to identify systemic spikes.</p>", unsafe_allow_html=True)
        df_analytics['year'] = df_analytics['creation_date'].dt.year
        yearly_counts = df_analytics.groupby('year').size()
        yearly_counts = yearly_counts[(yearly_counts.index >= 2000) & (yearly_counts.index <= 2026)]
        st.line_chart(yearly_counts, color="#8b5cf6")
        
    except Exception as e:
        st.error(f"Failed to load analytics data: {str(e)}")
'''
content += tab3_content

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS")
