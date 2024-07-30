import os
import unittest
from unittest.mock import patch
import subprocess

# Import the function to be tested
from your_module import analyze_code  # Replace 'your_module' with the actual module name

class TestAnalyzeCode(unittest.TestCase):
    @patch('os.listdir')
    @patch('subprocess.run')
    def test_analyze_code(self, mock_subprocess_run, mock_os_listdir):
        # Mock the list of files in the directory
        mock_os_listdir.return_value = ['test1.py', 'test2.py', 'test3.txt']

        # Call the function
        analyze_code('test_directory')

        # Check that subprocess.run was called for each Python file
        self.assertEqual(mock_subprocess_run.call_count, 4)  # 2 pylint + 2 flake8 for 2 python files

        # Check the exact calls
        expected_calls = [
            unittest.mock.call('pylint test_directory/test1.py', shell=True),
            unittest.mock.call('flake8 test_directory/test1.py', shell=True),
            unittest.mock.call('pylint test_directory/test2.py', shell=True),
            unittest.mock.call('flake8 test_directory/test2.py', shell=True)
        ]
        mock_subprocess_run.assert_has_calls(expected_calls, any_order=True)

    @patch('os.listdir')
    def test_no_python_files(self, mock_os_listdir):
        # Mock the list of files in the directory
        mock_os_listdir.return_value = ['test1.txt', 'test2.md']

        with patch('builtins.print') as mock_print:
            analyze_code('test_directory')
            mock_print.assert_called_once_with("No Python files found in the specified directory.")

if __name__ == '__main__':
    unittest.main()
