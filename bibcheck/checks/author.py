"""A check to ensure author initials are separated by a space."""

import re

import bibcheck.checker

INITIALS_REGEX = re.compile(r'author\s*=\s*[{"].*[A-Z]\.?[A-Z]\.?.*["}]')
HYPHENATED_REGEX = re.compile(r'author\s*=\s*[{"].*-[a-z].*["}]')


class InitialsIssue(bibcheck.checker.Issue):
    """Represents an issue with missing spaces in author initials."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "Author initials must be separated by a space."


class HyphenatedIssue(bibcheck.checker.Issue):
    """Represents an issue with hyphenated lowercase names that are not in braces."""

    @property
    def message(self):
        """Get the message for this issue."""
        return (
            "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}"
        )


def check(line: bibcheck.checker.Line):
    """
    Check if an author line contains any problems.

    :param bibcheck.issue.Context line: The line of text to check, along with file context
        information.
    :return: ``None`` if the given ``line`` passes the check.
    :return: An issue if the given ``line`` fails the check.
    :rtype: bibcheck.checks.author.Issue
    """
    issues = []
    if INITIALS_REGEX.search(line.text):
        issues.append(
            bibcheck.checks.author.InitialsIssue(line.file_path, line.line_number)
        )
    if HYPHENATED_REGEX.search(line.text):
        issues.append(
            bibcheck.checks.author.HyphenatedIssue(line.file_path, line.line_number)
        )
    return issues
