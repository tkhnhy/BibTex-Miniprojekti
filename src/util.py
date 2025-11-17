from repositories.reference_repository import get_references

class UserInputError(Exception):
    pass

def validate_reference(reference_type, reference_key, reference_data):

    if not reference_key.strip():
        raise UserInputError(f"Reference key can not be empty")

    required_fields = {
        "book": ["author", "book_title", "publisher", "year"],
    }

    if reference_type not in required_fields:
        raise UserInputError(f"Unknown reference type")

    for field in required_fields[reference_type]:
        if field not in reference_data or not reference_data[field].strip():
            raise UserInputError(f"All required fields must be filled")

    reference_keys = [ref.reference_key for ref in get_references()]
    if reference_key in reference_keys:
        raise UserInputError(f"Reference key '{reference_key}' already exists")

