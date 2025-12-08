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

    def __init__(self, id_: int, key: str, type_: ReferenceType | str,
                 content: dict[str, str], *, tags: list[Tag] = None, comment: str = ''):
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
        #This makes the reference show as a bibtex style entry when calling it as a str
        bibtex_string = ""
        bibtex_string += f"@{str(self.type.value)}{{{self.key},\n"
        for key, value in self.content.items():
            bibtex_string += f"   {key} = {{{value}}},\n"
        bibtex_string += "}\n"
        if self.comment:
            bibtex_string += f"% {self.comment}\n"

        return bibtex_string

    @classmethod
    def from_bibtex(cls, id_: int, bibtex_str: str): # pylint: disable=too-many-locals, too-many-nested-blocks, too-many-branches, too-many-statements
        """Create a Reference instance from a BibTeX formatted string.

        This parser is tolerant to entries formatted on a single line or with
        irregular spacing. It handles brace-nested values and quoted values.
        If a %-comment exists after the main entry it is parsed as the comment.
        """
        s = bibtex_str.strip()
        if not s:
            raise ValueError("empty bibtex string")

        # Find start: @type{
        at_pos = s.find('@')
        if at_pos == -1:
            raise ValueError("invalid bibtex: missing '@'")

        brace_open = s.find('{', at_pos)
        if brace_open == -1:
            raise ValueError("invalid bibtex: missing '{' after type")

        # type string
        type_str = s[at_pos + 1:brace_open].strip().lower()

        # Find closing brace for the entry
        depth = 0
        brace_close = None
        for i in range(brace_open, len(s)):
            ch = s[i]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    brace_close = i
                    break
        if brace_close is None:
            raise ValueError("invalid bibtex: no closing '}' found")

        # Extract key: text between opening brace comma
        key = None
        for i in range(brace_open + 1, brace_close):
            if s[i] == '{' or s[i] == '}':
                raise ValueError("invalid bibtex: unexpected brace in key")
            if s[i] == ',':
                key = s[brace_open + 1:i].strip()
                body_start = i + 1
                break
        if key is None:
            key = s[brace_open+1:brace_close].strip()
            body_start = brace_close
        if key == '':
            raise ValueError("invalid bibtex: empty key")

        # Extract trailing comment: any text after closing brace
        comment = ''
        trailing = s[brace_close + 1 :].strip()
        if trailing:
            pct = trailing.find('%')
            if pct != -1:
                comment = trailing[pct + 1 :].strip()

        # Extract entry body
        body = s[body_start:brace_close].strip()

        # Parse fields robustly
        content = {}
        i = 0
        while i < len(body): # pylint: disable=too-many-nested-blocks
            # skip whitespace and commas
            while i < len(body) and (body[i].isspace() or body[i] == ','):
                i += 1
            if i >= len(body):
                break

            # read field name
            start = i
            while i < len(body) and (body[i].isalnum() or body[i] in ['_', '-']):
                i += 1
            field = body[start:i].strip().lower()
            # skip whitespace
            while i < len(body) and body[i].isspace():
                i += 1
            # expect '='
            if i < len(body) and body[i] == '=':
                i += 1
            else:
                raise ValueError(f"invalid bibtex: expected '=' after field '{field}'")
            # skip whitespace after =
            while i < len(body) and body[i].isspace():
                i += 1
            # parse value, handle nesting
            if i < len(body) and body[i] == '{':
                i += 1
                val_start = i
                depth = 1
                while i < len(body) and depth > 0:
                    if body[i] == '{':
                        depth += 1
                    elif body[i] == '}':
                        depth -= 1
                    i += 1
                val = body[val_start:i - 1].strip()
            elif i < len(body) and body[i] == '"':
                # quoted string
                i += 1
                val_start = i
                while i < len(body):
                    if body[i] == '"' and body[i - 1] != '\\':
                        break
                    i += 1
                val = body[val_start:i].strip()
                i += 1 # skip closing quote
            else:
                # bare token
                val_start = i
                while i < len(body) and body[i] != ',':
                    i += 1
                val = body[val_start:i].strip()

            if val is not None:
                # replace multiple whitespace with a single space
                normalized = ' '.join(val.split())
                content[field] = normalized

        # Construct ReferenceType
        try:
            ref_type = ReferenceType(type_str)
        except Exception as ex:
            raise ValueError(f"invalid bibtex: unknown type '{type_str}'") from ex

        return cls(id_=id_, key=key, type_=ref_type, content=content, comment=comment)
