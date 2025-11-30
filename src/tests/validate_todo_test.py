import unittest
from app import app
from db_helper import setup_db, reset_db
from util import validate_reference, UserInputError

class TestReferenceValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_context = app.app_context()
        cls.app_context.push()
        setup_db()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        reset_db()

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

    def test_invalid_json_string(self):
        with self.assertRaises(UserInputError):
            validate_reference("book", "abc", "{not: valid json}")

    def test_content_not_dict(self):
        with self.assertRaises(UserInputError):
            validate_reference("book", "abc", 123)  # ei dict eikä JSON

    def test_missing_reference_type(self):
        with self.assertRaises(UserInputError):
            validate_reference("", "abc", {"author": "A", "title": "T", "publisher": "P", "year": "2000"})
