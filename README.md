# SmartBug Analyzer

An AI-powered Multi-Agent Triage & Root Cause Analysis system designed to automate software bug management.

## Architecture

This system leverages a multi-agent AI architecture to process bug reports in real-time:
1. **Triage Agent**: Analyzes defect descriptions to determine priority, severity, and assigned component.
2. **Log Analysis Agent**: Parses stack traces to pinpoint the exact file, line number, and root cause.
3. **Duplicate Agent**: Utilizes ChromaDB vector search to find similar historical bugs.
4. **Remediation Agent**: Synthesizes the output to recommend actionable code fixes.

## Features
- **Manual Analysis**: Interactive dashboard for submitting individual bug reports.
- **Automated Validation Suite**: High-throughput automated batch testing engine against seeded datasets.
- **Modern UI**: Sleek, fully responsive Streamlit interface with a custom glassmorphism design system.

## Installation

1. Clone the repository:
   ```bash
   git clone <https://github.com/ABHIGHUDAIYA/AI_SmartBugAnalyzer.git>
   cd AI_SmartBugAnalyzer
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\Activate.ps1
   # On Mac/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Configuration
Requires a Google Gemini API Key. You can configure this directly via the secure sidebar inside the Streamlit UI.

## License
MIT License.
