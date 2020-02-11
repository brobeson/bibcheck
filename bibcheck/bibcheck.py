"""Check BibTeX and BibLaTeX files for common errors."""

import argparse
import glob
import os.path
import sys

import bibcheck.reporters
import bibcheck.checks.author


BIBTEX_FILE = "bibtex"
LATEX_FILE = "latex"


def main():
    """The main entry point for the application."""
    arguments = _parse_command_line()
    try:
        files_to_check = _get_files_to_check(arguments.path)
    except FileNotFoundError as exception:
        sys.exit(str(exception))
    if not files_to_check:
        sys.exit(f"No LaTeX, BibTeX, or BibLaTeX files are in {arguments.path}.")
    _check_files(files_to_check)
    sys.exit(0)


def _parse_command_line():
    parser = argparse.ArgumentParser(
        description="Scan a LaTeX, BibTeX, or BibLaTeX file for common errors and lint.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--action",
        default="report",
        type=str,
        choices=["fix", "report", "report-and-fix"],
        help="The type of action BibCheck should take when it finds an issue. Not all issues can "
        "be fixed; those are just reported regardless of this option.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="./",
        type=str,
        help="The path to the LaTeX, BibTeX, or BibLaTeX file(s) to scan. If this a directory, all "
        ".tex and .bib files will be scanned.",
    )
    arguments = parser.parse_args()
    arguments.path = os.path.abspath(os.path.expanduser(arguments.path))
    return arguments


def _get_files_to_check(path_argument: str) -> list:
    if not os.path.exists(path_argument):
        raise FileNotFoundError(f"{path_argument} does not exist")
    if os.path.isdir(path_argument):
        # glob.glob() appears to not support {} in the pattern. So this function cannot search for
        # *.{bib,tex}. Instead, invoke glob.glob() a couple times.
        files = glob.glob(path_argument + "**/*.tex", recursive=True)
        files.extend(glob.glob(path_argument + "**/*.bib", recursive=True))
        files.sort()
        return files
    return [path_argument]


def _check_files(files: list) -> None:
    reporter = bibcheck.reporters.DefaultReporter()
    for file_path in files:
        try:
            file_type = _get_file_type(file_path)
            with open(file_path) as file_:
                lines = file_.readlines()
            if file_type == BIBTEX_FILE:
                _check_bibtex_lines(reporter, lines, file_path)
        except ValueError as exception:
            print(exception)


def _check_bibtex_lines(reporter, lines, file_path) -> None:
    checkers = [
        bibcheck.checks.author.AuthorChecker()
    ]
    for line_number, line in enumerate(lines, start=1):
        for checker in checkers:
            issue = checker.check(bibcheck.checker.Line(line, file_path, line_number))
            if issue:
                reporter.report_issue(issue)


def _get_file_type(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    if extension == ".bib":
        return BIBTEX_FILE
    if extension == ".tex":
        return LATEX_FILE
    raise ValueError(f"{file_path} is not a known file type.")


if __name__ == "__main__":
    main()
