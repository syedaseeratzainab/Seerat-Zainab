import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from .search_service import search_documents
from .prompt_builder import build_prompt


load_dotenv()


HF_TOKEN = os.getenv(
    "HF_TOKEN"
)

MODEL_ID = os.getenv(
    "MODEL_ID"
)


if not HF_TOKEN:
    raise RuntimeError(
        "HF_TOKEN is missing in the .env file."
    )


if not MODEL_ID:
    raise RuntimeError(
        "MODEL_ID is missing in the .env file."
    )


client = InferenceClient(
    api_key=HF_TOKEN
)


def generate_answer(
    prompt: str
):
    """
    Send the RAG prompt to the Hugging Face model.
    """

    try:

        response = client.chat_completion(
            model=MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful RAG assistant. "
                        "Use only the context provided by the user."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.2
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        if not answer:
            raise RuntimeError(
                "The LLM returned an empty answer."
            )

        return answer.strip()

    except Exception as error:

        raise RuntimeError(
            f"LLM error: {str(error)}"
        )


def ask_question(
    question: str,
    top_k: int = 3
):
    """
    Complete RAG pipeline.
    """

    results = search_documents(
        question,
        top_k
    )

    if not results:

        return {
            "answer": (
                "The available documents do not "
                "contain enough information to "
                "answer this question."
            ),
            "sources": []
        }

    prompt = build_prompt(
        question,
        results
    )

    answer = generate_answer(
        prompt
    )

    sources = []

    for result in results:

        sources.append(
            {
                "source": result["source"],
                "chunk_id": result["chunk_id"],
                "score": result["score"],
                "text_preview": (
                    result["text"][:200]
                )
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }