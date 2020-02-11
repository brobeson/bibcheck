"""Unit test for the author initials check."""

import unittest
import bibcheck.checker
import bibcheck.checks.author


class IssuesTest(unittest.TestCase):
    """Test cases for the author issue classes."""

    def test_intials_issue(self):
        """Test the InitialsIssue class."""
        issue = bibcheck.checks.author.InitialsIssue("bibliography.bib", 34)
        self.assertEqual(issue.file_path, "bibliography.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertEqual(issue.message, "Author initials must be separated by a space.")

    def test_hyphenated_issue(self):
        """Test the HyphenatedIssue class."""
        issue = bibcheck.checks.author.HyphenatedIssue("bibliography.bib", 34)
        self.assertEqual(issue.file_path, "bibliography.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertEqual(
            issue.message,
            "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}",
        )


class CheckTest(unittest.TestCase):
    """Test cases for the check() function."""

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.checker = bibcheck.checks.author.AuthorChecker()

    def test_initials_ok(self):
        """Test author lines that do not have issues with initial spaces."""
        lines = [
            bibcheck.checker.Line("title={Hamlet},", "references.bib", 10),
            bibcheck.checker.Line(
                "author={Shakespeare, William},", "references.bib", 11
            ),
            bibcheck.checker.Line("author={Shakespeare, W. A.},", "references.bib", 11),
            bibcheck.checker.Line(
                "author={Shakespeare, William and Bacon, Francis},",
                "references.bib",
                11,
            ),
            bibcheck.checker.Line(
                "title={Hamlet}, author={Shakespeare, William},", "references.bib", 10
            ),
        ]
        for line in lines:
            with self.subTest():
                self.assertFalse(self.checker.check(line))

    def test_initials_bad(self):
        """Test author lines that have issues with initial spaces."""
        lines = [
            bibcheck.checker.Line("author={Shakespeare, W.A.},", "references.bib", 11),
            bibcheck.checker.Line(
                "author={Shakespeare, W.A. and Bacon, Francis},", "references.bib", 11
            ),
            bibcheck.checker.Line(
                "author={Shakespeare, W. A. and Bacon, F.A.},", "references.bib", 11
            ),
            bibcheck.checker.Line(
                "title={Hamlet}, author={Shakespeare, W.A.},", "references.bib", 11
            ),
            bibcheck.checker.Line(
                "title={Hamlet}, author={Shakespeare, WA.},", "references.bib", 11
            ),
            bibcheck.checker.Line(
                "title={Hamlet}, author={Shakespeare, W.A},", "references.bib", 11
            ),
            bibcheck.checker.Line(
                "title={Hamlet}, author={Shakespeare, WA},", "references.bib", 11
            ),
        ]
        for line in lines:
            with self.subTest():
                issues = self.checker.check(line)
                self.assertEqual(len(issues), 1)
                self.assertIsNotNone(issues[0])
                self.assertEqual(issues[0].file_path, "references.bib")
                self.assertEqual(issues[0].line_number, 11)
                self.assertEqual(
                    issues[0].message, "Author initials must be separated by a space."
                )

    def test_hyphens_ok(self):
        """Test author lines that do not have issues with hyphenated names."""
        lines = [
            bibcheck.checker.Line(
                "author={Shakespeare, William}", "references.bib", 11
            ),
            bibcheck.checker.Line(
                "author={Shakespeare, Wil-{liam}", "references.bib", 11
            ),
            bibcheck.checker.Line(
                "author={Shakespeare, Wil-Liam", "references.bib", 11
            ),
        ]
        for line in lines:
            with self.subTest():
                self.assertFalse(self.checker.check(line))

    def test_hyphens_bad(self):
        """Test author lines that have issues with hyphenated names."""
        issues = self.checker.check(
            bibcheck.checker.Line(
                "author={Shakespeare, Wil-liam}", "references.bib", 11
            )
        )
        self.assertEqual(len(issues), 1)
        self.assertIsNotNone(issues[0])
        self.assertEqual(issues[0].file_path, "references.bib")
        self.assertEqual(issues[0].line_number, 11)
        self.assertEqual(
            issues[0].message,
            "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}",
        )
