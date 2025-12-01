import unittest
from entities.reference import Reference

class TestReferenceFromString(unittest.TestCase):
    bib_string = """% comment
                    @article{r1,
                        year = {2022},
                        title = {Artificial intelligence (AI) applications for marketing: A literature-based study},
                        author = {Abid Haleem, Mohd Javaid,  Mohd Asim Qadri, Ravi Pratap Singh, Rajiv Suman},
                        journal = {International Journal of Intelligent Netwroks},
                    }"""
    def test_from_bibtex(self):
        ref = Reference.from_bibtex(1, self.bib_string)
        self.assertIsNotNone(ref)
        self.assertEqual(ref.key, "r1")
        self.assertEqual(ref.type.value, "article")
        self.assertEqual(ref.content["author"], "Abid Haleem, Mohd Javaid,  Mohd Asim Qadri, Ravi Pratap Singh, Rajiv Suman")
        self.assertEqual(ref.content["title"], "Artificial intelligence (AI) applications for marketing: A literature-based study")
        self.assertEqual(ref.content["year"], "2022")
        self.assertEqual(ref.comment, "comment")
