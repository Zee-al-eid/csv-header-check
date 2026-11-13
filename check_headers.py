"""Check whether a CSV can be mapped to a list of expected columns."""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("columns", nargs="+", help="Required column names")
    args = parser.parse_args()

    try:
        with args.file.open(encoding="utf-8-sig", newline="") as source:
            header = next(csv.reader(source, strict=True), [])
    except (OSError, UnicodeError, csv.Error) as error:
        print(f"Could not read CSV: {error}", file=sys.stderr)
        return 2

    names = Counter(column.strip() for column in header)
    missing = sorted(set(args.columns) - names.keys())
    duplicates = sorted(name for name, count in names.items() if name and count > 1)
    if missing:
        print("Missing columns:", ", ".join(missing))
    if duplicates:
        print("Duplicate columns:", ", ".join(duplicates))
    if not header or "" in names:
        print("The header is empty or has an unnamed column.")
    if missing or duplicates or not header or "" in names:
        return 1
    print("CSV header is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
