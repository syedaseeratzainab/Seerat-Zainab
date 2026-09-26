from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask from the uploaded documents."
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of relevant chunks to retrieve."
    )


class Source(BaseModel):
    source: str
    chunk_id: int
    score: float
    text_preview: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


class UploadResponse(BaseModel):
    filename: str
    message: str
    chunks_created: int