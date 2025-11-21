from enum import Enum

class ReferenceType(Enum):
    ARTICLE = "article"
    BOOK = "book"
    BOOKLET = "booklet"
    CONFERENCE = "conference"
    INBOOK = "inbook"
    INCOLLECTION = "incollection"
    INPROCEEDINGS = "inproceedings"
    MANUAL = "manual"
    MASTERSTHESIS = "mastersthesis"
    MISC = "misc"
    PHDTHESIS = "phdthesis"
    PROCEEDINGS = "proceedings"
    TECHREPORT = "techreport"
    UNPUBLISHED = "unpublished"

    def required_fields(self) -> list[str]:
        """
        Return a list of required fields for this ReferenceType.
        """
        required_fields_map = {
            ReferenceType.ARTICLE: ["author", "title", "journal", "year"],
            ReferenceType.BOOK: ["author", "title", "publisher", "year"],
            ReferenceType.BOOKLET: ["title"],
            ReferenceType.CONFERENCE: ["author", "title", "booktitle", "year"],
            ReferenceType.INBOOK: ["author", "title", "chapter", "publisher", "year"],
            ReferenceType.INCOLLECTION: ["author", "title", "booktitle", "publisher", "year"],
            ReferenceType.INPROCEEDINGS: ["author", "title", "booktitle", "year"],
            ReferenceType.MANUAL: ["title"],
            ReferenceType.MASTERSTHESIS: ["author", "title", "school", "year"],
            ReferenceType.MISC: [],
            ReferenceType.PHDTHESIS: ["author", "title", "school", "year"],
            ReferenceType.PROCEEDINGS: ["title", "year"],
            ReferenceType.TECHREPORT: ["author", "title", "institution", "year"],
            ReferenceType.UNPUBLISHED: ["author", "title", "note"],
        }
        return required_fields_map.get(self, [])

    def display_str(self) -> str:
        """
        Return a human-readable display string for a ReferenceType.
        """
        display_strings = {
            ReferenceType.ARTICLE: "Article",
            ReferenceType.BOOK: "Book",
            ReferenceType.BOOKLET: "Booklet",
            ReferenceType.CONFERENCE: "Conference",
            ReferenceType.INBOOK: "In Book",
            ReferenceType.INCOLLECTION: "In Collection",
            ReferenceType.INPROCEEDINGS: "In Proceedings",
            ReferenceType.MANUAL: "Manual",
            ReferenceType.MASTERSTHESIS: "Master's Thesis",
            ReferenceType.MISC: "Misc",
            ReferenceType.PHDTHESIS: "PhD Thesis",
            ReferenceType.PROCEEDINGS: "Proceedings",
            ReferenceType.TECHREPORT: "Tech Report",
            ReferenceType.UNPUBLISHED: "Unpublished",
        }
        return display_strings.get(self, self.value.capitalize())

class Reference:
    def __init__(self, id_: int, key: str, type_: ReferenceType, content: dict):
        """
        Initialize a new Reference object.

        Parameters
        ----------
        id : int
            Database primary key.
        cite_key : str
            Unique BibTeX-style citation key.
        type : ReferenceType
            Type of the reference (e.g., ARTICLE, BOOK).
        content : dict
            Metadata fields for the reference, parsed from JSON/BibTeX input.
        """
        print(type(type_))
        self.id = id_
        self.key = key
        self.type = type_
        self.content = content

    def __str__(self):
        return f"{self.key}"
