import unittest
from entities.reference import ReferenceType

class TestReferenceType(unittest.TestCase):
    def test_display_str(self):
        string = ReferenceType.ARTICLE.display_str()
        self.assertEqual(string, "Article")
