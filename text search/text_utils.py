# function to clean text
def prepare_keyword(keyword):
    return keyword.strip().lower()


# function to chexk if keyword is empty or not
def is_valid_keyword(keyword):
    return keyword.strip() != ""


# fuction if keyword exists it lowercases the text
def contains_keyword(text, keyword):
    return prepare_keyword(keyword) in text.lower()


# This section runs only when we directly run text_utils.py.
# It allows us to test our functions independently.
if __name__ == "__main__":

    # Test prepare_keyword()
    print("Prepared keyword:", prepare_keyword(" Python "))

    # Test is_valid_keyword()
    print("Valid keyword:", is_valid_keyword("python"))

    # Test an empty keyword
    print("Empty keyword:", is_valid_keyword(""))

    # Test contains_keyword()
    print(
        "Keyword found:",
        contains_keyword("Python is easy to learn.", "python")
    )