# System Architecture & Design Document

## 1. System Overview
The Defect Analysis AI System is a platform that automatically analyzes software bug reports, stack traces, and error logs. It uses artificial intelligence to triage bugs, find duplicate issues from historical data, and suggest fixes.

## 2. Architecture Components

### 2.1 User Interface (Streamlit)
- **Role**: The main interface where users interact with the system.
- **Features**: Allows users to manually paste bug text, and features an Automated Validation Suite dashboard to process bulk test samples.
- **Tech**: Built entirely in Python using Streamlit with custom CSS (Glassmorphism).

### 2.2 Historical Defect Knowledge Base (RAG Pipeline)
- **Role**: Acts as the memory of the system. It stores thousands of resolved historical bugs from open-source projects (like Mozilla, Apache, and Eclipse) so the AI can learn from past solutions.
- **How it works**:
  1. **Data Cleaning**: Raw bug reports are loaded and cleaned.
  2. **Chunking**: Long bug reports are split into smaller, readable pieces.
  3. **Embedding**: The text is converted into numbers (vectors) using AI models.
  4. **Database**: These vectors are saved in a Vector Database (ChromaDB) for fast searching.

### 2.3 AI Orchestrator (Multi-Agent System)
- **Role**: Manages different AI "agents" that each have a specific job when analyzing a new bug.
- **The Agents**:
  - **Triage Agent**: Decides how severe the bug is and what part of the system it affects.
  - **Duplicate Agent**: Searches the Vector Database to see if this bug has happened before.
  - **Root Cause Agent**: Reads the error logs to guess the exact cause of the crash.
  - **Remediation Agent**: Suggests the code changes needed to fix the bug.

## 3. How a Bug is Processed (Workflow)
1. **Submit**: A user uploads an error log on the website.
2. **Search**: The system searches the Vector Database for similar past issues.
3. **Analyze**: The AI agents review the new error log alongside the historical data.
4. **Report**: The agents combine their findings into a simple, easy-to-read report and display it back to the user.

## 4. Database Schema
When historical bugs are saved in the database, they are stored with the following information:
- **`id`**: A unique ID for the text chunk.
- **`vector`**: The numerical representation of the text.
- **`text`**: The actual words of the bug report.
- **`metadata`**: Extra details, such as the original bug ID and whether it was successfully fixed.
