from pathlib import Path

import chromadb


CHROMA_DIR = Path("chroma_db")

COLLECTION_NAME = "documents"


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def add_to_vector_store(
    embeddings,
    chunks,
    metadata
):
    """
    Add document chunks and embeddings to ChromaDB.
    """

    if not embeddings:
        return

    ids = []

    for item in metadata:
        ids.append(
            f"{item['source']}_{item['chunk_id']}"
        )

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadata
    )


def search_vector_store(
    query_embedding,
    top_k=3
):
    """
    Search ChromaDB using the query embedding.
    """

    total_documents = collection.count()

    if total_documents == 0:
        return []

    top_k = min(
        top_k,
        total_documents
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    formatted_results = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        formatted_results.append(
            {
                "text": document,
                "source": metadata["source"],
                "chunk_id": int(
                    metadata["chunk_id"]
                ),
                "score": float(distance)
            }
        )

    return formatted_results


def get_collection_count():
    """
    Return the number of stored chunks.
    """

    return collection.count()