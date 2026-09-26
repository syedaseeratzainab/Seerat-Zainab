from fastapi import FastAPI

from .routes import router


app = FastAPI(
    title="Day 5 Complete RAG Question Answering API",
    description=(
        "A complete RAG API using FastAPI, "
        "ChromaDB and Hugging Face."
    ),
    version="1.0.0"
)


app.include_router(
    router
)


@app.get("/")
def root():
    return {
        "message": "Complete RAG API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }