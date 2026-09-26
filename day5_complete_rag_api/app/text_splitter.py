def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
):
    """
    Split text into overlapping chunks.
    """

    if not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks