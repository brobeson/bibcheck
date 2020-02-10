"""Unit test for the author initials check."""

import unittest
import bibcheck.issue
import bibcheck.checks.author as author


class IssuesTest(unittest.TestCase):
    """Test cases for the author issue classes."""

    def test_intials_issue(self):
        """Test the InitialsIssue class."""
        issue = author.InitialsIssue("bibliography.bib", 34)
        self.assertEqual(issue.file_path, "bibliography.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertEqual(issue.message, "Author initials must be separated by a space.")

    def test_hyphenated_issue(self):
        """Test the HyphenatedIssue class."""
        issue = author.HyphenatedIssue("bibliography.bib", 34)
        self.assertEqual(issue.file_path, "bibliography.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertEqual(
            issue.message,
            "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}",
        )


class CheckTest(unittest.TestCase):
    """Test cases for the check() function."""

    def test_initials_ok(self):
        """Test author lines that do not have issues with initial spaces."""
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
                self.assertFalse(author.check(case[0], case[1]))

    def test_initials_bad(self):
        """Test author lines that have issues with initial spaces."""
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
            (
                "  title={Hamlet}, author={Shakespeare, WA.},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  title={Hamlet}, author={Shakespeare, W.A},",
                bibcheck.issue.Context("references.bib", 11),
            ),
            (
                "  title={Hamlet}, author={Shakespeare, WA},",
                bibcheck.issue.Context("references.bib", 11),
            ),
        ]
        for case in cases:
            with self.subTest():
                issues = author.check(case[0], case[1])
                self.assertEqual(len(issues), 1)
                self.assertIsNotNone(issues[0])
                self.assertEqual(issues[0].file_path, "references.bib")
                self.assertEqual(issues[0].line_number, 11)
                self.assertEqual(
                    issues[0].message, "Author initials must be separated by a space."
                )

    def test_hyphens_ok(self):
        """Test author lines that do not have issues with hyphenated names."""
        cases = [
            ("author={Shakespeare, William}", bibcheck.issue.Context("references.bib", 11)),
            ("author={Shakespeare, Wil-{liam}", bibcheck.issue.Context("references.bib", 11)),
            ("author={Shakespeare, Wil-Liam", bibcheck.issue.Context("references.bib", 11)),
        ]
        for case in cases:
            with self.subTest():
                self.assertFalse(author.check(case[0], case[1]))

    def test_hyphens_bad(self):
        """Test author lines that have issues with hyphenated names."""
        issues = author.check(
            "author={Shakespeare, Wil-liam}",
            bibcheck.issue.Context("references.bib", 11)
        )
        self.assertEqual(len(issues), 1)
        self.assertIsNotNone(issues[0])
        self.assertEqual(issues[0].file_path, "references.bib")
        self.assertEqual(issues[0].line_number, 11)
        self.assertEqual(
            issues[0].message,
            "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}",
        )
