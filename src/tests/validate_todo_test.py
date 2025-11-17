import unittest
from util import validate_reference, UserInputError
from app import app

class TestTodoValidation(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_valid_length_does_not_raise_error(self):
        validate_reference("book", "juokse", {"author": "aa", "title": "aa", "publisher": "aa", "year": "2025"})

    #def test_too_short_or_long_raises_error(self):
        #with self.assertRaises(UserInputError):
            #validate_reference("ole")

        #with self.assertRaises(UserInputError):
            #validate_reference("koodaa" * 20)
