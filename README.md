# 🩺 Health & First-Aid AI Assistant

A privacy-focused, 100% local **Retrieval-Augmented Generation (RAG)** chatbot designed to provide health education and first-aid guidance. Powered by **Ollama**, **LangChain**, **ChromaDB**, and **Streamlit**.

---

## 🌟 Key Features

* **100% Local & Privacy-Preserving**: No external API keys required. Runs completely offline on your local machine using Ollama.
* **Dynamic Web Document Ingestion**: Fetches health and first-aid reference articles from trusted online sources using LangChain's `WebBaseLoader`.
* **Fast Vector Search**: Stores and retrieves semantic embeddings efficiently with **ChromaDB** and `nomic-embed-text`.
* **Lightweight LLM Integration**: Powered by `llama3.2:1b` for fast, low-resource local execution.
* **Interactive UI**: Clean and user-friendly web interface built with **Streamlit**.

---

## 🏗️ Project Architecture

```text
[Web / Health Articles] ──> WebBaseLoader ──> Chunking ──> nomic-embed-text ──> ChromaDB
                                                                                  │
[User Query] ─────────────> Similarity Search (Top-K Chunks) ─────────────────────┤
                                                                                  │
                                                                                  ▼
[User Query + Context] ───────────────────> ChatOllama (llama3.2:1b) ──> Final Response

```
---
## 📁 Repository Structure

```text
health-ai-assistant/
├── data/
│   ├── raw/                  # Placeholder for raw documents/text
│   └── vectorstore/          # Local persistent ChromaDB vector store
├── src/
│   ├── __init__.py
│   ├── config.py             # System configuration, paths & prompts
│   ├── document_loader.py    # Web scraping and text chunking pipeline
│   ├── vector_store.py       # Embeddings and ChromaDB management
│   └── rag_chain.py          # RAG pipeline orchestration with LCEL
├── app.py                    # Streamlit web interface
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

```

## 🚀 Getting Started
Prerequisites
1. Python: Version 3.10 or higher.
2. Ollama: Download and install from [ollama.com](url).

## Installation & Setup
1. Clone the Repository
   ```text
   git clone [https://github.com/username-kamu/health-ai-assistant.git](https://github.com/username-kamu/health-ai-assistant.git)
   cd health-ai-assistant
   ```
   
2. Set Up Virtual Environment
   ```text
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
     ```

3. Install Dependencies
   ```text
   pip install -r requirements.txt
    ```
4. Pull Required Ollama Models Make sure Ollama server is running (`ollama servec), then pull the required models:
   ```text
   ollama pull nomic-embed-text
   ollama pull llama3.2:1b
     ```
## 💻 Running the Application
1. Start Ollama Service (if not running as a system background service):
   ```text
   ollama serve
   ```
2. Launch Streamlit Web App:
   ```text
   python3 -m streamlit run app.py
   ```
3. Open your browser at `http://localhost:8501`.
4. Click "Indeks Ulang Dokumen PDF" in the sidebar to build/update the local vector database, then start chatting!

## ⚠️ Medical Disclaimer
This application is designed strictly for educational and informational purposes only. The responses provided by this AI assistant do not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional or emergency medical services for health concerns or life-threatening situations.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
  
  
