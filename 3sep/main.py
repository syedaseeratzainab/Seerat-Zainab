import requests
from bs4 import BeautifulSoup
import json
import re

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


# ============================================================
# CONFIGURATION
# ============================================================

JSON_FILE = "wikipedia_chunks.json"

QDRANT_PATH = "qdrant_db"

COLLECTION_NAME = "wikipedia_chunks"

MODEL_NAME = "all-MiniLM-L6-v2"

# Required settings
CHUNK_SIZE = 10
OVERLAP = 2
TOP_K = 3


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    # --------------------------------------------------------
    # Remove Wikipedia citation markers
    # Examples:
    # [1]
    # [23]
    # [note 1]
    # [a]
    # --------------------------------------------------------

    text = re.sub(
        r"\[(?:\d+|note\s+\d+|[a-zA-Z])\]",
        "",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Remove citation ranges
    # Examples:
    # [1-3]
    # [12–15]
    # --------------------------------------------------------

    text = re.sub(
        r"\[\d+\s*[-–]\s*\d+\]",
        "",
        text
    )

    # --------------------------------------------------------
    # Replace non-breaking spaces
    # --------------------------------------------------------

    text = text.replace(
        "\xa0",
        " "
    )

    # --------------------------------------------------------
    # Remove excessive whitespace
    # --------------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # --------------------------------------------------------
    # Remove spaces before punctuation
    # --------------------------------------------------------

    text = re.sub(
        r"\s+([,.!?;:])",
        r"\1",
        text
    )

    # --------------------------------------------------------
    # Clean spaces inside parentheses
    # --------------------------------------------------------

    text = re.sub(
        r"\(\s+",
        "(",
        text
    )

    text = re.sub(
        r"\s+\)",
        ")",
        text
    )

    # --------------------------------------------------------
    # Remove spaces around hyphens
    # --------------------------------------------------------

    text = re.sub(
        r"\s*[-–]\s*",
        "–",
        text
    )

    return text.strip()


# ============================================================
# FETCH WIKIPEDIA ARTICLE
# ============================================================

def fetch_wikipedia_document(topic: str):

    # Convert:
    #
    # Cristiano Ronaldo
    #
    # into:
    #
    # Cristiano_Ronaldo

    topic_clean = topic.replace(
        " ",
        "_"
    )

    url = (
        "https://en.wikipedia.org/wiki/"
        + topic_clean
    )

    headers = {
        "User-Agent": (
            "WikipediaSemanticSearch/1.0 "
            "(Educational Project)"
        )
    }

    print("\nConnecting to Wikipedia...")

    # --------------------------------------------------------
    # Try up to 3 times
    # --------------------------------------------------------

    response = None

    for attempt in range(3):

        try:

            print(
                f"Attempt {attempt + 1}/3..."
            )

            response = requests.get(
                url,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()

            print(
                f"Status Code: {response.status_code}"
            )

            print(
                "Status: Wikipedia page loaded successfully"
            )

            break

        except requests.exceptions.Timeout:

            print(
                "Wikipedia request timed out."
            )

            if attempt == 2:

                print(
                    "Wikipedia could not be reached "
                    "after 3 attempts."
                )

                return None

        except requests.exceptions.RequestException as e:

            print(
                f"Request error: {e}"
            )

            return None

    if response is None:

        return None

    # ========================================================
    # PARSE HTML
    # ========================================================

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # ========================================================
    # GET ARTICLE TITLE
    # ========================================================

    title_tag = soup.find("h1")

    if title_tag:

        title = title_tag.get_text(
            " ",
            strip=True
        )

    else:

        title = topic

    print(
        f"Title: {title}"
    )

    # ========================================================
    # FIND ARTICLE CONTENT
    # ========================================================

    content_div = soup.select_one(
        "#mw-content-text .mw-parser-output"
    )

    # Fallback
    if content_div is None:

        content_div = soup.select_one(
            "#mw-content-text"
        )

    if content_div is None:

        print(
            "Wikipedia article content not found."
        )

        return None

    # ========================================================
    # REMOVE UNWANTED CONTENT
    # ========================================================

    unwanted = content_div.select(
        "table, "
        ".reference, "
        ".reflist, "
        ".navbox, "
        ".vertical-navbox, "
        ".metadata, "
        ".ambox, "
        ".infobox, "
        ".sidebar, "
        ".mw-editsection, "
        "style, "
        "script, "
        "noscript"
    )

    for element in unwanted:

        element.decompose()

    # ========================================================
    # EXTRACT PARAGRAPHS AND LIST ITEMS
    # ========================================================

    elements = content_div.find_all(
        ["p", "li"]
    )

    texts = []

    for element in elements:

        text = element.get_text(
            " ",
            strip=True
        )

        text = clean_text(text)

        if text:

            texts.append(text)

    if not texts:

        print(
            "No textual content found."
        )

        return None

    print(
        f"Paragraphs/list items extracted: "
        f"{len(texts)}"
    )

    # ========================================================
    # COMBINE TEXT
    # ========================================================

    full_text = " ".join(texts)

    return {
        "content": full_text,
        "topic": topic,
        "title": title,
        "url": url
    }


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(
    document,
    chunk_size=CHUNK_SIZE,
    overlap=OVERLAP
):

    chunks = []

    text = document["content"]

    words = text.split()

    if not words:

        return []

    # --------------------------------------------------------
    # Validate overlap
    # --------------------------------------------------------

    if overlap >= chunk_size:

        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    # --------------------------------------------------------
    # Calculate step
    #
    # Example:
    #
    # chunk size = 10
    # overlap = 2
    #
    # step = 8
    # --------------------------------------------------------

    step = chunk_size - overlap

    chunk_index = 0

    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    for start in range(
        0,
        len(words),
        step
    ):

        chunk_words = words[
            start:start + chunk_size
        ]

        if not chunk_words:

            break

        chunk_text = " ".join(
            chunk_words
        )

        chunk = {
            "chunk_id": chunk_index + 1,

            "text": chunk_text,

            "metadata": {
                "topic": document["topic"],
                "title": document["title"],
                "url": document["url"],
                "chunk_index": chunk_index,
                "word_count": len(chunk_words)
            }
        }

        chunks.append(chunk)

        chunk_index += 1

        # ----------------------------------------------------
        # Stop after final chunk
        # ----------------------------------------------------

        if start + chunk_size >= len(words):

            break

    return chunks


# ============================================================
# SAVE CHUNKS TO JSON
# ============================================================

def save_chunks(
    path,
    chunks
):

    try:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                chunks,
                file,
                ensure_ascii=False,
                indent=4
            )

        print(
            f"\nChunks saved to: {path}"
        )

    except OSError as e:

        print(
            f"Error saving JSON: {e}"
        )


# ============================================================
# CREATE QDRANT CLIENT
# ============================================================

def create_qdrant():

    print(
        "\nCreating local Qdrant database..."
    )

    client = QdrantClient(
        path=QDRANT_PATH
    )

    # --------------------------------------------------------
    # Check existing collections
    # --------------------------------------------------------

    collections = client.get_collections()

    existing_names = [
        collection.name
        for collection in collections.collections
    ]

    # --------------------------------------------------------
    # Create collection if it doesn't exist
    # --------------------------------------------------------

    if COLLECTION_NAME not in existing_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,

            vectors_config=VectorParams(
                # all-MiniLM-L6-v2 = 384 dimensions
                size=384,

                distance=Distance.COSINE
            )
        )

        print(
            "Qdrant collection created."
        )

    else:

        print(
            "Qdrant collection already exists."
        )

    return client


# ============================================================
# GENERATE EMBEDDINGS
# ============================================================

def generate_embeddings(
    chunks,
    model
):

    if not chunks:

        return []

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print(
        "\nGenerating embeddings..."
    )

    embeddings = model.encode(
        texts,

        normalize_embeddings=True,

        show_progress_bar=True
    )

    print(
        "Embeddings generated successfully."
    )

    return embeddings


# ============================================================
# STORE DATA IN QDRANT
# ============================================================

def store_in_qdrant(
    client,
    chunks,
    embeddings
):

    if not chunks:

        print(
            "No chunks available for Qdrant."
        )

        return

    points = []

    for index, chunk in enumerate(chunks):

        point = PointStruct(

            id=chunk["chunk_id"],

            vector=embeddings[index].tolist(),

            payload={
                "text": chunk["text"],

                "topic": chunk["metadata"]["topic"],

                "title": chunk["metadata"]["title"],

                "url": chunk["metadata"]["url"],

                "chunk_index": (
                    chunk["metadata"]["chunk_index"]
                ),

                "word_count": (
                    chunk["metadata"]["word_count"]
                )
            }
        )

        points.append(point)

    # --------------------------------------------------------
    # Insert into Qdrant
    # --------------------------------------------------------

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points
    )

    print(
        f"Stored {len(points)} chunks in Qdrant."
    )


# ============================================================
# SEMANTIC SEARCH
# ============================================================

def semantic_search(
    client,
    model,
    question,
    top_k=TOP_K
):

    # --------------------------------------------------------
    # Create embedding for current question
    # --------------------------------------------------------

    query_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    # --------------------------------------------------------
    # Search Qdrant
    # --------------------------------------------------------

    results = client.query_points(

        collection_name=COLLECTION_NAME,

        query=query_embedding.tolist(),

        limit=top_k,

        with_payload=True
    )

    return results.points


# ============================================================
# QUESTION LOOP
# ============================================================

def question_loop(
    client,
    model
):

    print("\n")

    print("=" * 70)

    print("SEMANTIC SEARCH")

    print("=" * 70)

    print(
        "\nAsk questions about the stored Wikipedia article."
    )

    print(
        "Type 'exit' to stop."
    )

    while True:

        question = input(
            "\nQuestion: "
        ).strip()

        # ----------------------------------------------------
        # Reject empty question
        # ----------------------------------------------------

        if not question:

            print(
                "Please enter a question."
            )

            continue

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if question.lower() == "exit":

            print(
                "\nProgram stopped."
            )

            break

        print(
            f"\nSearching for: {question}"
        )

        # ----------------------------------------------------
        # Perform semantic search
        # ----------------------------------------------------

        results = semantic_search(
            client,
            model,
            question,
            TOP_K
        )

        if not results:

            print(
                "No results found."
            )

            continue

        print("\n")

        print("=" * 70)

        print("TOP SEMANTIC SEARCH RESULTS")

        print("=" * 70)

        # ----------------------------------------------------
        # Display results
        # ----------------------------------------------------

        for index, result in enumerate(
            results,
            start=1
        ):

            payload = result.payload

            print(
                f"\nResult {index}"
            )

            print(
                f"Similarity Score: "
                f"{result.score:.4f}"
            )

            print(
                f"Topic: "
                f"{payload.get('topic')}"
            )

            print(
                f"Title: "
                f"{payload.get('title')}"
            )

            print(
                f"URL: "
                f"{payload.get('url')}"
            )

            print(
                f"Chunk Index: "
                f"{payload.get('chunk_index')}"
            )

            print(
                f"Word Count: "
                f"{payload.get('word_count')}"
            )

            print(
                "\nText:\n"
                f"{payload.get('text')}"
            )

            print(
                "-" * 70
            )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 70)

    print("WIKIPEDIA SEMANTIC SEARCH SYSTEM")

    print("=" * 70)

    # ========================================================
    # GET WIKIPEDIA TOPIC
    # ========================================================

    topic = input(
        "\nEnter Wikipedia topic: "
    ).strip()

    if not topic:

        print(
            "No topic provided. Exiting."
        )

        return

    # ========================================================
    # FETCH WIKIPEDIA ARTICLE
    # ========================================================

    document = fetch_wikipedia_document(
        topic
    )

    if document is None:

        print(
            "Failed to fetch Wikipedia document."
        )

        return

    # ========================================================
    # CREATE CHUNKS
    # ========================================================

    print(
        "\nCleaning text and creating chunks..."
    )

    chunks = create_chunks(
        document,

        chunk_size=CHUNK_SIZE,

        overlap=OVERLAP
    )

    if not chunks:

        print(
            "No chunks created."
        )

        return

    print(
        f"Created {len(chunks)} chunks."
    )

    print(
        f"Chunk size: {CHUNK_SIZE} words"
    )

    print(
        f"Overlap: {OVERLAP} words"
    )

    # ========================================================
    # SAVE JSON
    # ========================================================

    save_chunks(
        JSON_FILE,
        chunks
    )

    # ========================================================
    # LOAD SENTENCE TRANSFORMER
    # ========================================================

    print(
        "\nLoading embedding model..."
    )

    print(
        f"Model: {MODEL_NAME}"
    )

    model = SentenceTransformer(
        MODEL_NAME
    )

    print(
        "Embedding model loaded successfully."
    )

    # ========================================================
    # CREATE QDRANT
    # ========================================================

    client = create_qdrant()

    # ========================================================
    # GENERATE EMBEDDINGS
    # ========================================================

    embeddings = generate_embeddings(
        chunks,
        model
    )

    # ========================================================
    # STORE IN QDRANT
    # ========================================================

    store_in_qdrant(
        client,
        chunks,
        embeddings
    )

    # ========================================================
    # START QUESTION LOOP
    # ========================================================

    question_loop(
        client,
        model
    )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()