"""A check to ensure author initials are separated by a space."""

import re

import bibcheck.issue

INITIALS_EXPRESSION = re.compile(r"[A-Z]\.[A-Z]\.")


class Issue(bibcheck.issue.Issue):
    """Represents an issue with missing spaces in author initials."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "Author initials must be separated by a space."


def check(line: str, context: bibcheck.issue.Context):
    """
    Check if a line contains author initials that are missing a space.

    :param str line: A line of text from a BibTeX or BibLaTeX file.
    :param bibcheck.issue.Context context: The context within the BibTeX or BibLaTeX file for the
        given ``line``.
    :return: ``None`` if the given ``line`` passes the check.
    :return: An issue if the given ``line`` fails the check.
    :rtype: bibcheck.checks.author_initials.Issue
    """
    if "author" in line:
        if INITIALS_EXPRESSION.search(line):
            return bibcheck.checks.author_initials.Issue(
                context.file_path, context.line_number
            )
    return None
