from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Book:
    author: str
    title: str

    def __str__(self) -> str:
        if not self.author:
            return self.title
        else:
            return f"{self.author} - {self.title}"


@dataclass(eq=True, frozen=True)
class Clipping:
    book: Book
    clipping_type: str
    timestamp: str
    content: str
    location: tuple[int, int] | tuple[None, None]
    page: int | None = None

    def __str__(self) -> str:
        """Return string representation of the clipping.

        Markdown convention for bullet lists and quotation blocks is used,
        for example:

            - some note
            > some highlight

        Returns
        -------
        str
            string representation of the clipping

        Raises
        ------
        ValueError
            when `self.clipping_type` has unknown value
        """
        if self.clipping_type == "Note":
            return f"- {self.content}\n\n"
        elif self.clipping_type == "Highlight":
            return f"> {self.content}\n\n"
        else:
            raise ValueError(f"Unknown type of clipping: {self.clipping_type}")
