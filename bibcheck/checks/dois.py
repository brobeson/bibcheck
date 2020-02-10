"""A check to ensure author initials are separated by a space."""

import re
import bibcheck.issue

DOI_URL_REGEX = re.compile(r'doi\s*=\s*[{"]\s*https://doi.org/.*["}]')


class Issue(bibcheck.issue.Issue):
    """Represents an issue with DOIs."""

    @property
    def message(self):
        """Get the message for this issue."""
        return "DOI entries should just contain the DOI."


def check(line: str, context: bibcheck.issue.Context):
    """
    Check if a DOI line contains a URL.

    :param str line: A line of text from a BibTeX or BibLaTeX file.
    :param bibcheck.issue.Context context: The context within the BibTeX or BibLaTeX file for the
        given ``line``.
    :return: ``None`` if the given ``line`` passes the check.
    :return: An issue if the given ``line`` fails the check.
    :rtype: bibcheck.checks.dois.Issue
    """
    if DOI_URL_REGEX.search(line):
        return bibcheck.checks.dois.Issue(
            context.file_path, context.line_number
        )
    return None
