from enum import Enum
from entities.tag import Tag

COMMON_BIBTEX_FIELDS: list[str] = [
    "author", "editor", "title", "journal", "booktitle", "publisher",
    "year", "month", "volume", "number", "pages", "chapter", "school",
    "institution", "note", "series", "address", "edition", "howpublished",
    "organization", "url", "doi",
]

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

    def field_requirements(self) -> list[str | list[str]]:
        """
        Return field requirements for this ReferenceType. Each requirement is either a single field
        (string) or a list of alternative field names (at least one of which is required).
        """
        required_fields_map = {
            ReferenceType.ARTICLE: ["author", "title", "journal", "year"],
            ReferenceType.BOOK: [["author", "editor"], "title", "publisher", "year"],
            ReferenceType.BOOKLET: ["title"],
            ReferenceType.CONFERENCE: ["author", "title", "booktitle", "year"],
            ReferenceType.INBOOK: [["author", "editor"], "title", ["chapter", "pages"], "publisher", "year"],
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
    """
    Represents a bibliographic reference.

    Attributes
    ----------
    id : int
        Database primary key.
    key : str
        Unique BibTeX-style citation key.
    type : ReferenceType
        Reference type as a ReferenceType enum member (e.g. ARTICLE, BOOK).
    content : dict[str, str]
        Mapping from field name to content.
    tags : list[Tag]
        List of associated tags.
    comment : str
        Optional comment about the reference.
    """

    def __init__(self, id_: int, key: str, type_: ReferenceType | str, # pylint: disable=too-many-arguments,too-many-positional-arguments
                 content: dict[str, str], comment: str = ''):
        self.id = int(id_)
        self.key = str(key)
        self.content = content
        self.tags = tags if tags is not None else []
        self.comment = comment

        if isinstance(type_, ReferenceType):
            self.type = type_
        else:
            self.type = ReferenceType(type_)

    def __str__(self):
        #This makes the reference show as a bibtex style entry when calling it as a str. (as defined in the backlog)

        bibtex_string = ""
        bibtex_string += f"@{str(self.type.value)}{{{self.key},\n"
        for key, value in self.content.items():
            bibtex_string += f"   {key} = {{{value}}},\n"
        bibtex_string += "}\n"
        if self.comment:
            bibtex_string += f"% {self.comment}\n"

        return bibtex_string

    @classmethod
    def from_bibtex(cls, id_: int, bibtex_str: str):
        """Create a Reference instance from a BibTeX formatted string."""
        lines = bibtex_str.strip().splitlines()

        # Parse header: @type{key,
        header = lines[0].strip()
        at_pos = header.find('@')
        brace_pos = header.find('{')
        comma_pos = header.find(',', brace_pos)

        type_ = ReferenceType(header[at_pos + 1:brace_pos].strip())
        key = header[brace_pos + 1:comma_pos].strip()

        # Parse content fields
        content = {}
        for line in lines[1:-1]:
            line = line.strip().rstrip(',')
            if '=' in line:
                field, value = line.split('=', 1)
                content[field.strip()] = value.strip().strip('{}')

        # Extract comment if present
        comment = ''
        if lines[-1].strip().startswith('%'):
            comment = lines[-1].strip().removeprefix('%').strip()

        return cls(id_=id_, key=key, type_=type_, content=content, comment=comment)
