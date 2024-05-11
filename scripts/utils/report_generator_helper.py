"""This module will be responsible for any helper functions used in the report generation process."""
from os.path import exists
from pandas import DataFrame
from . import PaymentColumnNames

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
    
    @staticmethod
    def calculate_total_by_payment_type(payments_df: DataFrame) -> dict:
        payment_totals = {}
        for _, row in payments_df.iterrows():
            payment_type = row[PaymentColumnNames.PAYMENT_TYPE.value]
            amount = row[PaymentColumnNames.AMOUNT.value]
            currency = row[PaymentColumnNames.CURRENCY.value]

            if payment_type in payment_totals:
                if currency not in payment_totals[payment_type]:
                    payment_totals[payment_type][currency] = amount
                else:
                    payment_totals[payment_type][currency] += amount
            else:
                payment_totals.update({payment_type: {currency: amount}})
        return payment_totals
    
    @staticmethod
    def calculate_total_by_meal_type(sales_df: DataFrame) -> dict:
        payment_totals = {}

        for _, row in sales_df.iterrows():
            pass
