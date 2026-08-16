# Multi-File Keyword Search Tool

A Python-based tool that searches for keywords across multiple text files. It displays matching lines, counts occurrences, saves search results, and keeps a history of searches.

## Features

- Searches multiple `.txt` files
- Case-insensitive keyword searching
- Exact-word search option
- Displays filename, line number, and matching text
- Shows the number of keyword occurrences in each matching line
- Counts matching files and total matches
- Sorts search results by filename and line number
- Saves search results with a timestamp
- Keeps a search history
- Appends new searches instead of overwriting previous history
- Shows a file-extension summary
- Allows the user to choose a documents folder
- Handles a missing documents folder without crashing
- Provides a colored terminal interface
- Allows repeated searches
- Allows the user to type `exit` to quit

## Project Structure

```text
Multi_File_Keyword_Search/
│
├── .venv/
│
├── documents/
│   ├── document1.txt
│   ├── document2.txt
│   └── document3.txt
│
├── results/
│   ├── search_results.txt
│   └── search_history.txt
│
├── main.py
├── text_utils.py
├── file_utils.py
├── requirements.txt
└── README.md