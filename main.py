from agents.tutor import TutorAgent


def main():
    tutor = TutorAgent()

    print("\nBienvenido al Tutor Académico de Seguridad!")
    print("Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tu pregunta: ")
        if user_input.lower() == "salir":
            break

        response = tutor.handle_question(user_input)
        print("\nRespuesta del tutor:\n", response)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()
