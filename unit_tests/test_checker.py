"""Unit test for the bibcheck.checker module."""

import unittest

import bibcheck.checker


class LineTest(unittest.TestCase):
    """Test the Line class."""

    def test_line(self):
        """Test the Line class."""
        line = bibcheck.checker.Line("Lorum ipsum delor", "references.bib", 34)
        self.assertEqual(line.text, "Lorum ipsum delor")
        self.assertEqual(line.file_path, "references.bib")
        self.assertEqual(line.line_number, 34)


class IssueTest(unittest.TestCase):
    """Test the Issue class."""

    def test_issue(self):
        """Test the Issue class."""
        issue = bibcheck.checker.Issue("references.bib", 34)
        self.assertEqual(issue.file_path, "references.bib")
        self.assertEqual(issue.line_number, 34)
        self.assertTrue(issue)
