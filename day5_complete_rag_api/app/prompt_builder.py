def build_prompt(
    question: str,
    retrieved_chunks: list
) -> str:
    """
    Build the prompt using retrieved document chunks.
    """

    context_parts = []

    for index, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        context_parts.append(
            f"""
Source {index}: {chunk['source']}
Chunk ID: {chunk['chunk_id']}

{chunk['text']}
"""
        )

    context = "\n".join(
        context_parts
    )

    prompt = f"""
You are a helpful RAG assistant.

Answer the user's question using only the
information provided in the context.

If the answer cannot be found in the context,
say:

"The available documents do not contain enough
information to answer this question."

Do not use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt.strip()