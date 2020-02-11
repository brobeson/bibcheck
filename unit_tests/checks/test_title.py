"""Unit test for the title initials check."""

import unittest
import bibcheck.checker
import bibcheck.checks.title


class IssuesTest(unittest.TestCase):
    """Test cases for the title issue classes."""

    def test_intials_issue(self):
        """Test the AllCapsIssue class."""
        issue = bibcheck.checks.title.AllCapsIssue("bibliography.bib", 34)
        self.assertEqual(issue.file_path, "bibliography.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertEqual(
            issue.message,
            "Title words in all capital letters should be wrapped in braces.",
        )

    # def test_hyphenated_issue(self):
    #    """Test the HyphenatedIssue class."""
    #    issue = title.HyphenatedIssue("bibliography.bib", 34)
    #    self.assertEqual(issue.file_path, "bibliography.bib")
    #    self.assertEqual(issue.line_number, 34)
    #    self.assertEqual(
    #        issue.message,
    #        "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}",
    #    )


class CheckTest(unittest.TestCase):
    """Test cases for the check() function."""

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.checker = bibcheck.checks.title.TitleChecker()

    def test_all_caps_ok(self):
        """Test title lines that do not have issues with all capital words."""
        lines = [
            bibcheck.checker.Line("title={Hamlet},", "references.bib", 10),
            bibcheck.checker.Line(
                "author={Shakespeare, William},", "references.bib", 11
            ),
        ]
        for line in lines:
            with self.subTest():
                self.assertFalse(self.checker.check(line))

    def test_all_cpas_bad(self):
        """Test title lines that have issues with words in all capital letters."""
        lines = [
            bibcheck.checker.Line("title={HAMLET},", "references.bib", 11),
            bibcheck.checker.Line("title={HaMLet},", "references.bib", 11),
        ]
        for line in lines:
            with self.subTest():
                issues = self.checker.check(line)
                self.assertEqual(len(issues), 1)
                self.assertIsNotNone(issues[0])
                self.assertEqual(issues[0].file_path, "references.bib")
                self.assertEqual(issues[0].line_number, 11)
                self.assertEqual(
                    issues[0].message,
                    "Title words in all capital letters should be wrapped in braces.",
                )
