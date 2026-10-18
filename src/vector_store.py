import os
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from src.config import EMBEDDING_MODEL, VECTORSTORE_DIR


def get_embedding_function() -> OllamaEmbeddings:
  """Inisialisasi fungsi embedding dari Ollama."""
  return OllamaEmbeddings(model=EMBEDDING_MODEL)


def create_or_get_vectorstore(
    chunks: List[Document] = None,
) -> Chroma:
  """Membuat database vektor baru jika belum ada,

  atau memuat database vektor lokal yang sudah tersimpan.
  """
  embeddings = get_embedding_function()

  # Cek apakah folder vectorstore sudah berisi data ChromaDB
  if os.path.exists(VECTORSTORE_DIR) and os.listdir(VECTORSTORE_DIR):
    print(f"[INFO] Memuat ChromaDB dari penyimpanan lokal: {VECTORSTORE_DIR}")
    vectorstore = Chroma(
        persist_directory=str(VECTORSTORE_DIR), embedding_function=embeddings
    )
  else:
    if not chunks:
      raise ValueError(
          "Database vektor belum ada dan tidak ada data chunk untuk dibuatkan "
          "indeks baru. Harap masukkan file PDF di data/raw/ terlebih dahulu."
      )
    print(f"[INFO] Membuat ChromaDB baru dan menyimpan ke: {VECTORSTORE_DIR}")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
    )
    print("[INFO] Database vektor berhasil dibuat dan disimpan.")

  return vectorstore


def get_retriever(vectorstore: Chroma, top_k: int = 3):
  """Mengembalikan objek retriever untuk pencarian similarity."""
  return vectorstore.as_retriever(search_kwargs={"k": top_k})