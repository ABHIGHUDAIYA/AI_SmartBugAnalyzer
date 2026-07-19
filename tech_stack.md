# Project Technology Stack

The following technologies and frameworks were used to build the complete Defect Analysis AI System.

## 1. User Interface
*   **Streamlit (Python)**: Used to build the entire web interface. It provides a simple and fast way to create interactive forms and file uploaders using pure Python.
*   **Custom CSS (Glassmorphism)**: Advanced CSS injections into Streamlit to create a modern, pill-toggle UI with gradient buttons and sleek dashboard animations.

## 2. Data Processing
*   **Pandas (Python)**: Used to load, clean, and manipulate the raw CSV datasets containing the historical bug reports.

## 3. Knowledge Base & Search (RAG Pipeline)
*   **ChromaDB**: An open-source Vector Database used to store the historical bug reports and perform fast similarity searches.
*   **HuggingFace (`sentence-transformers`)**: Open-source AI embedding models used to convert text (bug reports) into vector numbers.
*   **LangChain Text Splitters**: Used to split very long stack traces and bug reports into smaller chunks before saving them to the database.

## 4. AI Orchestration & Generation
*   **LangChain**: The primary Python framework used to connect the AI models, manage prompt templates, and orchestrate the interactions with the Vector Database.
*   **Google Gemini API**: Powers the Large Language Model reasoning behind the Triage, Log Analysis, and Remediation agents using the `gemini-1.5-pro` model.
