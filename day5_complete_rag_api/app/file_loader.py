from pathlib import Path
import csv
import json

from bs4 import BeautifulSoup
from docx import Document
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
    ".csv",
    ".json",
    ".md",
    ".html",
    ".htm"
}


def load_text_file(file_path: str) -> str:
    """
    Read a supported document and return its text.
    """

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".txt":
        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    if extension == ".pdf":
        return load_pdf(path)

    if extension == ".docx":
        return load_docx(path)

    if extension == ".csv":
        return load_csv(path)

    if extension == ".json":
        return load_json(path)

    if extension == ".md":
        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    if extension in {".html", ".htm"}:
        return load_html(path)

    raise ValueError(
        f"Unsupported file format: {extension}"
    )


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def load_docx(path: Path) -> str:
    document = Document(str(path))

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def load_csv(path: Path) -> str:
    rows = []

    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore",
        newline=""
    ) as file:

        reader = csv.reader(file)

        for row in reader:
            rows.append(" | ".join(row))

    return "\n".join(rows)


def load_json(path: Path) -> str:
    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        data = json.load(file)

    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )


def load_html(path: Path) -> str:
    html = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    return soup.get_text(
        separator="\n"
    )