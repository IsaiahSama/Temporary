"""This module is responsible for the manipulation of workbooks."""
import openpyxl

class ExcelController:
    """This class is responsible for the manipulation of workbooks."""

    def __init__(self, file_path: str) -> None:
        """
        Initializes a new instance of the ExcelController class.

        Parameters:
            file_path (str): The path to the Excel file.

        Returns:
            None
        """
        self.file_path: str = file_path
        self.workbook : openpyxl.Workbook = self.load_workbook(file_path)
        self.sheet = self.workbook.active

    def load_workbook(self, file_path: str) -> openpyxl.Workbook:
        """
        Loads an Excel workbook from a file path.

        Args:
            file_path (str): The path to the Excel file.

        Returns:
            openpyxl.Workbook: The loaded workbook.
        """
        return openpyxl.load_workbook(file_path)
    
    def change_sheet(self, sheet_name: str) -> None:
        """
        Changes the active sheet of the workbook.

        Args:
            sheet_name (str): The name of the sheet to be set as active.

        Returns:
            None
        """
        self.sheet = self.workbook[sheet_name]

    def insert_data_into_cell(self, data: int | str | float, cell: str) -> None:
        """
        Inserts data into a cell in the workbook.

        Args:
            data (int | str | float): The data to be inserted into the cell.
            cell (str): The cell address to insert the data.

        Returns:
            None
        """
        self.sheet[cell] = data

    def save(self, filename: str) -> None:
        """
        Saves the workbook to a file.

        Args:
            filename (str): The name of the file to save the workbook to.

        Returns:
            None
        """
        self.workbook.save(filename)