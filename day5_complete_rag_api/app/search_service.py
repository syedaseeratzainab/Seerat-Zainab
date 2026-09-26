from .embeddings import generate_embedding
from .vector_store import search_vector_store


def search_documents(
    question: str,
    top_k: int = 3
):
    """
    Convert the question into an embedding
    and search ChromaDB.
    """

    query_embedding = generate_embedding(
        question
    )

    results = search_vector_store(
        query_embedding,
        top_k
    )

    return results