import json
import chromadb


# -----------------------------------------
# SETTINGS
# -----------------------------------------

DATABASE_PATH = "chroma_db"
COLLECTION_NAME = "course_knowledge"
DATA_FILE = "knowledge_base.json"


# -----------------------------------------
# LOAD KNOWLEDGE BASE
# -----------------------------------------

def load_records(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


# -----------------------------------------
# CREATE AND FILL CHROMADB COLLECTION
# -----------------------------------------

def prepare_collection(records):

    # Create persistent ChromaDB client
    client = chromadb.PersistentClient(
        path=DATABASE_PATH
    )

    # Create or load collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    # Add records only if collection is empty
    if collection.count() == 0:

        ids = [
            record["id"]
            for record in records
        ]

        documents = [
            record["text"]
            for record in records
        ]

        metadatas = [
            {
                "source": record["source"],
                "category": record["category"]
            }
            for record in records
        ]

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        print("Knowledge base added to ChromaDB.")

    else:
        print("Existing ChromaDB collection loaded.")

    return collection


# -----------------------------------------
# SEARCH FUNCTION
# -----------------------------------------

def search(collection, query, top_k=3):

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\nTop 3 Results")
    print("-" * 60)

    for number, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1
    ):

        print(f"\nResult {number}")
        print(f"Document: {document}")
        print(f"Source: {metadata['source']}")
        print(f"Category: {metadata['category']}")
        print(f"Distance: {distance:.4f}")

    print("-" * 60)


# -----------------------------------------
# MAIN PROGRAM LOOP
# -----------------------------------------

def main():

    # Load records from JSON
    records = load_records(DATA_FILE)

    # Prepare ChromaDB collection
    collection = prepare_collection(records)

    print("\nCourse Knowledge Search Engine")
    print("Type 'exit' to close the program.")

    while True:

        # Get query from user
        query = input("\nEnter your question: ").strip()

        # Exit program
        if query.lower() == "exit":
            print("Program closed.")
            break

        # Reject empty input
        if not query:
            print("Please enter a question.")
            continue

        # Search for top 3 results
        search(collection, query, top_k=3)


# -----------------------------------------
# PROGRAM ENTRY POINT
# -----------------------------------------

if __name__ == "__main__":
    main()