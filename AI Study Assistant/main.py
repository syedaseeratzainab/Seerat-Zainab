import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load values from .env
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("MODEL_ID")


# Check required environment variables
if not HF_TOKEN:
    raise ValueError("HF_TOKEN is missing from .env")

if not MODEL_ID:
    raise ValueError("MODEL_ID is missing from .env")


# Create Hugging Face client
client = InferenceClient(
    model=MODEL_ID,
    token=HF_TOKEN,
    provider="auto"
)

# Beginner-friendly system message
SYSTEM_MESSAGE = """
You are an AI Study Assistant for beginners.
Explain topics in simple and clear language.
Use short examples when helpful.
If the student does not understand something, explain it in an easier way.
Be encouraging and focus on helping the student learn.
"""


# Keep only recent conversation messages
MAX_HISTORY_MESSAGES = 10

#This function ask the user for the temperature.
def get_temperature():
    """Ask the user for a temperature between 0.1 and 1.0."""

    while True:
        value = input("Enter temperature (0.1 - 1.0): ").strip()

        try:
            temperature = float(value)

            if 0.1 <= temperature <= 1.0:
                return temperature

            print("Temperature must be between 0.1 and 1.0.")

        except ValueError:
            print("Please enter a valid number.")

#This function sends the conversation to Hugging Face.
def get_response(messages, temperature):
    """Send conversation history to Hugging Face and return the response."""

    response = client.chat_completion(
        messages=messages,
        temperature=temperature,
        max_tokens=500
    )

    return response.choices[0].message.content  #gets the actual text answer from the response


def parse_json_response(response):
    """Parse a JSON response from the AI."""

    response = response.strip()

    # Remove Markdown code fences if the model adds them
    #Then we handle cases where the AI might return: ...
   
    if response.startswith("```json"):
        response = response[7:]
    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    return json.loads(response)   #Take JSON text and load it into Python.


def ask_json_question(temperature):
    # Ask the user for the question that should receive a JSON response
    json_question = input("Enter your question for JSON response: ").strip()

    # Reject an empty JSON question
    if not json_question:
        print("Please enter a question.")
        return

    # Tell the AI to return the answer in JSON format
    json_prompt = f"""
Answer the following study question for a beginner:

{json_question}

Return ONLY valid JSON using exactly this structure:

{{
    "question": "The question asked by the student",
    "answer": "A simple and clear answer",
    "example": "A short example if appropriate"
}}

Do not add Markdown or any text outside the JSON.
"""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        },
        {
            "role": "user",
            "content": json_prompt
        }
    ]

    try:
        # Ask the AI for a response
        response = get_response(messages, temperature)

        # Parse the JSON response into a Python dictionary
        data = parse_json_response(response)

        print("\nParsed JSON result:")
        print(data)

    except json.JSONDecodeError:
        print("\nThe AI did not return valid JSON.")
        print("Raw response:")
        print(response)

    except Exception as error:
        print(f"\nError: {error}")

def main():
    print("=" * 50)
    print("        AI STUDY ASSISTANT")
    print("=" * 50)

    print("\nCommands:")
    print("  clear  - Clear conversation history")
    print("  json   - Test JSON response and parsing")
    print("  exit   - Exit the program")

    temperature = get_temperature()

    # Start conversation with the system message
    conversation_history = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    while True:
        question = input("\nYou: ").strip()

        # Reject empty questions
        if not question:
            print("Please enter a question.")
            continue

        # Exit command
        if question.lower() == "exit":
            print("Goodbye! Keep learning!")
            break

        # Clear conversation history
        if question.lower() == "clear":
            conversation_history = [
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE
                }
            ]

            print("Conversation history cleared.")
            continue

        # JSON demonstration
        if question.lower() == "json":
            ask_json_question(temperature)
            continue

        # Add user's question to history
        conversation_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Keep only recent messages plus the system message
        conversation_history = (
            [conversation_history[0]]
            + conversation_history[-MAX_HISTORY_MESSAGES:]
        )

        try:
            answer = get_response(
                conversation_history,
                temperature
            )

            print(f"\nAI: {answer}")

            # Add AI response to conversation history
            conversation_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            # Keep history recent
            conversation_history = (
                [conversation_history[0]]
                + conversation_history[-MAX_HISTORY_MESSAGES:]
            )

        except Exception as error:
            print(f"\nError while contacting Hugging Face: {error}")

            # Remove the unanswered user question if the API failed
            if conversation_history[-1]["role"] == "user":
                conversation_history.pop()


if __name__ == "__main__":
    main()