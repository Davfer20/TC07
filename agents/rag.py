import os
import requests
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from pdfminer.high_level import extract_text
from langchain_ollama.embeddings import OllamaEmbeddings


class RAGAgent:
    def __init__(self):
        folder = "data"
        pdfs = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
        if not pdfs:
            raise FileNotFoundError("No hay PDFs en la carpeta 'data/'")

        self.pdf_path = os.path.join(folder, pdfs[0])
        print(f"Leyendo el PDF: {self.pdf_path}")
        self.db_path = "chromadb_store"
        self.vectordb = self._crear_base_vectorial()

    def _leer_pdf_pdfminer(self):
        try:
            texto = extract_text(self.pdf_path)
            if not texto.strip():
                raise ValueError("El PDF fue leído pero está vacío.")
            return texto
        except Exception as e:
            raise RuntimeError(f"Error al leer PDF con pdfminer: {e}")

    def _crear_base_vectorial(self):
        texto = self._leer_pdf_pdfminer()
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
        chunks = splitter.create_documents([texto])

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        return Chroma.from_documents(
            chunks, embedding=embeddings, persist_directory=self.db_path
        )

    def query_knowledge_base(self, pregunta):
        resultados = self.vectordb.similarity_search(pregunta, k=3)
        print("Fragmentos importantes recuperados:")
        for i, doc in enumerate(resultados, 1):
            print(f"\n--- Fragmento {i} ---\n{doc.page_content.strip()}")

        contexto = "\n".join([doc.page_content for doc in resultados])

        prompt = (
            "Usa los siguientes apuntes para responder la pregunta del estudiante:\n\n"
            f"{contexto}\n\nPregunta: {pregunta}\nRespuesta:"
        )

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "mistral",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
            )
            return response.json()["message"]["content"].strip()
        except Exception as e:
            return f"Error al consultar Ollama: {e}"
