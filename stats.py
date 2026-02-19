"""
Little script that update all the number of files, lines and words in the README.
"""

from typing import Optional, Any

import re
import os


parts_titles_to_folder: dict[str, str] = {
    "## Une partie traitant des types de récits": "type_de_recit",
    "## Une partie traitant du support de récit": "support_de_recit",
    "## Une partie traitant du monde / univers": "monde_univers",
    "## Une partie traitant de l'ambiance et des thèmes": "ambiance_theme",
    "## Une partie traitant des intrigues et scénarios": "intrigues_scenarios",
    "## Une partie traitant des personnages et des êtres vivants": "personnages_etre_vivants",
}

fields_to_replace: dict[str, Optional[tuple[int, int]]] = {
    "total_number_of_files": None,
    "total_number_of_words": None,
    "total_number_of_lines": None,
}

fields_to_replace_value: dict[str, int] = {}

DIR_TO_EXCLUDE: list[str] = [
    ".git",
    "__pycache__",
    ".venv",
    ".gemini",
    "brain",
]


def explore_recursively(from_folder: str = "./") -> dict[str, Any]:
    """
    Function to explore recursively

    folders are dicts
    files are tuple[int (number of lines), int (number of words)]
    """

    # Prepare the result dictionary
    result: dict[str, Any] = {}

    # Use try / except block to only skip if error instead of crashing
    try:
        # Loop through all the entries in the folder
        for entry in os.scandir(from_folder):
            # If the entry is a directory, recursively call the function
            if entry.is_dir():
                # Skip some directories
                if entry.name not in DIR_TO_EXCLUDE:
                    # Then, explore recursively the new discovered directory
                    result[entry.name] = explore_recursively(entry.path)

            # If the entry is a file and ends with .md we process it
            elif entry.is_file() and entry.name.endswith(".md"):
                # Use try / except block to only skip if error instead of crashing
                try:
                    # Cleanly open the file
                    with open(entry.path, "r", encoding="utf-8") as f:
                        # Read the content of the file
                        content: str = f.read()

                        # Get all the lines
                        lines_list: list[str] = content.splitlines()

                        # Count only non-empty lines
                        lines: int = len([line for line in lines_list if line.strip()])

                        # Count the number of words
                        words: int = len(re.findall(r"\w+", content))

                        # Add the number of lines and words to the result
                        result[entry.name] = (lines, words)

                # If there is an error, skip the file
                except (IOError, UnicodeDecodeError):
                    pass

    # If there is an error, skip the directory
    except OSError:
        pass

    # Return the result
    return result


def collect_stats(data: dict[str, Any]) -> tuple[int, int, int]:
    """
    Helper function to collect recursively statistics from the data dictionary
    """
    # Initialize the statistics
    files, lines, words = 0, 0, 0

    # Loop through all the values in the data dictionary
    for value in data.values():
        # If the value is a tuple, it's a file
        if isinstance(value, tuple):
            # Increment the number of files
            files += 1
            # Add the number of lines
            lines += value[0]
            # Add the number of words
            words += value[1]
        # If the value is a dictionary, it's a folder
        elif isinstance(value, dict):
            # Recursively call the function to get folder stats
            files_count, lines_count, words_count = collect_stats(value)
            # Add the folder statistics to the current ones
            files += files_count
            lines += lines_count
            words += words_count

    # Return the collected statistics
    return files, lines, words


def replace_section(
    match: re.Match[str], n_files: int, n_lines: int, n_words: int
) -> str:
    """
    Helper function to replace section content with updated badges
    """
    # Get the header of the section
    header = match.group(1)
    # Get the content of the section
    content = match.group(2)
    # Get the footer of the section
    footer = match.group(3)

    # Replace the number of files badge in the section
    content = re.sub(
        r"(Contenu-)\d+(_fichiers?-blue)",
        lambda m: (
            f"{m.group(1)}{n_files}_{'fichier' if n_files <= 1 else 'fichiers'}-blue"
        ),
        content,
    )
    # Replace the number of lines badge in the section
    content = re.sub(
        r"(Taille-)\d+(_lignes-brightgreen)", rf"\g<1>{n_lines}\g<2>", content
    )
    # Replace the number of words badge in the section
    content = re.sub(
        r"(Taille-)\d+(_mots-brightgreen)", rf"\g<1>{n_words}\g<2>", content
    )
    # Return the updated section
    return header + content + footer


def main() -> None:
    """
    Main function
    """

    # Prepare the fields_to_replace automatic content from parts_titles_to_folder
    for parts_folder in parts_titles_to_folder.values():
        # Number of files
        fields_to_replace[f"{parts_folder}_number_of_files"] = None

        # Number of lines
        fields_to_replace[f"{parts_folder}_number_of_lines"] = None

        # Number of words
        fields_to_replace[f"{parts_folder}_number_of_words"] = None

    # Get the repo structure and stats
    repo_data: dict[str, Any] = explore_recursively(".")

    # Calculate statistics
    total_files: int = 0
    # Initialize total lines
    total_lines: int = 0
    # Initialize total words
    total_words: int = 0

    # Loop through all the parts folders
    for folder_name in parts_titles_to_folder.values():
        # Initialize the folder statistics
        folder_files: int = 0
        # Initialize the folder lines
        folder_lines: int = 0
        # Initialize the folder words
        folder_words: int = 0

        # Crawl repo_data to find statistics for this specific folder
        if folder_name in repo_data:
            # Use the helper function to collect statistics
            folder_files, folder_lines, folder_words = collect_stats(
                repo_data[folder_name]
            )

        # Update the fields to replace values with the folder statistics
        fields_to_replace_value[f"{folder_name}_number_of_files"] = folder_files
        # Update the lines field
        fields_to_replace_value[f"{folder_name}_number_of_lines"] = folder_lines
        # Update the words field
        fields_to_replace_value[f"{folder_name}_number_of_words"] = folder_words

        # Add the folder statistics to the total
        total_files += folder_files
        # Add the folder lines to the total
        total_lines += folder_lines
        # Add the folder words to the total
        total_words += folder_words

    # Update the total fields to replace values
    fields_to_replace_value["total_number_of_files"] = total_files
    # Update the total lines field
    fields_to_replace_value["total_number_of_lines"] = total_lines
    # Update the total words field
    fields_to_replace_value["total_number_of_words"] = total_words

    # Get the README file content
    with open("README.md", "r", encoding="utf-8") as f:
        # Read the readme text
        readme_text = f.read()

    # Update total badges (top of the file)
    # We look for badges before the first section title
    first_title_pos = readme_text.find("## ")
    # Check if a title was found
    if first_title_pos == -1:
        # If no title, the entire text is the prefix
        prefix = readme_text
        # And the suffix is empty
        suffix = ""
    # If a title was found
    else:
        # Get the text before the title
        prefix = readme_text[:first_title_pos]
        # Get the text after the title
        suffix = readme_text[first_title_pos:]

    # Replace the total number of files badge
    prefix = re.sub(
        r"(Contenu-)\d+(_fichiers?-blue)",
        lambda m: (
            f"{m.group(1)}{total_files}_{'fichier' if total_files <= 1 else 'fichiers'}-blue"
        ),
        prefix,
    )
    # Replace the total number of lines badge
    prefix = re.sub(
        r"(Taille-)\d+(_lignes-brightgreen)", rf"\g<1>{total_lines}\g<2>", prefix
    )
    # Replace the total number of words badge
    prefix = re.sub(
        r"(Taille-)\d+(_mots-brightgreen)", rf"\g<1>{total_words}\g<2>", prefix
    )

    # Rebuild the readme text
    readme_text = prefix + suffix

    # Update section badges
    for title, folder in parts_titles_to_folder.items():
        # Get the statistices for the current folder
        n_files: int = fields_to_replace_value[f"{folder}_number_of_files"]
        # Get the lines
        n_lines: int = fields_to_replace_value[f"{folder}_number_of_lines"]
        # Get the words
        n_words: int = fields_to_replace_value[f"{folder}_number_of_words"]

        # Regex to find the section and its badges
        section_pattern: str = rf"({re.escape(title)}.*?\n)(.*?)(\n---|(?=\n## )|\Z)"

        # Update the readme text with the new section content
        readme_text: str = re.sub(
            section_pattern,
            lambda m: replace_section(m, n_files, n_lines, n_words),
            readme_text,
            flags=re.DOTALL,
        )

    # Write the updated README
    with open("README.md", "w", encoding="utf-8") as f:
        # Write the text
        f.write(readme_text)


if __name__ == "__main__":
    # Call the main function
    main()
