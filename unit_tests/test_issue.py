"""Unit test for the bibcheck.issue module."""

import unittest

import bibcheck.issue


class ContextTest(unittest.TestCase):
    """Test the Context class."""

    def test_context(self):
        """Test the Context class."""
        context = bibcheck.issue.Context("references.bib", 34)
        self.assertEqual(context.file_path, "references.bib")
        self.assertEqual(context.line_number, 34)


class IssueTest(unittest.TestCase):
    """Test the Issue class."""

    def test_issue(self):
        """Test the Issue class."""
        issue = bibcheck.issue.Issue("references.bib", 34)
        self.assertEqual(issue.file_path, "references.bib")
        self.assertEqual(issue.line_number, 34)

    def test_boolean_conversion(self):
        """Test Issue.__bool__()."""
        issue = bibcheck.issue.Issue("references.bib", 34)
        self.assertTrue(issue)
