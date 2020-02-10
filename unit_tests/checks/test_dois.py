"""Unit test for the author initials check."""

import unittest
import bibcheck.issue
import bibcheck.checks.dois as dois


class IssueTest(unittest.TestCase):
    """Test cases for the Issue class."""

    def test_class(self):
        """Test the Issue class."""
        issue = dois.Issue("bibliography.bib", 34)
        self.assertEqual(issue.file_path, "bibliography.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertEqual(issue.message, "DOI entries should just contain the DOI.")


class CheckTest(unittest.TestCase):
    """Test cases for the check() function."""

    def test_ok_lines(self):
        """Test BibTeX lines that should not fail the check."""
        cases = [
            # (test line, test context)
            ("  title={Hamlet},", bibcheck.issue.Context("references.bib", 10)),
            ("  doi={10.1109/5.771073},", bibcheck.issue.Context("references.bib", 11)),
        ]
        for case in cases:
            with self.subTest():
                self.assertIsNone(dois.check(case[0], case[1]))

    def test_bad_lines(self):
        """Test BibTeX lines that should fail the check."""
        cases = [
            # (test line, test context)
            (
                "  doi={https://doi.org/10.1109/5.771073},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  doi = {https://doi.org/10.1109/5.771073},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                '  doi = "https://doi.org/10.1109/5.771073",',
                bibcheck.issue.Context("references.bib", 11),
            ),
        ]
        for case in cases:
            with self.subTest():
                issue = dois.check(case[0], case[1])
                self.assertIsNotNone(issue)
                self.assertEqual(issue.file_path, "references.bib")
                self.assertEqual(issue.line_number, 11)
                self.assertEqual(
                    issue.message, "DOI entries should just contain the DOI."
                )
