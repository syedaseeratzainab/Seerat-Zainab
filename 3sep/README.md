# Wikipedia Semantic Search

A semantic search system that scrapes Wikipedia articles, cleans the text, creates overlapping word chunks, generates embeddings using Sentence Transformers, and stores the embeddings in a local Qdrant vector database.

## Features

- Scrapes Wikipedia articles
- Extracts paragraphs and list items
- Removes citation markers and unnecessary whitespace
- Creates fixed-size overlapping chunks
- Chunk size: 10 words
- Chunk overlap: 2 words
- Stores chunks and metadata in JSON
- Generates embeddings using `all-MiniLM-L6-v2`
- Stores embeddings in Qdrant
- Performs semantic search
- Returns the top 3 relevant chunks
- Supports multiple questions
- Type `exit` to stop

## Project Structure

```text
wikipedia_semantic_search/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── wikipedia_chunks.json
└── qdrant_db/
````

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Enter a Wikipedia article topic when asked.

Example:

```text
Enter Wikipedia topic: Cristiano Ronaldo
```

After the article is processed, ask questions:

```text
Question: When was Ronaldo born?

Question: Where was Ronaldo born?

Question: Which clubs did Ronaldo play for?
```

Type:

```text
exit
```

to stop the program.

## Technologies

* Python
* Requests
* BeautifulSoup
* Sentence Transformers
* all-MiniLM-L6-v2
* Qdrant
* JSON


