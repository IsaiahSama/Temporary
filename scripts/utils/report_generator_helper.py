"""This module will be responsible for any helper functions used in the report generation process."""
from os.path import exists


class ReportGeneratorHelper:
    """This class will contain any helper functions used in the report generation process."""

    @staticmethod
    def validate_file_exists(filepath: str) -> bool:
        """
        Validates if a file exists at the given filepath.

        Args:
            filepath (str): The path to the file.

        Returns:
            bool: True if the file exists, False otherwise.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if exists(filepath):
            return True
        raise FileNotFoundError("File in filepath: " + filepath + " does not exist")