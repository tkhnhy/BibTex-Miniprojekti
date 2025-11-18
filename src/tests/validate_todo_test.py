import unittest
from util import validate_reference, UserInputError
from app import app

class TestReferenceValidation(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_valid_book(self):
        validate_reference("book", "juokse", {"author": "aa", "title": "aa", "publisher": "aa", "year": "2025"})

    def test_invalid_type(self):
        with self.assertRaises(UserInputError):
            validate_reference(
                "books", # invalid
                "juokse",
                {"author": "aa", "title": "aa", "publisher": "aa", "year": "2025"}
            )

    def test_empty_key(self):
        with self.assertRaises(UserInputError):
            validate_reference(
                "book",
                "", # empty
                {"author": "aa", "title": "aa", "publisher": "aa", "year": "2025"}
            )

    def test_reference_missing_required_field(self):
        with self.assertRaises(UserInputError):
            validate_reference(
                "book",
                "juokse",
                {"author": "aa", "title": "aa", "publisher": "aa"}  # missing year
            )
