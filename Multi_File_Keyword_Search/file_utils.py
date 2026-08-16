import os


def get_text_files(folder_path):
    """Return a list of all .txt files in a folder."""
  #To handle empyty files
    if not os.path.exists(folder_path):
        return []
  #find txt files and store their path 
    text_files = []

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            text_files.append(file_path)

    return text_files


def get_extension_summary(folder_path):
    """Count files according to their extensions."""

    if not os.path.exists(folder_path):
        return {}

    extension_summary = {}

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            extension = os.path.splitext(file_name)[1].lower()

            if extension:
                extension_summary[extension] = (
                    extension_summary.get(extension, 0) + 1
                )

    return extension_summary