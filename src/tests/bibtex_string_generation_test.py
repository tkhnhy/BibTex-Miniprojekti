import unittest
from entities.reference import Reference, ReferenceType

class TestBibtexStringGeneration(unittest.TestCase):
    def test_basic_bibtex_generation(self):
        content = {"author": "Alice", "title": "Example Title", "year": "2025"}
        ref = Reference(1, "EX01", ReferenceType.BOOK, content)
        expected = (
            "@book{EX01,\n"
            "   author = {Alice},\n"
            "   title = {Example Title},\n"
            "   year = {2025},\n"
            "}\n"
        )
        self.assertEqual(str(ref), expected)

    def test_comment_included(self):
        content = {"author": "Bob", "title": "T"}
        ref = Reference(2, "EX02", ReferenceType.BOOK, content, comment="Bottom level comment")
        expected = (
            "@book{EX02,\n"
            "   author = {Bob},\n"
            "   title = {T},\n"
            "}\n"
            "% Bottom level comment\n"
        )
        self.assertEqual(str(ref), expected)

    def test_empty_content_without_comment(self):
        content = {}
        ref = Reference(3, "EMPTY01", ReferenceType.BOOK, content)
        expected = "@book{EMPTY01,\n}\n"
        self.assertEqual(str(ref), expected)

    def test_field_order_is_preserved(self):
        content = {"first": "1", "second": "2", "third": "3"}
        ref = Reference(4, "ORDER01", ReferenceType.ARTICLE, content)
        expected = (
            "@article{ORDER01,\n"
            "   first = {1},\n"
            "   second = {2},\n"
            "   third = {3},\n"
            "}\n"
        )
        self.assertEqual(str(ref), expected)
