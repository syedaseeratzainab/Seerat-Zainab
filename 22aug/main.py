import json
from sentence_transformers import SentenceTransformer


# Load records from JSON
with open("sentences.json", "r", encoding="utf-8") as file:
    records = json.load(file)


# Extract sentence text
sentences = [record["text"] for record in records]


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Generate embeddings
embeddings = model.encode(sentences)


# Print complete embeddings shape
print("Complete embeddings shape:", embeddings.shape)

print("\nSentence Details")
print("=" * 60)


# Print information for every record
for record, embedding in zip(records, embeddings):
    print("\nText:", record["text"])
    print("Topic:", record["topic"])
    print("Dimension:", len(embedding))
    print("First five values:", embedding[:5])