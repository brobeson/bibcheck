"""Unit test for the author initials check."""

import unittest
import bibcheck.issue
import bibcheck.checks.author_initials as author_initials


class IssueTest(unittest.TestCase):
    """Test cases for the Issue class."""

    def test_class(self):
        """Test the Issue class."""
        issue = author_initials.Issue("bibliography.bib", 34)
        self.assertEqual(issue.file_path, "bibliography.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertEqual(issue.message, "Author initials must be separated by a space.")


class CheckTest(unittest.TestCase):
    """Test cases for the check() function."""

    def test_ok_lines(self):
        """Test BibTeX lines that should not fail the check."""
        cases = [
            # (test line, test context)
            ("  title={Hamlet},", bibcheck.issue.Context("references.bib", 10)),
            (
                "  author={Shakespeare, William},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  author={Shakespeare, W. A.},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  author={Shakespeare, William and Bacon, Francis},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  title={Hamlet}, author={Shakespeare, William},",
                bibcheck.issue.Context("references.bib", 10),
            ),
        ]
        for case in cases:
            with self.subTest():
                self.assertIsNone(author_initials.check(case[0], case[1]))

    def test_bad_lines(self):
        """Test BibTeX lines that should fail the check."""
        cases = [
            # (test line, test context)
            (
                "  author={Shakespeare, W.A.},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  author={Shakespeare, W.A. and Bacon, Francis},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  author={Shakespeare, W. A. and Bacon, F.A.},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  title={Hamlet}, author={Shakespeare, W.A.},",
                bibcheck.issue.Context("references.bib", 11),
            ),
        ]
        for case in cases:
            with self.subTest():
                issue = author_initials.check(case[0], case[1])
                self.assertIsNotNone(issue)
                self.assertEqual(issue.file_path, "references.bib")
                self.assertEqual(issue.line_number, 11)
                self.assertEqual(
                    issue.message, "Author initials must be separated by a space."
                )
