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


def explore_recursively(from_folder: str = "./") -> dict[str, Any]:
    """
    Function to explore recursively

    folders are dicts
    files are tuple[int (number of lines), int (number of words)]
    """


def main() -> None:
    """
    Main function
    """

    # Prepare the fields_to_replace automatic content from parts_titles_to_folder
    for parts_folder in parts_titles_to_folder.values():
        # Number of lines
        fields_to_replace[f"{parts_folder}_number_of_lines"] = None

        # Number of words
        fields_to_replace[f"{parts_folder}_number_of_words"] = None

    # Get the README file content
    with open("README.md", "r", encoding="utf-8") as f:
        readme_text = f.read()

    # Find all the fields to replace

    field_


if __name__ == "__main__":
    main()
