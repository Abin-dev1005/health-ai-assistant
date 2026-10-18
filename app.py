import os
import streamlit as st

from src.document_loader import get_prepared_chunks
from src.rag_chain import build_rag_chain
from src.vector_store import VECTORSTORE_DIR, create_or_get_vectorstore

# Config Halaman Streamlit
st.set_page_config(
    page_title="Health & First-Aid AI Assistant",
    page_icon="🩺",
    layout="centered",
)

st.title("🩺 Health & First-Aid AI Assistant")
st.caption(
    "Asisten Edukasi Pertolongan Pertama berbasis RAG & Ollama (100% Lokal)"
)

# Sidebar untuk Pengelolaan Database Vektor
with st.sidebar:
  st.header("⚙️ Pengaturan Data")
  st.markdown(
      "Masukkan file PDF panduan kesehatan/pertolongan pertama di folder"
      " `data/raw/`."
  )

  if st.button("🔄 Indeks Ulang Dokumen PDF"):
    with st.spinner("Membaca & membuat database vektor baru..."):
      try:
        chunks = get_prepared_chunks()
        if chunks:
          # Hapus atau perbarui vector store
          create_or_get_vectorstore(chunks=chunks)
          st.success("Database Vektor berhasil diperbarui!")
          st.rerun()
        else:
          st.warning("Tidak ada file PDF ditemukan di folder `data/raw/`.")
      except Exception as e:
        st.error(f"Gagal memproses dokumen: {e}")

# Inisialisasi Riwayat Chat
if "messages" not in st.session_state:
  st.session_state.messages = [
      {
          "role": "assistant",
          "content": (
              "Halo! Saya asisten edukasi kesehatan dan pertolongan pertama."
              " Ada yang bisa saya bantu terkait panduan penanganan darurat?"
          ),
      }
  ]

# Menampilkan Riwayat Chat
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Cek Apakah Vectorstore Sudah Ada
vectorstore_exists = os.path.exists(VECTORSTORE_DIR) and os.listdir(
    VECTORSTORE_DIR
)

# Input Chat Pengguna
if user_query := st.chat_input("Tanyakan penanganan medis/pertolongan pertama..."):
  if not vectorstore_exists:
    st.error(
        "Database Vektor belum dibuat! Silakan letakkan file PDF di `data/raw/`"
        " lalu klik tombol 'Indeks Ulang Dokumen PDF' di sidebar."
    )
  else:
    # Tampilkan pesan user di UI
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
      st.markdown(user_query)

    # Generate jawaban dari RAG Chain
    with st.chat_message("assistant"):
      with st.spinner("Mencari di dokumen & menyusun jawaban..."):
        try:
          rag_chain = build_rag_chain()
          response = rag_chain.invoke(user_query)
          st.markdown(response)

          # Simpan respon di session
          st.session_state.messages.append(
              {"role": "assistant", "content": response}
          )
        except Exception as e:
          st.error(f"Terjadi kesalahan: {e}")