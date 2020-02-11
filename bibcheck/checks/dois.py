"""A check to ensure author initials are separated by a space."""

import re
import bibcheck.checker

DOI_URL_REGEX = re.compile(r'doi\s*=\s*[{"]\s*https://doi.org/.*["}]')


class Issue(bibcheck.checker.Issue):
    """Represents an issue with DOIs."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "DOI entries should just contain the DOI."


def check(line: bibcheck.checker.Line):
    """
    Check if a DOI line contains a URL.

    :param bibcheck.checker.Line line: The line of text to check, along with file context
        information.
    :return: ``None`` if the given ``line`` passes the check.
    :return: An issue if the given ``line`` fails the check.
    :rtype: bibcheck.checks.dois.Issue
    """
    if DOI_URL_REGEX.search(line.text):
        return bibcheck.checks.dois.Issue(line.file_path, line.line_number)
    return None
