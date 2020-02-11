"""Checks for titles."""

import re

import bibcheck.checker

ALL_CAPS_REGEX = re.compile(r'title\s*=\s*[{"].*[^{][A-Z0-9]+[^}].*["}]')


class AllCapsIssue(bibcheck.checker.Issue):
    """Represents an issue words in all capitals, but not wrapped in braces."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "Title words in all capital letters should be wrapped in braces."


# class HyphenatedIssue(bibcheck.checker.Issue):
#    """Represents an issue with hyphenated lowercase names that are not in braces."""
#
#    @property
#    def message(self):
#        """Get the message for this issue."""
#        return "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}"


def check(line: bibcheck.checker.Line):
    """
    Check if a title line contains any problems.

    :param bibcheck.checker.Line context: The line of text to check, along with file context
        information.
    :return: ``None`` if the given ``line`` passes the check.
    :return: A list of issues if any problems are found.
    :rtype: bibcheck.checks.author.Issue
    """
    issues = []
    if ALL_CAPS_REGEX.search(line.text):
        issues.append(
            bibcheck.checks.title.AllCapsIssue(line.file_path, line.line_number)
        )
    # if HYPHENATED_REGEX.search(line.text):
    #    issues.append(
    #        bibcheck.checks.author.HyphenatedIssue(
    #            line.file_path, line.line_number
    #        )
    #    )
    return issues
