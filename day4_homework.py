   #TASK 1

# List of sentences to search
sentences = [
    "Python is useful for AI.",
    "Python can process documents.",
    "AI systems use Python.",
    "Learning Python is fun.",
    "Programming helps solve problems."
]

while True:
    # Ask the user for a keyword
    keyword = input("Enter a keyword (or type exit): ").strip().lower()

    # Stop the program when the user enters exit
    if keyword == "exit":
        print("Program ended.")
        break

    # Reject empty input
    if keyword == "":
        print("Please enter a keyword.")
        continue

    matching_sentences = []

    # Search all sentences without case sensitivity
    for sentence in sentences:
        if keyword in sentence.lower():
            matching_sentences.append(sentence)

    # Display the total number of matches
    print("Total matches:", len(matching_sentences))

    if len(matching_sentences) == 0:
        print("No result found")
    else:
        print("Matching results:")

        # Display matching sentences with numbers
        for number, sentence in enumerate(matching_sentences, start=1):
            print(number, ".", sentence)


                         #TASK 2

    # Store each sentence with source and page information
sentences = [
    {
        "text": "Python is useful for AI.",
        "source": "notes.pdf",
        "page": 1
    },
    {
        "text": "Python can process documents.",
        "source": "notes.pdf",
        "page": 2
    },
    {
        "text": "AI systems use Python.",
        "source": "ai.pdf",
        "page": 3
    },
    {
        "text": "Learning Python is fun.",
        "source": "python.pdf",
        "page": 5
    },
    {
        "text": "Programming helps solve problems.",
        "source": "notes.pdf",
        "page": 6
    }
]

while True:
    # Ask the user for a keyword
    keyword = input("Enter a keyword (or type exit): ").strip().lower()

    # Stop the program
    if keyword == "exit":
        print("Program ended.")
        break

    # Reject empty input
    if keyword == "":
        print("Please enter a keyword.")
        continue

    # Ask for optional filters
    source_filter = input(
        "Enter source to filter or press Enter for all: "
    ).strip().lower()

    page_filter = input(
        "Enter page to filter or press Enter for all: "
    ).strip()

    matching_results = []
    total_occurrences = 0

    # Search through every sentence
    for position, sentence_data in enumerate(sentences, start=1):

        # Apply source filter
        if source_filter != "" and sentence_data["source"].lower() != source_filter:
            continue

        # Apply page filter
        if page_filter != "" and str(sentence_data["page"]) != page_filter:
            continue

        # Convert sentence into individual words
        words = sentence_data["text"].lower().replace(".", "").replace(",", "").split()

        # Exact-word matching
        word_count = words.count(keyword)

        if word_count > 0:
            matching_results.append({
                "position": position,
                "text": sentence_data["text"],
                "source": sentence_data["source"],
                "page": sentence_data["page"]
            })

            # Count total occurrences
            total_occurrences += word_count

    # Display total occurrences
    print("\nTotal keyword occurrences:", total_occurrences)
    print("Total matching sentences:", len(matching_results))

    if len(matching_results) == 0:
        print("No result found")

    else:
        print("\nMatching results:")

        # Display numbered results
        for number, result in enumerate(matching_results, start=1):
            print(
                number,
                ". Position:", result["position"],
                "|", result["text"],
                "| Source:", result["source"],
                "| Page:", result["page"]
            )

        # Display first matching result
        print("\nFirst matching result:")
        print(matching_results[0])

        # Display last matching result
        print("\nLast matching result:")
        print(matching_results[-1])