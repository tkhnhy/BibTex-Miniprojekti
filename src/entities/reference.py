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
