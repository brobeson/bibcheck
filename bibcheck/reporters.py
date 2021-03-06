"""Reporter classes for BibCheck."""

from bibcheck.checker import Issue


class DefaultReporter:  # pylint: disable=too-few-public-methods
    """
    Basic reporter that write to standard output.

    This report is very straight forward. It write a message to standard output. The message is
    formatted like so: "file path:line:message". Here is an example:

        ./references.bib:35:Use an en-dash (--) to separate page numbers in a range.

    """

    def report_issue(self, issue: Issue):
        # pylint: disable=no-self-use
        """Report an issue.

        :param bibcheck.issue.Issue issue: The issue to report.
        """
        print(issue.file_path, issue.line_number, issue.message, sep=":")
