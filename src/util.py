import json
from repositories.reference_repository import get_reference_by_key
from entities.reference import ReferenceType

class UserInputError(Exception):
    pass

def validate_reference(type_: str, key: str, content):
    """
    Parameters
    ----------
    type : str
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
        except Exception as ex:
            raise UserInputError("Invalid content format - expected JSON or dict") from ex
    if not isinstance(content, dict):
        raise UserInputError("Invalid content format - expected JSON or dict")

    # validate reference type
    try:
        ref_type = ReferenceType(type_)
    except ValueError as ex:
        raise UserInputError("Unknown reference type") from ex

    # check required fields (if any)
    for field in ref_type.required_fields():
        if field not in content or not str(content[field]).strip():
            raise UserInputError(f"Required field '{field}' must be filled")

    # check unique key
    if get_reference_by_key(key):
        raise UserInputError(f"Reference citation key '{key}' already exists")
