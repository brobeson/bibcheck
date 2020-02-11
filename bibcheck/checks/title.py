"""Checks for titles."""

import re

import bibcheck.checker


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


class TitleChecker(bibcheck.checker.Checker):  # pylint: disable=too-few-public-methods
    """
    Check lines for problems with titles.

    1. Words in a title that are all uppercase should be wrapped in braces: title={A Novel {GPU}
       Architecture} instead of title={A Novel GPU Architecture}.
    """

    def __init__(self):
        self.__all_caps_regex = re.compile(
            r'title\s*=\s*[{"].*[^{][A-Z0-9][A-Z0-9]+[^}].*["}]'
        )

    def check(self, line: bibcheck.checker.Line):
        """
        Check if a title line contains any problems.

        :param bibcheck.checker.Line context: The line of text to check, along with file context
            information.
        :return: A list of issues if any problems are found.
        :rtype: list of bibcheck.checks.author.Issue objects.
        """
        issues = []
        if self.__all_caps_regex.search(line.text):
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
