"""A check to ensure author initials are separated by a space."""

import re

import bibcheck.checker


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


class AuthorChecker(bibcheck.checker.Checker):  # pylint: disable=too-few-public-methods
    """
    Checks related to author data.

    1. Author initials should have spaces: E. B. White instead of E.B. White or EB White.
    2. Hyphenated names, with a lowercase letter after the hyphen, should wrap the hyphenated
       section in braces: Le{-chen} instead of Le-chen.
    """

    def __init__(self):
        self.__initials_regex = re.compile(r'author\s*=\s*[{"].*[A-Z]\.?[A-Z]\.?.*["}]')
        self.__hyphenated_regex = re.compile(r'author\s*=\s*[{"].*-[a-z].*["}]')

    def check(self, line: bibcheck.checker.Line):
        """
        Check if an author line contains any problems.

        :param bibcheck.issue.Context line: The line of text to check, along with file context
            information.
        :return: A list of issues if the given ``line`` has any problems.
        :rtype: list of bibcheck.checks.author.Issue objects.
        """
        issues = []
        if self.__initials_regex.search(line.text):
            issues.append(
                bibcheck.checks.author.InitialsIssue(line.file_path, line.line_number)
            )
        if self.__hyphenated_regex.search(line.text):
            issues.append(
                bibcheck.checks.author.HyphenatedIssue(line.file_path, line.line_number)
            )
        return issues
