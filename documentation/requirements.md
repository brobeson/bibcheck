# Requirements

This tables list the derived requirements, and their implementation status. Each
table is from a section of [Common Errors in
Bibliographies](https://www.ece.ucdavis.edu/~jowens/biberrors.html) by Professor
John Owens.

## Issues in Text: How to Cite Properly

| Status | Requirement |
|:---|:---|
| | Do not use citations as words. |
| | Use a non-breaking space, `~`, before `\cite{}` and `\shortcite{}`. |
| | Prefer `\shortcite{}` over `\cite{}`.
| | Sort references alphabetically by the first author's last name. |

## Issues with Bibliographies

| Status | Requirement |
|:---|:---|
| Done | Separate author initials with spaces. |
| Done | Wrap lowercase hyphenated names in braces. |
| Done | Wrap all-capital abbreviations in the title in braces. |
| Done | Do not wrap the entire title in double braces. |
| In Progress | Use three-letter abbreviations for months. |
| | Use an en-dash between pages in a range. |
| | Double check pages that start with page 1. |
| Done | DOIs should not be URLs. |
| | URL entries should not contain DOIs. |
| | Wrap URLs in a `\url{}` command. |
