import re


def search_keyword_in_file(file_path, keyword, exact_word=False):
    """Search for a keyword in a text file."""

    matches = []

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, start=1):

        if exact_word:
            # Match the complete word only
            pattern = r"\b" + re.escape(keyword) + r"\b"
            occurrences = re.findall(pattern, line, re.IGNORECASE)
        else:
            occurrences = re.findall(
                re.escape(keyword),
                line,
                re.IGNORECASE
            )

        if occurrences:
            occurrence_count = len(occurrences)

            matches.append(
                (line_number, line.strip(), occurrence_count)
            )

    return matches