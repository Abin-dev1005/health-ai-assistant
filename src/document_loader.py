from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_OVERLAP, CHUNK_SIZE

# Daftar URL artikel kesehatan/pertolongan pertama online
URL_LIST = [
    "https://id.wikipedia.org/wiki/Pertolongan_pertama",
    "https://id.wikipedia.org/wiki/Luka_bakar",
    "https://id.wikipedia.org/wiki/Pendarahan",
]


def load_online_documents() -> List[Document]:
  """Mengambil dan membaca teks langsung dari URL situs web."""
  print(f"[INFO] Mengunduh data dari {len(URL_LIST)} URL online...")
  try:
    loader = WebBaseLoader(URL_LIST)
    documents = loader.load()
    print(f"[INFO] Berhasil mengambil {len(documents)} halaman web.")
    return documents
  except Exception as e:
    print(f"[ERROR] Gagal mengunduh dokumen dari web: {e}")
    return []


def split_documents(documents: List[Document]) -> List[Document]:
  """Memotong teks halaman web menjadi chunks."""
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=CHUNK_SIZE,
      chunk_overlap=CHUNK_OVERLAP,
      separators=["\n\n", "\n", " ", ""],
  )
  chunks = text_splitter.split_documents(documents)
  print(f"[INFO] Teks web dipotong menjadi {len(chunks)} chunks.")
  return chunks


def get_prepared_chunks() -> List[Document]:
  """Fungsi utama untuk memuat dari web dan memotong teks sekaligus."""
  docs = load_online_documents()
  if not docs:
    return []
  return split_documents(docs)