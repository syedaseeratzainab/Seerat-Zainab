#IMPORTING FUNCTIONS
from text_utils import prepare_keyword, is_valid_keyword

from file_utils import search_folder, count_matching_files, save_results


# Store the location of the folder containing our text files.
documents_folder = "documents"

# Store the location where the search results will be saved.
output_file = "results/search_results.txt"

# These are the four keywords we need to search.
keywords = ["python", "rag", "AI", "java"]

# Create an empty list to store all search results.
all_results = []


# Search for each keyword one by one.
for keyword in keywords:


    keyword = prepare_keyword(keyword)
    if not is_valid_keyword(keyword):

        print("Invalid keyword.")
        continue

    # Search all text files for the keyword.
    matching_files = search_folder(documents_folder, keyword)

    # Count how many files contain the keyword.
    count = count_matching_files(documents_folder, keyword)

    # Display the search information on the screen.
    print("\nSearching for:", keyword)
    print("Number of matching files:", count)

    # Create a heading for this keyword in the results.
    all_results.append("Search keyword: " + keyword)
    all_results.append("Matching files: " + str(count))

    # Check whether any files matched.
    if count > 0:

        # Display and save each matching file.
        for file in matching_files:
            print("Found in:", file)
            all_results.append("Found in: " + file)

    else:

        # Display and save a message when no file matches.
        print("No matching files found.")
        all_results.append("No matching files found.")

    # Add a blank line between different searches.
    all_results.append("")


# Save all search results into the results folder.
save_results(all_results, output_file)


# Confirm that the results were saved.
print("\nAll search results saved to:", output_file)

