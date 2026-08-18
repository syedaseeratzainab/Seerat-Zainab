def analyze_text(text):
    words = text.split()

    if len(words) == 0:
        return {
            "prompt": text,
            "characters": len(text),
            "words": 0,
            "first_word": None,
            "last_word": None
        }

    return {
        "prompt": text,
        "characters": len(text),
        "words": len(words),
        "first_word": words[0],
        "last_word": words[-1]
    }


# Store the analysis of all three prompts
results = []

# Take three prompts
for i in range(3):
    prompt = input(f"\nEnter prompt {i + 1}: ")

    result = analyze_text(prompt)

    results.append(result)


# Display all results
print("\n--- Text Analysis Results ---")

for result in results:
    print("\nPrompt:", result["prompt"])
    print("Characters:", result["characters"])
    print("Words:", result["words"])
    print("First word:", result["first_word"])
    print("Last word:", result["last_word"])


# Find the prompt with the most words
most_words = max(results, key=lambda result: result["words"])

print("\n--- Prompt With Most Words ---")
print("Prompt:", most_words["prompt"])
print("Number of words:", most_words["words"])