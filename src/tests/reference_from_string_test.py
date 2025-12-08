import unittest
from entities.reference import Reference

class TestReferenceFromBibTeXParsing(unittest.TestCase):

    def test_single_line_entry_with_trailing_comment(self):
        bib = (
            "@article{r1, year = {2022}, title = {Artificial intelligence (AI) applications for marketing: "
            "A literature-based study}, author = {Abid Haleem, Mohd Javaid,  Mohd Asim Qadri, "
            "Ravi Pratap Singh, Rajiv Suman}, journal = {International Journal of Intelligent Networks} } % comment"
        )
        ref = Reference.from_bibtex(1, bib)
        self.assertIsNotNone(ref)
        self.assertEqual(ref.key, "r1")
        self.assertEqual(ref.type.value, "article")
        self.assertEqual(ref.content["year"], "2022")
        self.assertIn("Artificial intelligence", ref.content["title"])
        self.assertEqual(ref.comment, "comment")
        self.assertIn("Abid Haleem", ref.content["author"])

    def test_multi_line_entry(self):
        bib = (
            "@book{b1,\n"
            "   author = {John Doe},\n"
            "   title = {The Book Title},\n"
            "   publisher = {Fictional Publishing},\n"
            "   year = {2015}\n"
            "} % This is a comment"
        )
        ref = Reference.from_bibtex(2, bib)
        self.assertEqual(ref.key, "b1")
        self.assertEqual(ref.type.value, "book")
        self.assertEqual(ref.content["author"], "John Doe")
        self.assertEqual(ref.content["title"], "The Book Title")
        self.assertEqual(ref.content["publisher"], "Fictional Publishing")
        self.assertEqual(ref.content["year"], "2015")
        self.assertEqual(ref.comment, "This is a comment")

    def test_additional_whitespace_and_newlines(self):
        bib = (
            "@misc{   misc1  \n ,\n"
            "   title    =    {  A       Miscellaneous  Entry  }  ,\n"
            "   author= { Alice \n    Smith } ,\n"
            "   year= {  2021  } \n"
            "}   %  Another comment   "
        )
        ref = Reference.from_bibtex(3, bib)
        self.assertEqual(ref.key, "misc1")
        self.assertEqual(ref.type.value, "misc")
        self.assertEqual(ref.content["title"], "A Miscellaneous Entry")
        self.assertEqual(ref.content["author"], "Alice Smith")
        self.assertEqual(ref.content["year"], "2021")
        self.assertEqual(ref.comment, "Another comment")

    def test_trailing_text_after_closing_brace(self):
        bib = (
            "@techreport{tr1, title={Tech Report Title}, author={Bob Brown}, year={2019}} Some trailing text"
        )
        ref = Reference.from_bibtex(4, bib)
        self.assertEqual(ref.key, "tr1")
        self.assertEqual(ref.type.value, "techreport")
        self.assertEqual(ref.content["title"], "Tech Report Title")
        self.assertEqual(ref.content["author"], "Bob Brown")
        self.assertEqual(ref.content["year"], "2019")

    def test_nested_braces_in_value(self):
        bib = (
            "@inbook{k2, title = {A Book with {Nested {Braces}} in the Title}, "
            "author = {Doe, John}, pages = {13-42}, publisher = {Pub House}, year = {2018} }"
        )
        ref = Reference.from_bibtex(2, bib)
        self.assertEqual(ref.key, "k2")
        self.assertEqual(ref.type.value, "inbook")
        # inner braces must be preserved
        self.assertEqual(ref.content["pages"], "13-42")
        self.assertEqual(ref.content["publisher"], "Pub House")
        self.assertEqual(ref.content["title"], "A Book with {Nested {Braces}} in the Title")

    def test_quoted_values(self):
        bib = '@misc{q1, title = "A Quoted Title", author = "Smith, Jane", year = "2020"}'
        ref = Reference.from_bibtex(3, bib)
        self.assertEqual(ref.key, "q1")
        self.assertEqual(ref.content["title"], "A Quoted Title")
        self.assertEqual(ref.content["author"], "Smith, Jane")
        self.assertEqual(ref.content["year"], "2020")

    def test_bare_token_value(self):
        bib = "@book{b2, month = jan, year = 2010, title = {Some Title} }"
        ref = Reference.from_bibtex(5, bib)
        self.assertEqual(ref.content["month"], "jan")
        self.assertEqual(ref.content["year"], "2010")

    def test_minimal_entry_parses(self):
        bib = "@misc{m1}"
        ref = Reference.from_bibtex(4, bib)
        self.assertEqual(ref.key, "m1")
        self.assertEqual(ref.type.value, "misc")

    def test_missing_field_value_parses(self):
        bib = "@misc{m2, title = {Title Only}, author = , year = 2021 }"
        ref = Reference.from_bibtex(4, bib)
        self.assertEqual(ref.key, "m2")
        self.assertEqual(ref.type.value, "misc")
        self.assertEqual(ref.content["title"], "Title Only")
        self.assertEqual(ref.content["author"], "")

    def test_empty_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            Reference.from_bibtex(0, "")

    def test_invalid_type_raises_value_error(self):
        bad = "@unknown{r1, title={X}}"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(6, bad)

    def test_missing_opening_brace_raises_value_error(self):
        bad = "@article r1, title=none}"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(7, bad)

    def test_misplaced_opening_brace_raises_value_error(self):
        bad = "{@article r1, title=none}"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(7, bad)

    def test_missing_closing_brace_raises_value_error(self):
        bad = "@article{r1, title={X}"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(7, bad)

    def test_missing_key_raises_value_error(self):
        bad = "@article{   , title={X}}"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(7, bad)

    def test_brace_in_key_raises_value_error(self):
        bad = "@article{bad{key}, title={X}}"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(7, bad)

    def test_missing_at_raises_value_error(self):
        bad = "article{noat, title={X}}"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(7, bad)

    def test_unclosed_brace_raises_value_error(self):
        bad = "@article{b1, title={Missing end"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(8, bad)

    def test_malformed_field_missing_equals_raises_value_error(self):
        # missing '=' after field name
        bib = "@article{f1, title = {T}, malformedfield  title2 = {X}, year = {2000} }"
        with self.assertRaises(ValueError):
            Reference.from_bibtex(9, bib)


if __name__ == "__main__":
    unittest.main()
