import lancedb

from sentence_transformers import SentenceTransformer


# ----------------------------
# 1. Load Embedding Model
# ----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ----------------------------
# 2. Create LanceDB
# ----------------------------

DATABASE_PATH = "vector_db"

db = lancedb.connect(
    DATABASE_PATH
)

TABLE_NAME = "course_documents"


# ----------------------------
# 3. Create Embeddings
# ----------------------------

def create_embeddings(chunks):

    if not chunks:
        return []

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()


# ----------------------------
# 4. Store Chunks
# ----------------------------

def store_chunks(chunks):

    if not chunks:

        print(
            "No chunks available to store."
        )

        return

    embeddings = create_embeddings(
        chunks
    )

    data = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        data.append({
            "id": str(
                chunk["chunk_id"]
            ),
            "text": chunk["text"],
            "source": str(
                chunk["source"]
            ),
            "page": (
                chunk["page"]
                if chunk["page"] is not None
                else 0
            ),
            "chunk_index": chunk["chunk_index"],
            "vector": embedding
        })

    if TABLE_NAME in db.table_names():

        table = db.open_table(
            TABLE_NAME
        )

        table.delete(
            "true"
        )

        table.add(
            data
        )

    else:

        table = db.create_table(
            TABLE_NAME,
            data=data
        )

    print(
        f"Stored {len(chunks)} chunks in LanceDB."
    )


# ----------------------------
# 5. Get Vector Count
# ----------------------------

def get_vector_count():

    if TABLE_NAME not in db.table_names():

        return 0

    table = db.open_table(
        TABLE_NAME
    )

    return table.count_rows()


# ----------------------------
# 6. Semantic Search
# ----------------------------

def search_chunks(
    question,
    top_k=3
):

    if TABLE_NAME not in db.table_names():

        print(
            "Vector database is empty."
        )

        return None

    table = db.open_table(
        TABLE_NAME
    )

    if table.count_rows() == 0:

        print(
            "Vector database is empty."
        )

        return None

    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )[0].tolist()

    results = (
        table.search(
            query_embedding
        )
        .limit(top_k)
        .to_list()
    )

    documents = []
    metadatas = []
    distances = []

    for result in results:

        documents.append(
            result["text"]
        )

        metadatas.append({
            "source": result["source"],
            "page": result["page"],
            "chunk_index": result["chunk_index"]
        })

        distances.append(
            result.get(
                "_distance",
                0
            )
        )

    return {
        "documents": [
            documents
        ],
        "metadatas": [
            metadatas
        ],
        "distances": [
            distances
        ]
    }