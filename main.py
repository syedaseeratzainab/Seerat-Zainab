import json
import os

from document_loader import load_document
from text_cleaner import clean_text
from chunk_creator import create_chunks
from vector_store import (
    store_chunks,
    search_chunks,
    get_vector_count
)

# Input / Output
INPUT_FILE = "documents/employee_training_karachi.docx"
OUTPUT_FILE = "output/chunks.json"

# 1. Load Document
documents = load_document(INPUT_FILE)

print(
    f"Loaded pages/documents: {len(documents)}"
)

# 2. Clean Text
for doc in documents:
    doc["content"] = clean_text(
        doc["content"]
    )

# 3. Create Chunks
chunks = create_chunks(
    documents,
    chunk_size=120,
    overlap=20
)

print(
    f"Total chunks created: {len(chunks)}"
)

# 4. Save Chunks to JSON
os.makedirs(
    "output",
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        chunks,
        file,
        indent=4,
        ensure_ascii=False
    )

print(
    "RAG chunks created successfully!"
)

print(
    f"Saved at: {OUTPUT_FILE}"
)

# 5. Store in ChromaDB
store_chunks(
    chunks
)

print(
    f"Vector records: {get_vector_count()}"
)

# 6. Semantic Search
question = input(
    "\nEnter your search question: "
).strip()

if question:
    results = search_chunks(
        question,
        top_k=3
    )

    if results:
        print(
            "\nTop Semantic Search Results:"
        )

        documents_result = results["documents"][0]
        metadatas_result = results["metadatas"][0]

        for index, text in enumerate(
            documents_result,
            start=1
        ):
            metadata = metadatas_result[
                index - 1
            ]

            print(
                f"\nResult {index}"
            )

            print(
                "Text:",
                text
            )

            print(
                "Source:",
                metadata["source"]
            )

            print(
                "Page:",
                metadata["page"]
            )
