# Course Knowledge Search Engine

A small semantic search engine that stores course knowledge in a persistent ChromaDB collection and returns the most relevant results for a user's question.

## Technologies Used

- Python
- ChromaDB
- JSON

## Project Structure

```text
course_knowledge_search/
│
├── main.py
├── knowledge_base.json
├── requirements.txt
├── README.md
└── chroma_db

Knowledge Base

The knowledge base contains 10 records from four categories:

Programming
Artificial Intelligence
Databases
Software Development

Each record contains:

Unique ID
Document text
Source
Category

How It Works
The program loads records from knowledge_base.json.
A persistent ChromaDB client is created.
A ChromaDB collection is created or loaded.
The knowledge base is added to the collection if it is empty.
The user enters a question.
ChromaDB searches for the three most relevant documents.
The program displays the document, source, category, and distance.
The user can type exit to close the program.
Empty queries are rejected.