import os
from datetime import datetime

from colorama import Fore, Style, init

from file_utils import get_text_files, get_extension_summary
from text_utils import search_keyword_in_file


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

    with open("results/search_results.txt", "a", encoding="utf-8") as file:
        file.write("\n" + "=" * 70 + "\n")
        file.write(f"Search keyword: {keyword}\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Documents folder: {folder_path}\n")
        file.write(f"Exact-word search: {exact_word}\n")
        file.write(f"Matching files: {matching_files}\n")
        file.write(f"Total matches: {total_matches}\n")
        file.write("=" * 70 + "\n")

        for filename, line_number, line_text, occurrence_count in results:
            file.write(
                f"{filename} | Line {line_number} | "
                f"Occurrences: {occurrence_count} | {line_text}\n"
            )


def save_search_history(keyword, folder_path, exact_word):
    """Save each search to the search history file."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("results/search_history.txt", "a", encoding="utf-8") as file:
        file.write(
            f"{timestamp} | Keyword: {keyword} | "
            f"Folder: {folder_path} | Exact-word: {exact_word}\n"
        )


def show_extension_summary(folder_path):
    """Display the file-extension summary."""

    extension_summary = get_extension_summary(folder_path)

    print(Fore.CYAN + "\nFile Extension Summary")
    print("-" * 30)

    if not extension_summary:
        print(Fore.YELLOW + "No files found.")
        return

    for extension, count in sorted(extension_summary.items()):
        print(Fore.GREEN + f"{extension}: {count} file(s)")


def perform_search(keyword, folder_path, exact_word):
    """Search for the keyword in all text files."""

    text_files = get_text_files(folder_path)

    if not text_files:
        print(
            Fore.RED
            + "No .txt files were found in the selected folder."
        )
        return

    results = []
    matching_files = 0
    total_matches = 0

    for file_path in text_files:
        matches = search_keyword_in_file(
            file_path,
            keyword,
            exact_word
        )

        if matches:
            matching_files += 1
            total_matches += sum(
                match[2] for match in matches
            )

            filename = os.path.basename(file_path)

            for line_number, line_text, occurrence_count in matches:
                results.append(
                    (
                        filename,
                        line_number,
                        line_text,
                        occurrence_count
                    )
                )

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

    # Sort results by filename and then by line number
    results.sort(key=lambda result: (result[0], result[1]))

    print(Fore.CYAN + "\nSearch Results")
    print("-" * 75)

    for filename, line_number, line_text, occurrence_count in results:
        print(
            Fore.GREEN
            + f"{filename}"
            + Fore.WHITE
            + f" | Line {line_number}"
            + Fore.MAGENTA
            + f" | Occurrences: {occurrence_count}"
            + Fore.WHITE
            + f" | {line_text}"
        )

    print("-" * 75)
    print(
        Fore.CYAN
        + f"Matching files: {matching_files}"
    )
    print(
        Fore.CYAN
        + f"Total matches: {total_matches}"
    )

    save_results(
        keyword,
        results,
        matching_files,
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
            print(Fore.YELLOW + "Please enter a keyword.")
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