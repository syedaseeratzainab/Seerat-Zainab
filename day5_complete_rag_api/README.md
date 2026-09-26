# Day 5 Complete RAG Question Answering API

This project implements a complete Retrieval-Augmented Generation (RAG) pipeline using:

- FastAPI
- ChromaDB
- Sentence Transformers
- Hugging Face Inference
- PDF, DOCX, TXT, CSV, JSON, Markdown and HTML support

## RAG Flow

User Question
↓
Query Embedding
↓
ChromaDB Similarity Search
↓
Top-K Relevant Chunks
↓
Prompt Creation
↓
Hugging Face LLM
↓
Final Answer + Sources

## Project Structure

```text
day5_complete_rag_api/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── file_loader.py
│   ├── text_cleaner.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── search_service.py
│   ├── prompt_builder.py
│   └── rag_service.py
│
├── data/
├── chroma_db/
├── .env
├── .gitignore
├── requirements.txt
└── README.md