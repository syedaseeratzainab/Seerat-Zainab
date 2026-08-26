import json
from pathlib import Path

from sentence_transformers import SentenceTransformer, util


# -----------------------------------------
# 1. SETTINGS
# -----------------------------------------

MODEL_ID = "all-MiniLM-L6-v2"
TOP_K = 3

DATA_FILE = Path(__file__).parent / "knowledge_base.json"


# -----------------------------------------
# 2. LOAD THE KNOWLEDGE BASE
# -----------------------------------------

def load_records():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    return records


# -----------------------------------------
# 3. LOAD THE EMBEDDING MODEL
# -----------------------------------------

print("Loading embedding model...")

model = SentenceTransformer(MODEL_ID)

print("Model loaded successfully!")


# -----------------------------------------
# 4. LOAD DOCUMENTS
# -----------------------------------------

records = load_records()

documents = [record["text"] for record in records]

print(f"Total documents: {len(documents)}")


# -----------------------------------------
# 5. CREATE DOCUMENT EMBEDDINGS
# -----------------------------------------

document_embeddings = model.encode(
    documents,
    convert_to_tensor=True
)

print(
    f"Embedding shape: {tuple(document_embeddings.shape)}"
)


# -----------------------------------------
# 6. SEARCH FUNCTION
# -----------------------------------------

def search(query, top_k=TOP_K):

    # Create an embedding for the query
    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    # Calculate cosine similarity
    scores = util.cos_sim(
        query_embedding,
        document_embeddings
    )[0]

    # Store document + score
    results = []

    for record, score in zip(records, scores):

        results.append({
            "id": record["id"],
            "text": record["text"],
            "source": record["source"],
            "score": float(score)
        })

    # Sort highest score first
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # Return top-k results
    return results[:top_k]


# -----------------------------------------
# 7. USER SEARCH
# -----------------------------------------

while True:

    query = input(
        "\nEnter your question (or type 'exit'): "
    ).strip()

    # Exit the program
    if query.lower() == "exit":
        print("Program ended.")
        break

    # Check for empty query
    if not query:
        print("Please enter a non-empty query.")
        continue

    # Perform search
    results = search(query)

    # Display results
    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    for rank, result in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print(f"Score: {result['score']:.4f}")
        print(f"Text: {result['text']}")
        print(f"Source: {result['source']}")