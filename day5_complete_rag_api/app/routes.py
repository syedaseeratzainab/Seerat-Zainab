from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File
)

from .schemas import (
    AskRequest,
    AskResponse,
    UploadResponse
)

from .rag_service import ask_question

from .file_loader import (
    load_text_file,
    SUPPORTED_EXTENSIONS
)

from .text_cleaner import clean_text
from .text_splitter import split_text
from .embeddings import generate_embeddings

from .vector_store import add_to_vector_store


# Create FastAPI router
router = APIRouter()


# Folder where uploaded files will be saved
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# UPLOAD FILE
# --------------------------------------------------

@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_file(
    file: UploadFile = File(...)
):

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    # Get file extension
    extension = Path(
        file.filename
    ).suffix.lower()

    # Check supported file format
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format. "
                "Supported formats: "
                "PDF, DOCX, TXT, CSV, JSON, MD and HTML."
            )
        )

    # Create file path
    file_path = DATA_DIR / file.filename

    try:

        # Read uploaded file
        file_content = await file.read()

        # Save file
        with open(
            file_path,
            "wb"
        ) as saved_file:

            saved_file.write(
                file_content
            )

        # Extract text from file
        text = load_text_file(
            str(file_path)
        )

        # Check extracted text
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "The uploaded file contains "
                    "no readable text."
                )
            )

        # Clean text
        text = clean_text(text)

        # Split text into chunks
        chunks = split_text(
            text,
            chunk_size=500,
            overlap=50
        )

        # Check chunks
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks could be created."
            )

        # Generate embeddings
        embeddings = generate_embeddings(
            chunks
        )

        # Create metadata for each chunk
        metadata = []

        for index in range(
            len(chunks)
        ):

            metadata.append(
                {
                    "source": file.filename,
                    "chunk_id": index
                }
            )

        # Store chunks and embeddings
        # in ChromaDB
        add_to_vector_store(
            embeddings,
            chunks,
            metadata
        )

        # Return successful response
        return {
            "filename": file.filename,
            "message": (
                "File uploaded and indexed successfully."
            ),
            "chunks_created": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"File processing error: {str(error)}"
            )
        )


# --------------------------------------------------
# ASK QUESTION
# --------------------------------------------------

@router.post(
    "/ask",
    response_model=AskResponse
)
def ask(
    request: AskRequest
):

    try:

        # Send question to RAG pipeline
        result = ask_question(
            request.question,
            request.top_k
        )

        return result

    except RuntimeError as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Unexpected error: {str(error)}"
            )
        )