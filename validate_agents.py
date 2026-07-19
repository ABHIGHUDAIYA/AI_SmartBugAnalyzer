import pandas as pd
import json
import sys
import time
import os

sys.path.append('src')
from agents import run_triage_agent, run_log_analysis_agent

def validate_agents(api_key: str, dataset_path: str, num_samples: int = 5):
    print(f"Loading dataset from {dataset_path}...")
    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Sample a few diverse bugs
    if len(df) > num_samples:
        df_sample = df.sample(num_samples, random_state=42)
    else:
        df_sample = df
        
    report = "# Agent Validation Report\n\n"
    report += "This report validates the accuracy of the Triage and Log Analysis AI agents against real historical bugs from our seeded dataset.\n\n"

    print(f"Validating {len(df_sample)} samples...")

    for index, row in df_sample.iterrows():
        bug_id = row.get('bug_id', 'Unknown')
        short_desc = str(row.get('short_description', ''))
        long_desc = str(row.get('long_description', ''))
        
        # We will use short description as the bug report for Triage
        # And long description as the stack trace/error log for Log Analysis
        
        print(f"Processing Bug ID: {bug_id}...")
        
        # Run Triage Agent
        triage_res = run_triage_agent(api_key, short_desc)
        
        # Run Log Analysis Agent
        log_res = run_log_analysis_agent(api_key, long_desc, "")
        
        report += f"## Bug ID: {bug_id}\n"
        report += f"**Original Summary:** {short_desc}\n\n"
        
        report += "### 🚨 Triage Agent Output\n"
        report += f"- **Severity:** {triage_res.severity}\n"
        report += f"- **Priority:** {triage_res.priority}\n"
        report += f"- **Component:** {triage_res.component}\n"
        report += f"- **Confidence:** {triage_res.confidence * 100:.0f}%\n"
        report += f"- **Reasoning:** {triage_res.reasoning}\n\n"
        
        report += "### 🔍 Log Analysis Agent Output\n"
        report += f"- **Exception Type:** {log_res.exception_type}\n"
        report += f"- **Failure Point:** {log_res.failure_point}\n"
        report += f"- **Code Path:** {log_res.code_path}\n"
        report += f"- **Suggested Fix / Investigation:** {log_res.suggested_investigation}\n\n"
        
        report += "---\n\n"
        
        # Sleep for a bit to avoid hitting API rate limits
        time.sleep(2)

    with open("validation_report.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print("Validation complete! Results saved to validation_report.md")

if __name__ == "__main__":
    # PASTE YOUR GOOGLE GEMINI API KEY HERE BEFORE RUNNING
    # (Remember to remove it before pushing to GitHub!)
    API_KEY = "YOUR_API_KEY_HERE"
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Please open validate_agents.py, paste your API key into the API_KEY variable at the bottom of the file, and save before running!")
        sys.exit(1)
        
    validate_agents(api_key=API_KEY, dataset_path="DATASET.csv", num_samples=5)
