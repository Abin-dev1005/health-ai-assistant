import os
from pathlib import Path

# ==========================================
# PATH CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"

# Memastikan direktori data ada
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# OLLAMA & MODEL CONFIGURATION
# ==========================================
# Diubah ke versi 1B yang jauh lebih ringan dan cepat
LLM_MODEL = "llama3.2:1b"
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"

# ==========================================
# TEXT SPLITTER (CHUNKING) CONFIGURATION
# ==========================================
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RESULTS = 3

# ==========================================
# PROMPT TEMPLATE (HEALTH ASSISTANT)
# ==========================================
HEALTH_SYSTEM_PROMPT = """Kamu adalah Asisten Edukasi Kesehatan dan Pertolongan Pertama yang ramah, empati, dan presisi.
Tugas utama kamu adalah memberikan informasi edukasi kesehatan berdasarkan KONTEKS DOKUMEN yang diberikan.

ATURAN PENTING:
1. Jawablah pertanyaan HANYA berdasarkan informasi yang ada pada Konteks di bawah ini.
2. Jika informasi tidak ada di dalam Konteks, katakan dengan jujur bahwa kamu tidak menemukan informasinya di dokumen panduan. Jangan mengarang jawaban.
3. Selalu sertakan penafian (disclaimer) di akhir jawaban bahwa informasi ini bertujuan untuk edukasi dan bukan pengganti saran/diagnosis medis dari dokter profesional.

Konteks Dokumen:
{context}

Pertanyaan Pengguna:
{question}

Jawaban Edukasi Medis:"""