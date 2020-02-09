"""The Issue class, which encapsulates a bibliography error."""


class Context:
    """Context with in the file for a line."""

    def __init__(self, file_path: str, line_number: int) -> None:
        self.__file_path = file_path
        self.__line_number = line_number

    @property
    def file_path(self):
        """Get the file path."""
        return self.__file_path

    @property
    def line_number(self):
        """Get the line number."""
        return self.__line_number


class Issue:
    """Encapsulates the meta-data about a bibliography issue."""

    def __init__(self, file_path: str, line_number) -> None:
        """
        Create an Issue object.

        :param str file_path: The path the file which contains the issue.
        :param int line_number: The line that contains the issue.
        """
        self.__file_path = file_path
        self.__line_number = line_number

    @property
    def file_path(self) -> str:
        """Get the path of the file that contains this issue."""
        return self.__file_path

    @property
    def line_number(self):
        """The line number where the issue was found."""
        return self.__line_number

    def __bool__(self):
        return True
