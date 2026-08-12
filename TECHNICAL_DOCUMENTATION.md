# Technical Documentation

## 1. System Architecture
SmartBug Analyzer is built on a 5-agent orchestration model using the Google Gemini LLM API, Streamlit, and a Chroma vector database for Retrieval-Augmented Generation (RAG).

The system consists of the following components:
*   **Orchestrator Layer (`app.py`)**: A Streamlit application handling user inputs, file parsing, vector DB querying, and agent orchestration.
*   **Agent Logic (`src/agents.py`)**: Contains Pydantic models for structured output parsing, dynamic Gemini API endpoint validation, and individual agent prompts.
*   **Knowledge Base (`chroma_db/`)**: Local persistent vector database storing historical bug resolutions.

## 2. Agent Pipeline
1.  **Triage Agent**: Classifies priority, severity, and component based on the raw bug report.
2.  **Log Analysis Agent**: Parses raw stack traces and logs to pinpoint the exact code path failure.
3.  **Duplicate Detection Agent**: Performs semantic similarity searches on the `chroma_db` to find resolved bugs matching the current defect.
4.  **Root Cause Agent**: Cross-references the Log Analysis failure point against the Duplicate Detection historical summaries to hypothesize the root cause.
5.  **Remediation Agent**: Combines outputs from all 4 previous agents to generate highly specific, contextually grounded fixes.

## 3. Knowledge Base Growth Mechanism
When a bug is successfully resolved, users click the "Verify Fix & Add to Knowledge Base" button. The orchestrator embeds the bug report and the generated remediation step back into ChromaDB using HuggingFace `all-MiniLM-L6-v2` embeddings, ensuring future agents learn from the new resolution.

## 4. Defect Pattern Analytics
The analytics dashboard leverages the `DATASET.csv` file using Pandas. It computes macro-level trends over historical data, visually identifying vulnerable components and systemic spikes over time.

## 5. Local Setup
1.  Clone the repository.
2.  Install requirements: `pip install -r requirements.txt`. Ensure `numpy<2.0.0` is strictly installed to avoid ChromaDB compatibility errors.
3.  Add `DATASET.csv` to the root directory for automated validation and analytics.
4.  Run the application: `streamlit run app.py`.
5.  Enter a valid Google Gemini API Key in the UI sidebar.
