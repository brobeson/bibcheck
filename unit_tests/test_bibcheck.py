"""Unit test for the main bibcheck module."""

import os.path
import unittest

import bibcheck.bibcheck


# pylint: disable=protected-access


class GetFilesToCheckTest(unittest.TestCase):
    """Test the function _get_files_to_check()."""

    def test_nonexistent_path(self):
        """Test calling the function with a path that does not exist."""
        self.assertRaises(
            FileNotFoundError,
            bibcheck.bibcheck._get_files_to_check,
            os.path.join(os.path.abspath(__file__), "i_dont_exist"),
        )

    def test_directory(self):
        """Test passing in a directory."""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_paper")
        actual = bibcheck.bibcheck._get_files_to_check(path)
        self.assertEqual(
            actual,
            [os.path.join(path, "paper.tex"), os.path.join(path, "references.bib")],
        )

    def test_file(self):
        """Test passing in a path to a single file."""
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_paper", "references.bib"
        )
        actual = bibcheck.bibcheck._get_files_to_check(path)
        self.assertEqual(actual, [path])


class GetFileTypeTest(unittest.TestCase):
    """Test the function _get_file_type()."""

    def test_get_file_type(self):
        """Test the function _get_file_type()."""
        self.assertEqual(
            bibcheck.bibcheck._get_file_type("references.bib"),
            bibcheck.bibcheck.BIBTEX_FILE,
        )
        self.assertEqual(
            bibcheck.bibcheck._get_file_type("paper.tex"), bibcheck.bibcheck.LATEX_FILE
        )
        self.assertRaises(ValueError, bibcheck.bibcheck._get_file_type, "paper.docx")
