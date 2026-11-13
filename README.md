# CSV Header Check

A small Python CLI for checking CSV headers before importing data. It reports missing, duplicate and unnamed columns. Extra columns are allowed, and the file is read without modification.

Run with Python 3:

```sh
python check_headers.py timetable.csv "Course Code" Day "Start Time"
```

Exit status is 0 for a valid header, 1 for header problems and 2 if the file cannot be read or parsed. Header matching is case-sensitive and ignores surrounding whitespace. CSV files can include a UTF-8 byte order mark.
