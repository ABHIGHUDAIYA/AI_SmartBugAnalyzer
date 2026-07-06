# 🐛 AI SmartBugAnalyzer

An AI-powered defect analysis tool that uses a RAG pipeline and multi-agent orchestration to automatically triage bug reports and detect duplicates.

## 📌 Project Overview
This system is designed to ingest bug reports, stack traces, and error logs, analyze them against a historical knowledge base of resolved bugs (from Mozilla, Apache, and Eclipse), and provide automated triage, duplicate detection, and root-cause analysis.

## 📂 Current Progress (Milestone 1)
*   **Architecture Design**: The system architecture, agent responsibilities, and orchestration flow have been fully documented.
*   **Bug Submission Module**: A Python-based interactive frontend UI has been built using Streamlit (`app.py`).
*   **Dependencies Configured**: Core technologies configured in `requirements.txt`.

*(Note: Data pipelines and RAG implementation scripts are currently in active development and will be released in upcoming commits.)*

## 📄 Documentation
*   [System Architecture & Design Document](design_document.md)
*   [Project Technology Stack](tech_stack.md)
