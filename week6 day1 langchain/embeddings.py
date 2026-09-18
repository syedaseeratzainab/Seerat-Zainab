from langchain_huggingface import HuggingFaceEmbeddings


# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def generate_word_embeddings(text):

    words = text.split()

    word_embeddings = {}

    for word in words:

        vector = embeddings.embed_query(word)

        word_embeddings[word] = vector

    return word_embeddings


# Test
if __name__ == "__main__":

    text = input("Enter text: ").strip()

    word_embeddings = generate_word_embeddings(text)

    print("\nWord embeddings generated!")

    for word, vector in word_embeddings.items():

        print("\nWord:", word)
        print("Embedding size:", len(vector))
        print("First 385 values:", vector[:385])