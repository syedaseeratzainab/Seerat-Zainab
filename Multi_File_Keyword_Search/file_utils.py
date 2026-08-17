import os
import re
from docx import Document
from pypdf import PdfReader
from docx import Document
from pypdf import PdfReader


def search_keyword_in_file(file_path, keyword, exact_word=False):
    """Search for a keyword in a DOCX or PDF file."""

    matches = []

    if file_path.lower().endswith(".docx"):
        document = Document(file_path)

        for paragraph_number, paragraph in enumerate(
            document.paragraphs, start=1
        ):
            line = paragraph.text.strip()

            if not line:
                continue

            if exact_word:
                pattern = r"\b" + re.escape(keyword) + r"\b"
                occurrences = re.findall(
                    pattern, line, re.IGNORECASE
                )
            else:
                occurrences = re.findall(
                    re.escape(keyword),
                    line,
                    re.IGNORECASE
                )

            if occurrences:
                matches.append({
                    "file": file_path,
                    "location": f"Paragraph {paragraph_number}",
                    "text": line,
                    "count": len(occurrences)
                })

    elif file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            for line in text.splitlines():
                line = line.strip()

                if not line:
                    continue

                if exact_word:
                    pattern = r"\b" + re.escape(keyword) + r"\b"
                    occurrences = re.findall(
                        pattern, line, re.IGNORECASE
                    )
                else:
                    occurrences = re.findall(
                        re.escape(keyword),
                        line,
                        re.IGNORECASE
                    )

                if occurrences:
                    matches.append({
                        "file": file_path,
                        "location": f"Page {page_number}",
                        "text": line,
                        "count": len(occurrences)
                    })

    return matches


def get_document_files(folder_path):
    """Get all DOCX and PDF files from the documents folder."""

    if not os.path.exists(folder_path):
        raise FileNotFoundError(
            f"Folder not found: {folder_path}"
        )

    files = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            if filename.lower().endswith((".docx", ".pdf")):
                files.append(file_path)

    files.sort()

    return files

def search_documents(folder_path, keyword, exact_word=False):
    """Search for a keyword in all DOCX and PDF files."""

    document_files = get_document_files(folder_path)

    all_matches = []

    for file_path in document_files:
        matches = search_keyword_in_file(
            file_path,
            keyword,
            exact_word
        )

        all_matches.extend(matches)

    return all_matches, len(document_files)