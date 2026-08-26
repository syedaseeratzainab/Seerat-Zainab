# Build Your Own Similarity Search

## Overview

This project is a simple semantic similarity search system built using Python and Sentence Transformers.

The program stores documents in a JSON knowledge base, converts the documents and user queries into embeddings, calculates cosine similarity, and returns the three most similar documents.

## Technologies Used

- Python
- JSON
- Sentence Transformers
- PyTorch
- Cosine Similarity
- `all-MiniLM-L6-v2`

## Project Structure

```text
similarity_search/
│
├── .venv/
├── knowledge_base.json
├── main.py
├── requirements.txt
└── README.md
