"""A check to ensure author initials are separated by a space."""

import re

import bibcheck.issue

INITIALS_REGEX = re.compile(r'author\s*=\s*[{"].*[A-Z]\.?[A-Z]\.?.*["}]')
HYPHENATED_REGEX = re.compile(r'author\s*=\s*[{"].*-[a-z].*["}]')


class InitialsIssue(bibcheck.issue.Issue):
    """Represents an issue with missing spaces in author initials."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "Author initials must be separated by a space."


class HyphenatedIssue(bibcheck.issue.Issue):
    """Represents an issue with hyphenated lowercase names that are not in braces."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}"


def check(line: str, context: bibcheck.issue.Context):
    """
    Check if an author line contains any problems.

    :param str line: A line of text from a BibTeX or BibLaTeX file.
    :param bibcheck.issue.Context context: The context within the BibTeX or BibLaTeX file for the
        given ``line``.
    :return: ``None`` if the given ``line`` passes the check.
    :return: An issue if the given ``line`` fails the check.
    :rtype: bibcheck.checks.author.Issue
    """
    issues = []
    if INITIALS_REGEX.search(line):
        issues.append(
            bibcheck.checks.author.InitialsIssue(
                context.file_path, context.line_number
            )
        )
    if HYPHENATED_REGEX.search(line):
        issues.append(
            bibcheck.checks.author.HyphenatedIssue(
                context.file_path, context.line_number
            )
        )
    return issues
