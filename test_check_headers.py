import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RowValidationTests(unittest.TestCase):
    def run_cli(self, contents, *flags):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "sample.csv"
            source.write_text(contents, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(Path(__file__).with_name("check_headers.py")),
                 *flags, str(source), "A", "B"],
                capture_output=True, text=True, check=False,
            )

    def test_short_and_long_rows(self):
        result = self.run_cli("A,B\n1\n2,3,4\n", "--check-rows")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Line 2: expected 2 fields, got 1", result.stdout)
        self.assertIn("Line 3: expected 2 fields, got 3", result.stdout)

    def test_multiline_record(self):
        result = self.run_cli('A,B\n"first\nsecond",third\n', "--check-rows")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_header_only_ignores_row_width(self):
        self.assertEqual(self.run_cli("A,B\n1\n").returncode, 0)


    def test_tab_delimiter(self):
        result = self.run_cli('A\tB\n1\t2\n', '--delimiter', 'tab', '--check-rows')
        self.assertEqual(result.returncode, 0, result.stderr)


    def test_semicolon_delimiter(self):
        result = self.run_cli('A;B\n1;2\n', '--delimiter', ';', '--check-rows')
        self.assertEqual(result.returncode, 0, result.stderr)


    def test_missing_required_header(self):
        result = self.run_cli('A,C\n1,2\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Missing columns: B', result.stdout)


    def test_duplicate_after_trimming(self):
        result = self.run_cli('A,B, B \n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Duplicate columns: B', result.stdout)


    def test_unterminated_quote_in_data(self):
        result = self.run_cli('A,B\n1,"unfinished\n', '--check-rows')
        self.assertEqual(result.returncode, 2)
        self.assertIn('Could not read CSV', result.stderr)


if __name__ == "__main__":
    unittest.main()
