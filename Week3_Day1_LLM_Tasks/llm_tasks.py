import re
import random
import math


# ============================================================
# TASK 1 - BUILD A SIMPLE TOKENIZATION ANALYZER
# ============================================================

print("\n" + "=" * 60)
print("TASK 1 - SIMPLE TOKENIZATION ANALYZER")
print("=" * 60)

text = input("Enter some text: ")

# Count characters
character_count = len(text)

# Count words using split()
words = text.split()
word_count = len(words)

# Find token-like units using regular expression
token_like_units = re.findall(r"\w+|[^\w\s]", text)
token_count = len(token_like_units)

print("\n--- Tokenization Analysis ---")
print("Characters:", character_count)
print("Words:", word_count)
print("Token-like units:", token_count)

print("\nComparison:")

if word_count == token_count:
    print("Word count and token-like count are the same.")
else:
    print("Word count and token-like count are different.")


# ============================================================
# TASK 2 - SIMULATE NEXT-TOKEN PREDICTION
# ============================================================

print("\n" + "=" * 60)
print("TASK 2 - NEXT-TOKEN PREDICTION")
print("=" * 60)

prompt = input("Enter a prompt: ")

probabilities = {
    "AI": 0.60,
    "systems": 0.25,
    "people": 0.10,
    "data": 0.05
}

# Select the token with the highest probability
next_token = max(probabilities, key=probabilities.get)

print("\nPrompt:", prompt)

print("\nPossible next tokens:")

for token, probability in probabilities.items():
    print(token, "->", probability)

print("\nSelected next token:", next_token)


# ============================================================
# TASK 3 - SIMULATE TEMPERATURE
# ============================================================

print("\n" + "=" * 60)
print("TASK 3 - TEMPERATURE SIMULATION")
print("=" * 60)

probabilities = {
    "AI": 0.60,
    "systems": 0.25,
    "people": 0.10,
    "data": 0.05
}


def apply_temperature(probabilities, temperature):
    adjusted = {}

    for token, probability in probabilities.items():
        adjusted[token] = probability ** (1 / temperature)

    total = sum(adjusted.values())

    for token in adjusted:
        adjusted[token] = adjusted[token] / total

    return adjusted


def select_token(probabilities):
    tokens = list(probabilities.keys())
    values = list(probabilities.values())

    return random.choices(tokens, weights=values, k=1)[0]


temperatures = [0.5, 1.0, 2.0]

for temperature in temperatures:

    adjusted_probabilities = apply_temperature(
        probabilities,
        temperature
    )

    print("\nTemperature:", temperature)

    print("Adjusted probabilities:")

    for token, probability in adjusted_probabilities.items():
        print(token, "->", round(probability, 3))

    print("Generated samples:")

    for i in range(5):
        selected = select_token(adjusted_probabilities)
        print(selected, end=" ")

    print()


# ============================================================
# TASK 4 - CONTEXT-WINDOW BUDGET CALCULATOR
# ============================================================

print("\n" + "=" * 60)
print("TASK 4 - CONTEXT-WINDOW BUDGET CALCULATOR")
print("=" * 60)


def check_context_budget(
    system_tokens,
    history_tokens,
    document_tokens,
    question_tokens,
    output_tokens,
    context_limit
):
    used = (
        system_tokens
        + history_tokens
        + document_tokens
        + question_tokens
        + output_tokens
    )

    remaining = context_limit - used

    fits = used <= context_limit

    return {
        "used": used,
        "remaining": remaining,
        "fits": fits
    }


context_limit = 1000

system_tokens = 100
history_tokens = 250
document_tokens = 300
question_tokens = 50
output_tokens = 200

result = check_context_budget(
    system_tokens,
    history_tokens,
    document_tokens,
    question_tokens,
    output_tokens,
    context_limit
)

print("\nContext limit:", context_limit)
print("Tokens used:", result["used"])
print("Tokens remaining:", result["remaining"])
print("Fits context window:", result["fits"])


# ============================================================
# TASK 5 - PROMPT-TO-RESPONSE ROLE-PLAY
# ============================================================

print("\n" + "=" * 60)
print("TASK 5 - PROMPT-TO-RESPONSE ROLE-PLAY")
print("=" * 60)

role_play_prompt = "RAG helps an AI system"

print("\nUser:")
print(role_play_prompt)

print("\nTokenizer:")
tokens = role_play_prompt.split()
print(tokens)

print("\nContext Manager:")
print("The prompt is placed inside the context window.")

print("\nTransformer / Attention:")
print("The important relationships between tokens are analyzed.")

print("\nToken Selector:")

token_probabilities = {
    "retrieve": 0.40,
    "answer": 0.30,
    "find": 0.20,
    "understand": 0.10
}

selected_token = max(
    token_probabilities,
    key=token_probabilities.get
)

print("Possible next tokens:")

for token, probability in token_probabilities.items():
    print(token, "->", probability)

print("Selected token:", selected_token)

print("\nRecorder:")
print("The selected token is added to the response.")

print("\nFinal simulated response:")
print("RAG helps an AI system", selected_token)