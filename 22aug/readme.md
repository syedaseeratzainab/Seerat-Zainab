# Sentence Embedding Project

## Description

This project loads sentence records from a JSON file and generates embeddings using the `all-MiniLM-L6-v2` model from Sentence Transformers.

The dataset contains sentences from three topics:

- Programming
- Science
- Sports

## Project Structure

```text
22aug/
├── main.py
├── sentences.json
├── requirements.txt
└── README.md
Requirements
Python 3
sentence-transformers
Setup

Create and activate a virtual environment, then install the required package:

pip install -r requirements.txt
Run

Run the program using:

python main.py
Output

The program prints:

Complete embeddings shape
Text of every sentence
Topic of every sentence
Embedding dimension
First five values of every embedding

The project uses the all-MiniLM-L6-v2 model, which generates embeddings with 384 dimensions.