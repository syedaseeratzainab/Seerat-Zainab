import json
import os

from document_loader import load_document
from text_cleaner import clean_text
from chunk_createor import create_chunks

# Input PDF file
INPUT_FILE = "documents/Unit01_Digital_Logic_Chapter1.pdf"
# Output JSON file
OUTPUT_FILE = "output/chunks.json"


# 1. Load Document
documents = load_document(INPUT_FILE)

print(f"Loaded pages: {len(documents)}")


# 2. Clean Text
for doc in documents:
    doc["content"] = clean_text(
        doc["content"]
    )


# 3. Create Chunks
# Chunk size and overlap are controlled
# from chunk_creator.py
chunks = create_chunks(
    documents
)

print(f"Total chunks created: {len(chunks)}")

# Save JSON

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

    print("RAG chunks created successfully!")
    print(f"Saved at: {OUTPUT_FILE}")