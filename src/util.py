from repositories.reference_repository import get_reference_by_key

class UserInputError(Exception):
    pass

def validate_reference(type_: str, key: str, content: str):
    if not key.strip():
        raise UserInputError("Reference citation key can not be empty")

    required_fields = {
        "book": ["author", "title", "publisher", "year"],
    }

    if type_ not in required_fields:
        raise UserInputError("Unknown reference type")

    for field in required_fields[type_]:
        if field not in content or not content[field].strip():
            raise UserInputError("All required fields must be filled")

    if get_reference_by_key(key):
        raise UserInputError(f"Reference citation key '{key}' already exists")
