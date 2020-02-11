"""The Issue class, which encapsulates a bibliography error."""


class Line:
    """Context with in the file for a line."""

    def __init__(self, text: str, file_path: str, line_number: int) -> None:
        self.__text = text
        self.__file_path = file_path
        self.__line_number = line_number

    @property
    def file_path(self):
        """The path to the file from this line of text is from."""
        return self.__file_path

    @property
    def line_number(self):
        """The line number within the file for this line of text."""
        return self.__line_number

    @property
    def text(self):
        """The line of text from the file."""
        return self.__text


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

    @property
    def message(self):
        """The message for this issue."""
        raise NotImplementedError("The derived class needs to implement this property.")

    def __bool__(self):
        return True


class Checker:  # pylint: disable=too-few-public-methods
    """
    Base class for all checks.

    Checks are implemented as classes so they can preserve state if necessary. Checks must inherit
    from this class, and provide an implementation of the check() method.
    """

    def check(self, line: Line) -> list:
        """
        The method that does the checking for a line of text.

        :param bibcheck.checker.Line: The text to check, along with file context information.
        :return: A list of issues for the given ``line``. If no issues are found, the list will be
            empty.
        :rtype: list
        :raises NotImplementedError: This is always raised by this method. Derived classes must
            override this method to avoid the exception.

        This is a "pure virtual" method. If a derived class fails to implement this method, a
        ``NotImplementedError`` is raised.
        """
        raise NotImplementedError(
            "Checker.check() is not implemented by design; a derived class "
            "must implement it."
        )
