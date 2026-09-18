import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from prompts import study_prompt
from embeddings import generate_word_embeddings


def create_client():

    project_folder = Path(__file__).resolve().parent
    env_path = project_folder / ".env"

    load_dotenv(
        dotenv_path=env_path,
        override=True
    )

    token = os.getenv("HF_TOKEN")
    model_id = os.getenv("MODEL_ID")

    if not token:
        raise RuntimeError(
            "HF_TOKEN is missing from .env"
        )

    if not model_id:
        raise RuntimeError(
            "MODEL_ID is missing from .env"
        )

    print(
        "Loaded model:",
        model_id
    )

    client = InferenceClient(
        model=model_id,
        token=token
    )

    return client


def main():

    try:

        client = create_client()

        print("\nAI Study Helper")
        print("Type 'exit' to close the program.\n")

        while True:

            topic = input(
                "Topic: "
            ).strip()

            if topic.lower() == "exit":

                print("\nGoodbye!")
                break

            if not topic:

                print(
                    "\nPlease enter a topic.\n"
                )
                continue

            # Generate separate embeddings for each word
            word_embeddings = generate_word_embeddings(topic)

            print("\nWord embeddings generated!")

            for word, vector in word_embeddings.items():

                print("\nWord:", word)
                print("Embedding size:", len(vector))
                print("First 385 values:", vector[:385])

            level = input(
                "Level (beginner/intermediate): "
            ).strip()

            if not level:

                level = "beginner"

            messages = study_prompt.format_messages(
                topic=topic,
                level=level
            )

            hf_messages = []

            for message in messages:

                if message.type == "system":
                    role = "system"
                else:
                    role = "user"

                hf_messages.append(
                    {
                        "role": role,
                        "content": message.content
                    }
                )

            print(
                "\nGenerating explanation...\n"
            )

            response = client.chat_completion(
                messages=hf_messages,
                max_tokens=500,
                temperature=0.3
            )

            answer = response.choices[0].message.content

            print(answer)

            print(
                "\n" + "-" * 50 + "\n"
            )

    except Exception as error:

        print(
            "\nThe program could not run."
        )

        print(
            "\nError details:"
        )

        print(error)


if __name__ == "__main__":
    main()

