from clipping import Book, Clipping

import re
from pathlib import Path
from typing import Generator
import unicodedata
from collections import defaultdict

# TODO: Add configuration files for readers different than Kindle Paperwhite 4
# TODO: Simplify below regexes as now they unnecessarily complicated
# TODO: Add more specific exceptions
# TODO: Use `re.VERBOSE` to increase readability of these regexes
PATTERN_A: re.Pattern = re.compile(
    r"(?P<title>.*) \((?P<author>.*)\)\n- Your (?P<type>\w+) at location ((?P<location_start>\d+)-(?P<location_end>\d+)|(?P<location>\d+)) \| Added on (?P<timestamp>.*)\n\n(?P<content>.*)"
)

PATTERN_B: re.Pattern = re.compile(
    r"(?P<title>.*) \((?P<author>.*)\)\n- Your (?P<type>\w+) on page (?P<page>\d+) \| location ((?P<location_start>\d+)-(?P<location_end>\d+)|(?P<location>\d+)) \| Added on (?P<timestamp>.*)\n\n(?P<content>.*)"
)


PATTERN_C: re.Pattern = re.compile(
    r"(?P<title>.*)\n- Your (?P<type>\w+) on page (?P<page>(\d+)) \| Added on (?P<timestamp>.*)\n\n(?P<content>.*)"
)

PATTERN_D: re.Pattern = re.compile(
    r"(?P<title>.*)\n- Your (?P<type>\w+) on page (?P<page>\d+)-\d+ \| Added on (?P<timestamp>.*)\n\n(?P<content>.*)"
)


def parse_clipping(clipping: str) -> Clipping:
    """Given clipping in a str format, return it as Clipping format.

    Clipping format may contain both Highlight and Note.
    Book object is created, too, to make it possible later
    to filter all clippings by book author/title.

    Parameters
    ----------
    clipping : str
        multiline text string with clipping from Kindle

    Returns
    -------
    Clipping
        Clipping object containing data from text string

    Raises
    ------
    ValueError
        when unknown format of clipping is used in provided clipping
    """
    for pattern in [PATTERN_A, PATTERN_B, PATTERN_C, PATTERN_D]:
        if match := pattern.search(clipping):
            break
    else:
        raise ValueError(f"Pattern for clipping:\n\n{clipping}\n\nis not defined!")

    try:
        author = match.group("author")
    except IndexError:
        author = ""

    title = match.group("title").strip()

    book = Book(author=author, title=title)

    location: tuple[int, int] | tuple[None, None]
    if "location" in match.groupdict() and match.group("location") is not None:
        location = (int(match.group("location")), int(match.group("location")))
    elif "location" not in match.groupdict():
        location = (None, None)
    else:
        location = (
            int(match.group("location_start")),
            int(match.group("location_end")),
        )

    page = int(match.group("page")) if "page" in match.groupdict() else None
    return Clipping(
        book=book,
        timestamp=match.group("timestamp"),
        clipping_type=match.group("type"),
        content=match.group("content"),
        location=location,
        page=page,
    )


def parse_my_clippings(file_location: Path) -> Generator[Clipping, None, None]:
    """Read file with clippings and yield split clippings as Clippings.

    Parameters
    ----------
    file_location : Path
        path to Kindle file with clippings

    Yields
    ------
    Generator[Clipping, None, None]
        generator yielding parsed Clippings
    """
    CLIPPING_SEPARATOR = "=========="

    with open(file_location, encoding="utf-8-sig") as file:
        # Read file and normalize its content - different books may have different encodings
        file_content = (
            unicodedata.normalize("NFKD", file.read()).strip().replace("\ufeff", "")
        )
        raw_clippings = file_content.split(CLIPPING_SEPARATOR)

    for clipping in raw_clippings:
        if clipping:
            yield parse_clipping(clipping)


def sort_clippings(clippings: list[Clipping]) -> dict[Book, list[Clipping]]:
    """Given list of clippings, return a mapping clippings to books.

    For example, the list with single clipping:
    [
        Clipping(
            book=Book(author="Anne Frank", title="Dziennik"),
            clipping_type="Note",
            timestamp="Wednesday, 3 February 2021 23:00:55",
            content="Ciekawe jakie to standardy wymusily te karteczki na zywnosc",
            location=(1194, 1194),
            page=78,
        ),
    ]

    will be sorted into:

    {
        Book(author="Anne Frank", title="Dziennik"): [
            Clipping(
                book=Book(author="Anne Frank", title="Dziennik"),
                clipping_type="Note",
                timestamp="Wednesday, 3 February 2021 23:00:55",
                content="Ciekawe jakie to standardy wymusily te karteczki na zywnosc",
                location=(1194, 1194),
                page=78,
            ),
        ]
    }

    Parameters
    ----------
    clippings : list[Clipping]
        list of clippings

    Returns
    -------
    dict[Book, list[Clipping]]
        mapping of books to clippings
    """
    result = defaultdict(list)
    for clipping in clippings:
        if clipping.clipping_type == "Bookmark":
            continue
        result[clipping.book].append(clipping)
    return result


def dump_book_to_markdown(
    mapping: dict[Book, list[Clipping]], target_location: Path
) -> None:
    """Create file for each book and dump all notes and highlights to this file.

    Parameters
    ----------
    mapping : dict[Book, list[Clipping]]
        mapping books and clippings
    target_location : Path
        target directory in which new files should be created

    Raises
    ------
    FileNotFoundError
        when target directory does not exist
    """
    if target_location.is_dir() is False:
        # TODO: Improve handling this exception
        raise FileNotFoundError(f"{target_location} is not a directory!")

    for book, clippings in mapping.items():
        filename = target_location / f"{str(book)}.md"
        with open(filename, "w") as file:
            # TODO: Templating would be nice here.
            file.write(f"# {str(book)}\n\n")
            # TODO: Sort clippings by their timestamps.
            # TODO: Split functionality for headers and content
            # TODO: As templates are added,
            file.write(f"First note: {clippings[0].timestamp}\n")
            file.write(f"Last note: {clippings[-1].timestamp}\n\n")
            file.write("## Notes & Highlights from Kindle\n\n")

            for clipping in clippings:
                file.write(str(clipping))
