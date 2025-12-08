from urllib.parse import quote
import json
import requests
from repositories.reference_repository import get_reference_by_key
from entities.reference import ReferenceType

class UserInputError(Exception):
    pass

def validate_reference(type_: str, key: str, content, old_key: str = None):
    """
    Parameters
    ----------
    type_ : str
        The reference type name (e.g. "book", "article").
    key : str
        The citation key for the reference.
    content : dict or str
        Either a mapping of field names to values, or a JSON string representing such a mapping.

    Raises
    ------
    UserInputError
        - A reference with the same citation key already exists.
        - `key` is empty or consists only of whitespace.
        - `content` is an invalid JSON string or is not a dict after parsing.
        - `type_` is not a known ReferenceType.
        - Any required field for the resolved ReferenceType is missing or empty in `content`.
    """
    if not key or not str(key).strip():
        raise UserInputError("Reference citation key can not be empty")

    # parse content
    if isinstance(content, str):
        try:
            content = json.loads(content) if content.strip() else {}
        except (json.JSONDecodeError, ValueError) as ex:
            raise UserInputError("Invalid content format - expected JSON or dict") from ex
    if not isinstance(content, dict):
        raise UserInputError("Invalid content format - expected JSON or dict")

    # validate reference type
    if not type_:
        raise UserInputError("Missing reference type")
    try:
        ref_type = ReferenceType(type_)
    except ValueError as ex:
        raise UserInputError("Unknown reference type") from ex

    # check required fields
    for req in ref_type.field_requirements():
        if isinstance(req, (list, tuple)):
            # at least one of the alternatives must be present and non-empty
            if not any(alt in content and str(content[alt]).strip() for alt in req):
                raise UserInputError(f"One of the required fields '{', '.join(req)}' must be filled")
        else:
            if req not in content or not str(content[req]).strip():
                raise UserInputError(f"Required field '{req}' must be filled")

    # check unique key
    if old_key is None or key != old_key:
        if get_reference_by_key(key):
            raise UserInputError(f"Reference citation key '{key}' already exists")


def fetch_doi_bibtex(doi: str, *, timeout: int = 10) -> str | None:
    """
    Fetch a BibTeX string for the given DOI using content negotiation via doi.org.
    Returns the BibTeX string on success, or None on failure.
    """
    if not doi or not str(doi).strip():
        return None

    url = f"https://doi.org/{quote(str(doi).strip())}"
    headers = {
        "Accept": "application/x-bibtex",
        "User-Agent": "BibTex-Miniprojekti/1.0 (mailto:you@example.com)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200 and resp.text:
            return resp.text
        return None
    except requests.RequestException:
        return None
