from agents.rag import RAGAgent
from agents.evaluator import EvaluatorAgent
import requests


class TutorAgent:
    def __init__(self):
        self.rag = RAGAgent()
        self.eval = EvaluatorAgent()
        self.api_url = "http://localhost:11434/api/chat"
        self.system_prompt = (
            "Eres un tutor experto en seguridad de software. "
            "Responde de forma clara, educativa y paso a paso usando los apuntes como contexto."
        )

    def handle_question(self, question):
        question = question.strip()
        # Permitir preguntas de práctica
        if question.lower().startswith("practica:"):
            print("Generando ejercicios de práctica con el evaluador...")
            partes = question.split(":", 1)[1].strip()

            # Por si viene dificultad entre paréntesis como "tema (nivel)"
            if "(" in partes and ")" in partes:
                tema, nivel = partes.split("(")
                tema = tema.strip()
                nivel = nivel.replace(")", "").strip()
            else:
                tema = partes
                nivel = "básico"

            return self.eval.generar_ejercicios(tema, nivel)

        # Pregunta normal con uso de RAG
        contexto = self.rag.query_knowledge_base(question)

        prompt = (
            f"{self.system_prompt}\n\n"
            f"Apuntes relevantes:\n{contexto}\n\n"
            f"Pregunta del estudiante: {question}\nRespuesta:"
        )

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": "mistral",
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
            )

            return response.json()["message"]["content"].strip()

        except Exception as e:
            return f"Error al generar respuesta: {e}"
