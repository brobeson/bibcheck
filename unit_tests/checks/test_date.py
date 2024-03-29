"""Unit test for the author initials check."""

import unittest
import bibcheck.checker
import bibcheck.checks.date


class IssueTest(unittest.TestCase):
    """Test cases for the Issue class."""

    def test_class(self):
        """Test the Issue class."""
        issue = bibcheck.checks.doi.Issue("bibliography.bib", 34)
        self.assertEqual(issue.file_path, "bibliography.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertEqual(issue.message, "DOI entries should just contain the DOI.")


class CheckTest(unittest.TestCase):
    """Test cases for the check() function."""

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.checker = bibcheck.checks.doi.DoiChecker()

    def test_ok_lines(self):
        """Test BibTeX lines that should not fail the check."""
        lines = [
            bibcheck.checker.Line("  title={Hamlet},", "references.bib", 10),
            bibcheck.checker.Line("  doi={10.1109/5.771073},", "references.bib", 11),
        ]
        for line in lines:
            with self.subTest():
                self.assertFalse(self.checker.check(line))

    def test_bad_lines(self):
        """Test BibTeX lines that should fail the check."""
        lines = [
            bibcheck.checker.Line(
                "doi={https://doi.org/10.1109/5.771073},", "references.bib", 11
            ),
            bibcheck.checker.Line(
                "doi = {https://doi.org/10.1109/5.771073},", "references.bib", 11
            ),
            bibcheck.checker.Line(
                'doi = "https://doi.org/10.1109/5.771073",', "references.bib", 11
            ),
        ]
        for line in lines:
            with self.subTest():
                issue = self.checker.check(line)
                self.assertIsNotNone(issue)
                self.assertEqual(issue.file_path, "references.bib")
                self.assertEqual(issue.line_number, 11)
                self.assertEqual(
                    issue.message, "DOI entries should just contain the DOI."
                )
