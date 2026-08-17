# Multi-File Keyword Search Tool

A Python-based tool that searches for keywords across multiple **TXT, DOCX, and PDF files**. It displays matching content, counts occurrences, saves search results, and keeps a history of searches.

## Features

- Searches multiple `.txt`, `.docx`, and `.pdf` files
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
- Supports reading content from DOCX and PDF files

## Project Structure

```text
Multi_File_Keyword_Search/
│
├── .venv/
│
├── documents/
│   ├── Multi_File_Keyword_Search_Tool_Project_Documentation.docx
│   ├── Multi_File_Keyword_Search_Tool_Project_Documentation (1).docx
│   └── file3_web_development.pdf
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

## Libraries Used

- **colorama** – for colored terminal output
- **python-docx** – for reading DOCX files
- **pypdf** – for reading PDF files