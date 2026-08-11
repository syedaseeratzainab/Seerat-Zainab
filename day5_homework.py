# List of AI- and RAG-related sentences
sentences = [
    "Artificial intelligence helps computers solve complex problems.",
    "RAG systems combine retrieval with language generation.",
    "Python is widely used for artificial intelligence projects.",
    "A vector database stores embeddings for fast retrieval.",
    "Machine learning allows computers to learn from data.",
    "RAG can improve the accuracy of AI-generated answers.",
    "Natural language processing helps computers understand text.",
    "Embeddings represent text as numerical vectors.",
    "Large language models can generate human-like responses.",
    "Document retrieval is an important part of a RAG pipeline.",
    "AI applications can process and analyze large documents.",
    "Chunking divides documents into smaller pieces for retrieval."
]


# 1. Function to clean the text
def clean_text(text):
    return text.lower()


# 2. Function to count the words in a sentence
def count_words(text):
    text = clean_text(text)
    words = text.split()
    return len(words)


# 3. Function to count a keyword in the text
def count_keyword(text, keyword):
    text = clean_text(text)
    keyword = clean_text(keyword)

    words = text.split()
    count = 0

    for word in words:
        if word == keyword:
            count += 1

    return count


# 4. Function to search all sentences
def search_sentences(sentences, keyword, case_sensitive=False):
    results = []

    for number, sentence in enumerate(sentences, start=1):

        # Search without case sensitivity
        if keyword.lower() in sentence.lower():

            # Store the matching sentence information
            results.append({
                "number": number,
                "text": sentence,
                "word_count": count_words(sentence)
            })

    return results


# 5. Function to display the results
# message has a default value
def display_results(results, message="Search Results"):

    print("\n===", message, "===")

    # Check if there are no matching sentences
    if len(results) == 0:
        print("No result found")
        return

    # Display every matching sentence
    for result in results:
        print("\nSentence", result["number"], ":", result["text"])
        print("Word count:", result["word_count"])

    # Display total number of matches
    print("\nTotal matches:", len(results))


# Main program

# Ask the user to enter a keyword
keyword = input("Enter a keyword: ").strip()


# Reject an empty keyword
if keyword == "":
    print("Keyword cannot be empty.")

else:
    # Search the sentences
    # Keyword arguments are used here
    results = search_sentences(
        sentences=sentences,
        keyword=keyword
    )

    # Display the results
    # 'message' is also passed as a keyword argument
    display_results(
        results=results,
        message="Matching Sentences"
    )