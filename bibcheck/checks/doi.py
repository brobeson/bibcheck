"""A check to ensure author initials are separated by a space."""

import re
import bibcheck.checker


class Issue(bibcheck.checker.Issue):
    """Represents an issue with DOIs."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "DOI entries should just contain the DOI."


class DoiChecker(bibcheck.checker.Checker):  # pylint: disable=too-few-public-methods
    """
    Check for issues with DOI entries.

    1. DOI entries should not be a URL: doi={10.1000/foo} instead of
       doi={https://doi.org/10.1000/foo}.
    """

    def __init__(self):
        self.__doi_url_regex = re.compile(r'doi\s*=\s*[{"]\s*https://doi.org/.*["}]')

    def check(self, line: bibcheck.checker.Line):
        """
        Check if a line contains any DOI issues.

        :param bibcheck.checker.Line line: The line of text to check, along with file context
            information.
        :return: A list of issues if the given ``line`` contains DOI problems.
        :rtype: list of bibcheck.checks.doi.Issue objects.
        """
        if self.__doi_url_regex.search(line.text):
            return bibcheck.checks.doi.Issue(line.file_path, line.line_number)
        return []
