def analyze_text(text):
    words = text.split()

    if len(words) == 0:
        return {
            "characters": len(text),
            "words": 0,
            "first_word": None,
            "last_word": None
        }

    return {
        "characters": len(text),
        "words": len(words),
        "first_word": words[0],
        "last_word": words[-1]
    }


text = input("Enter a text: ")

result = analyze_text(text)

print("\n--- Text Analysis ---")
print("Characters:", result["characters"])
print("Words:", result["words"])
print("First word:", result["first_word"])
print("Last word:", result["last_word"])