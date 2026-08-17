import os
from datetime import datetime

from colorama import Fore, init

from file_utils import (
    get_document_files,
    search_keyword_in_file
)


# Initialize colored terminal output
init(autoreset=True)


def save_results(
    keyword,
    results,
    matching_files,
    total_matches,
    folder_path,
    exact_word
):
    """Save search results with a timestamp."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(
        "results/search_results.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n" + "=" * 70 + "\n")
        file.write(f"Search keyword: {keyword}\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Documents folder: {folder_path}\n")
        file.write(f"Exact-word search: {exact_word}\n")
        file.write(f"Matching files: {matching_files}\n")
        file.write(f"Total matches: {total_matches}\n")
        file.write("=" * 70 + "\n")

        for result in results:
            file.write(
                f"{result['file']} | "
                f"{result['location']} | "
                f"Occurrences: {result['count']} | "
                f"{result['text']}\n"
            )


def save_search_history(keyword, folder_path, exact_word):
    """Save each search to the search history file."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(
        "results/search_history.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{timestamp} | "
            f"Keyword: {keyword} | "
            f"Folder: {folder_path} | "
            f"Exact-word: {exact_word}\n"
        )


def show_extension_summary(folder_path):
    """Display the number of DOCX and PDF files."""

    document_files = get_document_files(folder_path)

    docx_count = 0
    pdf_count = 0

    for file_path in document_files:

        if file_path.lower().endswith(".docx"):
            docx_count += 1

        elif file_path.lower().endswith(".pdf"):
            pdf_count += 1

    print(Fore.CYAN + "\nFile Extension Summary")
    print("-" * 30)

    if docx_count == 0 and pdf_count == 0:
        print(Fore.YELLOW + "No DOCX or PDF files found.")
        return

    print(Fore.GREEN + f".docx: {docx_count} file(s)")
    print(Fore.GREEN + f".pdf: {pdf_count} file(s)")


def perform_search(keyword, folder_path, exact_word):
    """Search for the keyword in all DOCX and PDF files."""

    document_files = get_document_files(folder_path)

    if not document_files:
        print(
            Fore.RED
            + "No .docx or .pdf files were found "
            + "in the selected folder."
        )
        return

    results = []
    matching_files = set()
    total_matches = 0

    for file_path in document_files:

        matches = search_keyword_in_file(
            file_path,
            keyword,
            exact_word
        )

        if matches:

            filename = os.path.basename(file_path)

            matching_files.add(filename)

            for match in matches:

                result = {
                    "file": filename,
                    "location": match["location"],
                    "text": match["text"],
                    "count": match["count"]
                }

                results.append(result)

                total_matches += match["count"]

    if not results:

        print(
            Fore.YELLOW
            + f"\nNo matches found for '{keyword}'."
        )

        save_search_history(
            keyword,
            folder_path,
            exact_word
        )

        return

    # Sort results by filename and location
    results.sort(
        key=lambda result: (
            result["file"],
            result["location"]
        )
    )

    print(Fore.CYAN + "\nSearch Results")
    print("-" * 80)

    for result in results:

        print(
            Fore.GREEN
            + f"{result['file']}"
            + Fore.WHITE
            + f" | {result['location']}"
            + Fore.MAGENTA
            + f" | Occurrences: {result['count']}"
            + Fore.WHITE
            + f" | {result['text']}"
        )

    print("-" * 80)

    print(
        Fore.CYAN
        + f"Matching files: {len(matching_files)}"
    )

    print(
        Fore.CYAN
        + f"Total matches: {total_matches}"
    )

    save_results(
        keyword,
        results,
        len(matching_files),
        total_matches,
        folder_path,
        exact_word
    )

    save_search_history(
        keyword,
        folder_path,
        exact_word
    )

    print(
        Fore.GREEN
        + "\nResults saved to results/search_results.txt"
    )

    print(
        Fore.GREEN
        + "Search added to results/search_history.txt"
    )


def choose_documents_folder():
    """Allow the user to choose the documents folder."""

    default_folder = "documents"

    print(Fore.CYAN + "\nDocuments Folder")

    print(
        Fore.WHITE
        + f"Press Enter to use the default folder: {default_folder}"
    )

    folder_path = input(
        "Enter another folder path or press Enter: "
    ).strip()

    if folder_path == "":
        folder_path = default_folder

    if not os.path.exists(folder_path):

        print(
            Fore.RED
            + "The selected folder does not exist."
        )

        print(
            Fore.YELLOW
            + "Using the default documents folder instead."
        )

        folder_path = default_folder

    return folder_path


def main():
    """Run the Multi-File Keyword Search Tool."""

    os.makedirs("results", exist_ok=True)

    print(Fore.CYAN + "=" * 70)

    print(
        Fore.CYAN
        + "           MULTI-FILE KEYWORD SEARCH TOOL"
    )

    print(Fore.CYAN + "=" * 70)

    print(
        Fore.WHITE
        + "This version searches DOCX and PDF files."
    )

    folder_path = choose_documents_folder()

    show_extension_summary(folder_path)

    while True:

        keyword = input(
            Fore.WHITE
            + "\nEnter a keyword "
            + "(or type 'exit' to quit): "
        ).strip()

        if keyword.lower() == "exit":

            print(
                Fore.GREEN
                + "\nThank you for using the Keyword Search Tool!"
            )

            break

        if keyword == "":

            print(
                Fore.YELLOW
                + "Please enter a keyword."
            )

            continue

        exact_choice = input(
            "Use exact-word search? (y/n): "
        ).strip().lower()

        exact_word = exact_choice == "y"

        perform_search(
            keyword,
            folder_path,
            exact_word
        )


if __name__ == "__main__":
    main()