import requests


class EvaluatorAgent:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/chat"
        self.base_prompt = (
            "Eres un generador de ejercicios de práctica sobre seguridad de software.\n"
            "Debes crear 2 preguntas variadas para estudiantes:\n"
            "- 1 de comprensión teórica\n"
            "- 1 de aplicación o análisis práctico\n\n"
            "Muestra las preguntas numeradas y bien redactadas.\n"
            "No incluyas respuestas, solo las preguntas.\n"
        )

    def generar_ejercicios(self, tema, nivel="básico"):
        prompt = (
            f"{self.base_prompt}"
            f"Nivel: {nivel}\n"
            f"Tema: {tema}\n"
            f"Comienza a generar las preguntas:"
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

            data = response.json()
            return data["message"]["content"].strip()

        except Exception as e:
            return f"Error al generar ejercicios: {e}"
