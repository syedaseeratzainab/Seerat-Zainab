# ============================================================
# SAFE DOCUMENT SEARCH AND REPORT GENERATOR
# ============================================================


# ------------------------------------------------------------
# FUNCTION 1: clean_line()
# ------------------------------------------------------------

def clean_line(line):
    return line.strip()


# ------------------------------------------------------------
# FUNCTION 2: search_keyword()
# ------------------------------------------------------------

def search_keyword(filename, keyword):
    matches = []
    total_occurrences = 0

    with open(filename, "r", encoding="utf-8") as file:

        # Read the file one line at a time.
        for line_number, line in enumerate(file, start=1):

            # Clean the current line.
            clean = clean_line(line)

            # Ignore empty lines.
            if clean == "":
                continue

        
            if keyword.lower() in clean.lower():

                # Save the original line number and line.
                matches.append(
                    f"Line {line_number}: {clean}"
                )

                # Count how many times the keyword occurs
                # in this line.
                total_occurrences += clean.lower().count(
                    keyword.lower()
                )

    # Return all three results to the main program.
    return matches, len(matches), total_occurrences


# ------------------------------------------------------------
# FUNCTION 3: save_results()
# ------------------------------------------------------------

def save_results(filename, keyword, matches,
                 total_lines, total_occurrences):

    # using x mode to avoid overwriting an exisiting file.
    with open("search_results.txt", "x", encoding="utf-8") as file:

        file.write("===== SEARCH REPORT =====\n")

        # Save the source filename.
        file.write(f"Source File: {filename}\n")

        # Save the searched keyword.
        file.write(f"Keyword: {keyword}\n")

        # Save the number of matching lines.
        file.write(
            f"Total Matching Lines: {total_lines}\n"
        )

        # Save the total keyword occurrences.
        file.write(
            f"Total Keyword Occurrences: {total_occurrences}\n"
        )

        file.write("\nMatching Lines:\n")

        # If matching lines exist, save each one.
        if matches:

            for result in matches:
                file.write(result + "\n")

        # Otherwise save "No result found."
        else:
            file.write("No result found.\n")


# ------------------------------------------------------------
# FUNCTION 4: save_history()
# ------------------------------------------------------------

def save_history(filename, keyword, total_lines,
                 total_occurrences):

    with open("search_history.txt", "a", encoding="utf-8") as file:

        file.write(
            f"File: {filename} | "
            f"Keyword: {keyword} | "
            f"Matching Lines: {total_lines} | "
            f"Occurrences: {total_occurrences}\n"
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

while True:

    print("\n===================================")
    print("       SAFE DOCUMENT SEARCH")
    print("===================================")


    # --------------------------------------------------------
    # STEP 1: Ask for the input filename.
    # --------------------------------------------------------

    filename = input(
        "Enter the input filename (or type exit): "
    ).strip()

    if filename.lower() == "exit":
        print("Program ended.")
        break

    if filename == "":
        print("Filename cannot be empty.")
        continue


    # --------------------------------------------------------
    # STEP 2: Ask for the keyword.
    # --------------------------------------------------------

    keyword = input(
        "Enter a keyword (or type exit): "
    ).strip()

    if keyword.lower() == "exit":
        print("Program ended.")
        break

    if keyword == "":
        print("Keyword cannot be empty.")
        continue


    # --------------------------------------------------------
    # STEP 3: Search the document safely.
    # --------------------------------------------------------

    try:

        # Call our search function.
        matches, total_lines, total_occurrences = search_keyword(
            filename,
            keyword
        )


        # ----------------------------------------------------
        # STEP 4: Display the results.
        # ----------------------------------------------------

        print("\n===== SEARCH RESULTS =====")

        if matches:

            for result in matches:
                print(result)
        else:
            print("No result found.")
        print(
            "\nTotal matching lines:",
            total_lines
        )
        print(
            "Total keyword occurrences:",
            total_occurrences
        )


        # ----------------------------------------------------
        # STEP 5: Save the complete report.
        # ----------------------------------------------------

        try:

            save_results(
                filename,
                keyword,
                matches,
                total_lines,
                total_occurrences
            )

            print(
                "Report saved to search_results.txt."
            )


        # x mode error   
        except FileExistsError:

            print(
                "search_results.txt already exists."
            )

            print(
                "The existing report was not overwritten."
            )


        # ----------------------------------------------------
        # STEP 6: Save one-line search history.
        # ----------------------------------------------------

        save_history(
            filename,
            keyword,
            total_lines,
            total_occurrences
        )

        print(
            "Search summary added to search_history.txt."
        )


    # --------------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------------

    except FileNotFoundError:

        print(
            "Error: File not found."
        )
    except PermissionError:

        print(
            "Error: Permission denied."
        )

    except UnicodeDecodeError:

        print(
            "Error: File is not valid UTF-8."
        )

    except Exception as error:

        print(
            "An unexpected error occurred:",
            error
        )