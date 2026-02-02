# 🧬 Clinical Insight Agent (Autonomous RAG System)

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![AI](https://img.shields.io/badge/AI-LangGraph%20%26%20Gemini-purple)
![License](https://img.shields.io/badge/License-MIT-green)

**Clinical Insight Agent** is an autonomous AI assistant designed for medical researchers and healthcare professionals to query, analyze, and summarize clinical trial data.

The project utilizes a **Hybrid RAG (Retrieval-Augmented Generation)** architecture, leveraging both structured SQL databases and semantic vector stores (ChromaDB) simultaneously. The agent autonomously decides whether to perform statistical analysis via SQL or read medical documents for qualitative insights using **LangGraph**.

---

## 🚀 Architecture & Workflow

The system follows a strict technical pipeline designed for reliability and autonomous reasoning:

1.  **Data Ingestion (ETL):** Real-time data is fetched from the **ClinicalTrials.gov API**, cleaned, and split into structured and unstructured components.
2.  **Hybrid Storage:**
    - **Metadata (SQL):** Dates, Phases, Status, and enrollment numbers are stored in a relational database.
    - **Semantic Data (ChromaDB):** Study summaries and eligibility criteria are vectorized using the **`all-MiniLM-L6-v2`** model.
3.  **Autonomous Routing (LangGraph):** The agent analyzes the user's intent. It intelligently decides whether to run a SQL query (for statistics) or a Vector Search (for medical context).
4.  **Retrieval & Context Injection:** Relevant data is retrieved from the selected source.
5.  **LLM Generation:** The retrieved context and prompt are sent to **Gemini Flash-Latest** to generate an evidence-based, hallucination-free answer.

### 🌟 Key Features

- **Agentic Workflow:** It doesn't just retrieve; it _thinks_. It uses tools dynamically based on the question.
- **Hybrid Memory:** Combines SQL for exact numbers ("How many phase 3 trials?") and Vector DB for concepts ("How does GZR102 work?").
- **Optimized Performance:** Uses lightweight embeddings and asynchronous API calls for speed.
- **One-Click Setup:** Includes automated scripts (`.sh` and `.bat`) for instant local environment setup.
- **Evidence-Based:** Every answer is grounded in actual NCT-ID records, minimizing hallucinations.

---

## 📸 Project Demo

Below you can see how the agent operates, switching between SQL tools and Vector Search tools based on the user's query.

[Click Here to Watch the Demo Video](asset/example.webm)

---

## 🛠️ Tech Stack

This project is built on a modern, scalable, and AI-first technology stack:

### AI & Orchestration

- 🦜️🕸️ **LangGraph** – Stateful agentic workflows and decision-making logic
- 🧠 **Google Gemini-Flash-Latest"** – High-performance, cost-effective LLM
- 🤗 **HuggingFace Embeddings** – Medical text embeddings (`all-MiniLM-L6-v2`)

### Backend & API

- ⚡ **FastAPI** – High-performance async REST API
- 🗄️ **SQLAlchemy & SQLite / PostgreSQL** – Structured data storage
- 🎨 **ChromaDB** – Vector database for semantic retrieval

### Frontend

- 👑 **Streamlit** – Interactive and user-friendly UI

### DevOps & Tooling

- 🐳 **Docker** – Optional containerized deployment
- 📝 **Custom Logging** – Monitoring and debugging support

---

## 📂 Dataset & Pipeline

The system is powered by real-time data from the **ClinicalTrials.gov API v2**.

### ETL Pipeline

1. **Extract**  
   Fetches clinical studies for target conditions (e.g., Diabetes, Cancer)

2. **Transform**
   - **SQL Path:** Title, Phase, Status, Dates, Locations
   - **Vector Path:** Brief Summary + Eligibility Criteria → text chunks → embeddings

3. **Load**
   - Relational DB (SQL)
   - Vector DB (ChromaDB)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/BozyelOzan/clinical-insight-agent.git
cd clinical-insight-agent
```

---

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# --- API KEYS ---
GOOGLE_API_KEY=your_gemini_api_key_here

# --- DATABASE CONFIG ---
DATABASE_URL=sqlite:///./data/clinical_trials.db

# --- VECTOR DB CONFIG ---
CHROMA_PERSIST_DIR=./data/chroma_db
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

# --- PROJECT SETTINGS ---
PROJECT_NAME=Clinical Insight Agent
VERSION=1.0.0
LOG_DIR=./data/raw_logs
```

> ⚠️ **Important:** Replace `GOOGLE_API_KEY` with your actual Gemini API key.

---

### 3. Quick Start (Recommended) ⚡

Automated scripts are provided for one-click setup:

- **Windows:** Double-click `run_windows.bat`
- **Linux / macOS:**

  ```bash
  ./run_linux_mac.sh
  ```

These scripts will:

- Create a virtual environment
- Install dependencies
- Launch backend & frontend

---

## 🖐️ Manual Installation

### 1. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Ingest Data (Initialize Memory)

```bash
python -m scripts.bulk_ingest
```

### 3. Start Backend Server

```bash
uvicorn backend.main:app --reload
```

### 4. Start Frontend UI (New Terminal)

```bash
streamlit run frontend/app.py
```

---
