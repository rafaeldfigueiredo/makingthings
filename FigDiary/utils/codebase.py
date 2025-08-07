import sys
import os
import pyperclip # type: ignore # Import the pyperclip library for clipboard functionality

def aggregate_codebase(file_paths):
    """
    Reads code from specified files and aggregates it into 'codebase.txt'.
    After aggregation, it attempts to copy the content of 'codebase.txt' to the clipboard.

    Args:
        file_paths (list): A list of strings, where each string is the path to a code file.
    """
    output_filename = "codebase.txt"
    # Open the output file in append mode ('a'), which creates it if it doesn't exist,
    # or appends to it if it does. This ensures future runs add to the file
    # instead of overwriting it.
    # 'utf-8' encoding is used for broad compatibility with various characters.
    with open(output_filename, 'a', encoding='utf-8') as outfile:
        print(f"Aggregating code into '{output_filename}'...")
        for file_path in file_paths:
            # Check if the file exists before attempting to open it.
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found. Skipping this file.")
                continue # Move to the next file in the list

            try:
                # Open each input file in read mode.
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # Read the entire content of the file.
                    content = infile.read()

                    # Format the header as requested: # filename.py code #
                    # os.path.basename extracts just the file name from the full path.
                    header = f"# {os.path.basename(file_path)} code #\n"

                    # Write the header, followed by the file content, and then a newline
                    # for separation between files in the output.
                    outfile.write(header)
                    outfile.write(content)
                    outfile.write("\n\n") # Add extra newlines for better readability between files
                    print(f"Successfully added '{file_path}' to '{output_filename}'.")

            except Exception as e:
                # Catch any other potential errors during file reading (e.g., permission issues).
                print(f"An error occurred while reading '{file_path}': {e}")
                continue # Move to the next file

    print(f"\nCode aggregation complete. All available code saved to '{output_filename}'.")

    # --- Clipboard functionality ---
    try:
        # After writing to the file, read its entire content to copy to clipboard
        with open(output_filename, 'r', encoding='utf-8') as outfile_read:
            full_codebase_content = outfile_read.read()
            pyperclip.copy(full_codebase_content)
            print(f"Content of '{output_filename}' copied to clipboard!")
    except pyperclip.PyperclipException as e:
        print(f"Warning: Could not copy to clipboard. Please ensure you have a clipboard utility installed (e.g., xclip or xsel on Linux). Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while trying to copy to clipboard: {e}")


if __name__ == "__main__":
    # sys.argv is the list of command-line arguments.
    # sys.argv[0] is the script name itself (e.g., 'codebase.py').
    # So, we slice from index 1 onwards to get only the file paths provided by the user.
    files_to_process = sys.argv[1:]

    if not files_to_process:
        # If no file paths are provided, print usage instructions.
        print("Usage: python codebase.py <file1.py> <file2.js> <another_file.txt> ...")
        print("Please provide at least one file path to aggregate.")
    else:
        # If file paths are provided, call the aggregation function.
        aggregate_codebase(files_to_process)
