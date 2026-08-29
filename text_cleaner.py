import re


def clean_text(text):

    if text is None:
        return ""

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove leading/trailing spaces
    text = text.strip()

    return text

