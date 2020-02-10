"""Checks for titles."""

import re

import bibcheck.issue

ALL_CAPS_REGEX = re.compile(r'title\s*=\s*[{"].*[^{][A-Z0-9]+[^}].*["}]')


class AllCapsIssue(bibcheck.issue.Issue):
    """Represents an issue words in all capitals, but not wrapped in braces."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "Title words in all capital letters should be wrapped in braces."


#class HyphenatedIssue(bibcheck.issue.Issue):
#    """Represents an issue with hyphenated lowercase names that are not in braces."""
#
#    @property
#    def message(self):
#        """Get the message for this issue."""
#        return "Author names with hyphenated lowercase should use braces: Na-me -> Na{-me}"


def check(line: str, context: bibcheck.issue.Context):
    """
    Check if a title line contains any problems.

    :param str line: A line of text from a BibTeX or BibLaTeX file.
    :param bibcheck.issue.Context context: The context within the BibTeX or BibLaTeX file for the
        given ``line``.
    :return: ``None`` if the given ``line`` passes the check.
    :return: A list of issues if any problems are found.
    :rtype: bibcheck.checks.author.Issue
    """
    issues = []
    if ALL_CAPS_REGEX.search(line):
        issues.append(
            bibcheck.checks.title.AllCapsIssue(
                context.file_path, context.line_number
            )
        )
    #if HYPHENATED_REGEX.search(line):
    #    issues.append(
    #        bibcheck.checks.author.HyphenatedIssue(
    #            context.file_path, context.line_number
    #        )
    #    )
    return issues
