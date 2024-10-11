"""Module with CLI interface basic functions."""

import sys
import kindle_parser
from pathlib import Path

DESCRIPTION = """kindleparse tool that parses clippings from Kindle's `My Clipping.txt` into manageable markdown files.

Usage: 
    kindleparse <input_file> <output_dir>

Example: 
    kindleparse "My Clippings.txt" some_directory
"""


def main(argv):
    # Verification of list of args
    if len(argv) != 2:
        raise SystemExit(DESCRIPTION)

    # Parse paths
    input_file = Path(argv[0])
    output_dir = Path(argv[1])
    if not output_dir.exists():
        output_dir.mkdir()

    # Trigger logic
    clippings = kindle_parser.parse_my_clippings(input_file)
    mapping = kindle_parser.sort_clippings(clippings)
    kindle_parser.dump_book_to_markdown(mapping, output_dir)


if __name__ == "__main__":
    # Strip script path from argv and pass it to main
    main(sys.argv[1:])
