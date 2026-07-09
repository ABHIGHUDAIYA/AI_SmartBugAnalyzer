# 🐛 AI SmartBugAnalyzer

An AI-powered defect analysis tool that uses a RAG pipeline and multi-agent orchestration to automatically triage bug reports and detect duplicates.

## 📌 Project Overview
This system is designed to ingest bug reports, stack traces, and error logs, analyze them against a historical knowledge base of resolved bugs (from Mozilla, Apache, and Eclipse), and provide automated triage, duplicate detection, and root-cause analysis.

## 📂 Current Progress (Milestone 1)
*   **Architecture Design**: The system architecture, agent responsibilities, and orchestration flow have been fully documented.
*   **Bug Submission Module**: A Python-based interactive frontend UI has been built using Streamlit (`app.py`).
*   **Dependencies Configured**: Core technologies configured in `requirements.txt`.

*   **Data Engineering Pipeline**: The knowledge base scripts (`src/`) for data cleaning, chunking, and ChromaDB vector embedding have been completed and uploaded.

## 📄 Documentation
*   [System Architecture & Design Document](design_document.md)
*   [Project Technology Stack](tech_stack.md)
