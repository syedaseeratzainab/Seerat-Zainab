Document Semantic Search using LanceDB
📌 Project Overview

This project is a document semantic search system that loads documents, cleans their text, divides the text into smaller chunks, converts the chunks into vector embeddings, stores them in LanceDB, and retrieves the most relevant chunks based on a user's question.

The project is designed as a foundation for building a Retrieval-Augmented Generation (RAG) application.

🔄 Workflow
Document
   ↓
Document Loader
   ↓
Text Cleaning
   ↓
Text Chunking
   ↓
Sentence Transformer
   ↓
Vector Embeddings
   ↓
LanceDB
   ↓
Semantic Search
   ↓
Top Relevant Results
✨ Features
Supports .txt, .pdf, and .docx files
Cleans extracted text
Splits documents into smaller chunks
Generates embeddings using all-MiniLM-L6-v2
Stores embeddings and document information in LanceDB
Performs semantic/vector search
Returns the top relevant results
Displays:
Text
Source
Page
Chunk index
Distance/similarity information
🛠️ Technologies Used
Python
LanceDB — vector database
Sentence Transformers — text embeddings
PyPDF — PDF document loading
python-docx — DOCX document loading
tiktoken — text/token processing
📁 Project Structure
29aug/
│
├── documents/
│   └── employee_training_karachi.docx
│
├── output/
│   └── chunks.json
│
├── vector_db/
│   └── LanceDB database files
│
├── main.py
├── document_loader.py
├── text_cleaner.py
├── chunk_creator.py
├── vector_store.py
├── requirements.txt
├── .gitignore
└── README.md

vector_db/ and .venv/ are excluded from Git using .gitignore.

⚙️ Installation
1. Clone the repository
git clone YOUR_REPOSITORY_URL
2. Open the project folder
cd 29aug
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment

On Windows:

.venv\Scripts\activate
5. Install the required packages
pip install -r requirements.txt