# Tutor Académico Multiagente con RAG

Este es un sistema de inteligencia artificial multiagente que simula un tutor academico de seguridad

- Responder preguntas teóricas usando recuperación semántica (RAG) sobre apuntes en PDF.
- Generar prácticas con ejercicios de repaso.

Todo el sistema funciona offline usando modelos locales con _Ollama_ y una base vectorial generada con _LangChain + ChromaDB_.

- [Python 3.10+](https://www.python.org/)
- [LangChain](https://docs.langchain.com)
- [ChromaDB](https://www.trychroma.com/)
- [Ollama](https://ollama.com) (modelo: mistral y nomic-embed-text)
- [pdfminer.six](https://github.com/pdfminer/pdfminer.six) (lectura de PDF)

1. Instalar Python
   Python 3.10 o superior instalado:

2. Clonar el repositorio y entra al proyecto
   git clone <tu-repo>
   cd <nombre-del-proyecto>

3. Instalar las dependencias

pip install langchain langchain_ollama langchain-community chromadb pdfminer.six requests
nomic-embed-text

4. Instalar Ollama y modelos
   Descarga e instala Ollama desde: https://ollama.com
   En terminal, descarga los modelos necesarios:
   ollama pull mistral
   ollama pull

5. Se ejecuta el main de python
