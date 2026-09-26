from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


model = SentenceTransformer(
    MODEL_NAME
)


def generate_embeddings(texts: list[str]):
    """
    Generate embeddings for multiple text chunks.
    """

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def generate_embedding(text: str):
    """
    Generate an embedding for one query.
    """

    embedding = model.encode(
        [text],
        normalize_embeddings=True
    )

    return embedding[0].tolist()