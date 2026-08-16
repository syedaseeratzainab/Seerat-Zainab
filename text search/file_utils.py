import os


# Function to find all text files inside a folder
def get_text_files(folder_path):

    #list to store path of files inside folder
    text_files = []

    # Go through everything inside the folder.
    for filename in os.listdir(folder_path):

        # Check whether the file ends with .txt
        if filename.endswith(".txt"):

            # Create the complete path of the file.
            file_path = os.path.join(folder_path, filename)

            # Add the file path to our list.
            text_files.append(file_path)

    # Return the list of text files.
    return text_files


# Tfunction to search for keyword inside only one text file
def search_file(file_path, keyword):
    #reading file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Checking whether the keyword exists in the file.
    if keyword.lower() in content.lower():
        return True
    return False

# function to find keyword inside all files in folder
def search_folder(folder_path, keyword):

    # Get all text files from the folder.
    files = get_text_files(folder_path)

    # Create an empty list to store files
    # where the keyword is found.
    matching_files = []

    # Check each text file one by one.
    for file in files:

        # Use search_file() to check whether
        # the keyword exists in this file.
        if search_file(file, keyword):

            # Add the file to the matching files list.
            matching_files.append(file)

    # Return the list of files containing the keyword.
    return matching_files

# functio to count how many files contain keyword
def count_matching_files(folder_path, keyword):

    # Search the folder for files containing the keyword.
    matching_files = search_folder(folder_path, keyword)

    # Count the number of matching files.
    count = len(matching_files)

    # Return the total number of matching files.
    return count

# function to save search result 
def save_results(results, output_file):

    # Open the output file in write mode.
    with open(output_file, "w", encoding="utf-8") as file:

        # Write each result into the file.
        for result in results:

            # Write the result and move to the next line.
            file.write(result + "\n")

# This section runs only when we directly run file_utils.py.
if __name__ == "__main__":

    # Path of our documents folder.
    folder = "documents"

    # Get all text files from the documents folder.
    files = get_text_files(folder)

    # Display the files that were found.
    print("Text files found:")

    for file in files:
        print(file)

    # Test searching for the keyword "python" in the first file.
    result = search_file(files[0], "python")

    # Display whether the keyword was found.
    print("Python found in first file:", result)
        # Test searching for "python" in the entire documents folder.
    matching_files = search_folder("documents", "python")

    # Display the files where the keyword was found.
    print("Files containing python:")

    for file in matching_files:
        print(file)

            # Test counting the files that contain "python".
    count = count_matching_files("documents", "python")

    # Display the number of matching files.
    print("Number of files containing python:", count)

        # Test saving the matching files into the results folder.
    save_results(
        matching_files,
        "results/search_results.txt"
    )

    # Display a message after saving the results.
    print("Search results saved successfully.")

    