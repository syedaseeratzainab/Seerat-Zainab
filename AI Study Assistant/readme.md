# AI Study Assistant

A beginner-friendly command-line AI Study Assistant built with Python and Hugging Face. The application allows students to ask repeated questions, maintain recent conversation history, clear the conversation, control response temperature, and test JSON responses.

## Features

* Uses Hugging Face Inference API
* Loads `HF_TOKEN` and `MODEL_ID` from a `.env` file
* Beginner-friendly AI system message
* Accepts repeated questions
* Rejects empty questions
* Maintains recent conversation history
* `clear` command resets the conversation history
* `exit` command closes the program
* Supports temperature values from `0.1` to `1.0`
* Includes a JSON prompt
* Parses the AI's JSON response using Python's `json` module
* Handles API and JSON parsing errors

## Project Structure

```text
AI_Study_Assistant/
│
├── main.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

* Python 3
* A Hugging Face account
* A Hugging Face access token with inference permission
* Internet connection

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project folder:

```text
HF_TOKEN=your_actual_huggingface_token
MODEL_ID=your_model_id
```

The `.env.example` file is provided as a template.



## Running the Program

Run:

```powershell
python main.py
```

The program will ask you to enter a temperature between `0.1` and `1.0`.

After that, you can enter your study questions.

## Available Commands

### `clear`

Clears the recent conversation history while keeping the system instructions.

### `json`

Runs a special JSON prompt. The AI returns a JSON-formatted response, and the program parses the response using Python's `json` module.

### `exit`

Exits the AI Study Assistant.

## Author

AI Study Assistant — Python and Hugging Face API practice project.
