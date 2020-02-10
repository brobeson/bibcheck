"""Unit test for the title initials check."""

import unittest
import bibcheck.issue
import bibcheck.checks.title as title


class IssuesTest(unittest.TestCase):
    """Test cases for the title issue classes."""

    def test_intials_issue(self):
        """Test the AllCapsIssue class."""
        issue = title.AllCapsIssue("bibliography.bib", 34)
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

    def test_all_caps_ok(self):
        """Test title lines that do not have issues with all capital words."""
        cases = [
            # (test line, test context)
            ("  title={Hamlet},", bibcheck.issue.Context("references.bib", 10)),
            (
                "author={Shakespeare, William},",
                bibcheck.issue.Context("references.bib", 11),
            ),
        ]
        for case in cases:
            with self.subTest():
                self.assertFalse(title.check(case[0], case[1]))

    def test_all_cpas_bad(self):
        """Test title lines that have issues with words in all capital letters."""
        cases = [
            # (test line, test context)
            ("title={HAMLET},", bibcheck.issue.Context("references.bib", 11)),
            ("title={HaMLet},", bibcheck.issue.Context("references.bib", 11)),
        ]
        for case in cases:
            with self.subTest():
                issues = title.check(case[0], case[1])
                self.assertEqual(len(issues), 1)
                self.assertIsNotNone(issues[0])
                self.assertEqual(issues[0].file_path, "references.bib")
                self.assertEqual(issues[0].line_number, 11)
                self.assertEqual(
                    issues[0].message,
                    "Title words in all capital letters should be wrapped in braces.",
                )
