# CSV Header Check

A small Python CLI for checking CSV headers before importing data. It reports missing, duplicate and unnamed columns. Extra columns are allowed, and the file is read without modification.

Run with Python 3:

```sh
python check_headers.py timetable.csv "Course Code" Day "Start Time"
```

Exit status is 0 for a valid header, 1 for header problems and 2 if the file cannot be read or parsed. Header matching is case-sensitive and ignores surrounding whitespace. CSV files can include a UTF-8 byte order mark.

Add `--check-rows` to check each record against the header width. Blank lines
are skipped. For a quoted record spanning several lines, the report uses its
ending line number. A width mismatch returns exit status 1.

## Example CSV

```csv
Course Code,Day,Start Time
CS101,Monday,09:00
```

Save this as `timetable.csv` and run the command above. Removing `Start Time` from the header produces a missing column error.

Use --delimiter tab for TSV files or --delimiter ';' for semicolon-separated files.

## Tab-separated input

Run `python check_headers.py --delimiter tab --check-rows export.tsv A B` to validate a TSV export.
