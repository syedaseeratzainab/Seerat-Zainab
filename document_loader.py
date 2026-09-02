import os
from pypdf import PdfReader
from docx import Document


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return [{
        "content": text,
        "source": file_path,
        "page": None
    }]


def load_pdf(file_path):

    reader = PdfReader(file_path)

    document = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() 

        document.append({
            "content": text,
            "source": file_path,
            "page": page_number + 1
        })

    return document


def load_docx(file_path):

    doc = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
    )

    return [{
        "content": text,
        "source": file_path,
        "page": None
    }]

def load_document(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return load_txt(file_path)

    elif extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    else:
        raise ValueError("Unsupported file type")
