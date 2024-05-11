"""This module will be responsible for any helper functions used in the report generation process."""
from os.path import exists
from pandas import DataFrame
from . import PaymentColumnNames, SalesColumnNames

class ReportGeneratorHelper:
    """This class will contain any helper functions used in the report generation process."""

    @staticmethod
    def clean_sales(sales_df_dirty: DataFrame) -> DataFrame:
        """
            Cleans the sales DataFrame by removing prefixes from the Session and Category columns.
        
        Args:
            sales_df_dirty (DataFrame): The DataFrame containing sales data.
        
        Returns:
            DataFrame: The cleaned sales DataFrame.
        """

        # Remove the leading N- from Session column.
        # Example: Turning 3-Dinner into Dinner
        sales_df = sales_df_dirty.copy()

        def clean_session(session: str) -> str:
            """
            Splits the session string by '-' and returns the second part.

            Args:
                session (str): The session string to be cleaned.

            Returns:
                str: The cleaned session string.
            """
            return session.split('-')[1]
        
        session_key = SalesColumnNames.SESSION.value
        sales_df[session_key] = sales_df[session_key].apply(clean_session)

        # Removing the leading ABBR/Sales/ from Category column.
        # Example: Turning QPB/Sales/Food into Food or None

        def clean_category(category: str) -> str:
            """
            Cleans the category by removing the leading ABBR/Sales/ from the category string.
            
            Args:
                category (str): The category string to be cleaned.
            
            Returns:
                str: The cleaned category string or None if it does not match the criteria.
            """
            split_category = category.split('/')
            if len(split_category) > 2: return split_category[2]
            else: return None

        category_key = SalesColumnNames.CATEGORY.value
        sales_df[category_key] = sales_df[category_key].apply(clean_category)

        return sales_df

    @staticmethod
    def clean_payments(payments_df: DataFrame) -> DataFrame:
        """
        Cleans the payments DataFrame by removing any unnecessary prefixes or suffixes from the column values.

        Parameters:
            payments_df (DataFrame): The DataFrame containing the payments data.

        Returns:
            DataFrame: The cleaned payments DataFrame.
        """
        return payments_df

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
