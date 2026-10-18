from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

from src.config import HEALTH_SYSTEM_PROMPT, LLM_MODEL, TOP_K_RESULTS
from src.vector_store import create_or_get_vectorstore, get_retriever


def format_docs(docs):
  """Menggabungkan potongan teks hasil pencarian menjadi satu string konteks."""
  return "\n\n---\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
  """Membangun alur RAG menggunakan Ollama dan ChromaDB."""
  # 1. Memuat vectorstore & retriever
  vectorstore = create_or_get_vectorstore()
  retriever = get_retriever(vectorstore, top_k=TOP_K_RESULTS)

  # 2. Inisialisasi LLM Ollama
  llm = ChatOllama(model=LLM_MODEL, temperature=0.1)

  # 3. Inisialisasi Prompt Template
  prompt = ChatPromptTemplate.from_template(HEALTH_SYSTEM_PROMPT)

  # 4. Rantai Alur RAG (LCEL)
  rag_chain = (
      {"context": retriever | format_docs, "question": RunnablePassthrough()}
      | prompt
      | llm
      | StrOutputParser()
  )

  return rag_chain