"""This module will be responsible for any helper functions used in the report generation process."""
import openpyxl
from os.path import exists
from pandas import DataFrame, isna
from . import PaymentColumnNames, SalesColumnNames, generic, errors
from .excel_controller import ExcelController
from datetime import datetime

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
            else: return "Misc"

        category_key = SalesColumnNames.CATEGORY.value
        sales_df[category_key] = sales_df[category_key].apply(clean_category)

        return sales_df

    @staticmethod
    def clean_payments(payments_df_dirty: DataFrame) -> DataFrame:
        """
        Cleans the payments DataFrame by removing any unnecessary prefixes or suffixes from the column values.

        Parameters:
            payments_df (DataFrame): The DataFrame containing the payments data.

        Returns:
            DataFrame: The cleaned payments DataFrame.
        """
        
        payments_df = payments_df_dirty.copy()

        # Create a Session Column
        def get_session(date: str) -> str:
            """
            Parses the input date string to extract the hour, then uses the hour to classify the session using the get_session_classification function.

            Args:
                date (str): The date string to extract the session hour from.

            Returns:
                str: The session classification based on the hour extracted from the date.
            """
            if "PM" in date or "AM" in date:
                dt = datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")
            else:
                try:
                    dt = datetime.strptime(date, "%m/%d/%Y %H:%M")
                except ValueError:
                    dt = datetime.strptime(date, "%m/%d/%Y")

            hour = dt.hour
            return generic.get_session_classification(hour)
        
        payments_df[PaymentColumnNames.SESSION.value] = payments_df[PaymentColumnNames.DATE.value].apply(get_session)

        return payments_df

    @staticmethod
    def validate_file_exists(filepath: str, error: bool = True) -> bool:
        """
        Validates if a file exists at the given filepath.

        Args:
            filepath (str): The path to the file.

        Returns:
            bool: True if the file exists, False otherwise.

        Raises:
            FileNotFoundError: If the file does not exist, and `error` is True.
        """
        if exists(filepath):
            return True
        if error: raise FileNotFoundError("File in filepath: " + filepath + " does not exist")
        return False
    
    @staticmethod
    def calculate_total_by_payment_type(payments_df: DataFrame) -> dict:
        """
        Calculate the total amount spent by payment type.

        Parameters:
            payments_df (DataFrame): The DataFrame containing payment data.

        Returns:
            dict: A dictionary where the keys are the payment types and the values are dictionaries 
                containing the currency as keys and the total amount spent as values.

        """
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
        
        payment_totals = {k: {currency: round(amount, 2) for currency, amount in v.items()} for k, v in payment_totals.items()}
        return payment_totals
    
    @staticmethod
    def calculate_total_by_meal_and_payment_type(payments_df: DataFrame) -> dict:
        """
        Calculate the total amount spent by meal and payment type.

        Parameters:
            payments_df (DataFrame): The DataFrame containing payment data.

        Returns:
            dict: A dictionary where the keys are the session types, and the values are dictionaries 
                containing the payment types as keys and dictionaries of currency and total amount spent as values.
        """
        session_totals = {}

        for _, row in payments_df.iterrows():
            payment_type = row[PaymentColumnNames.PAYMENT_TYPE.value]
            session = row[PaymentColumnNames.SESSION.value]
            currency = row[PaymentColumnNames.CURRENCY.value]
            amount = row[PaymentColumnNames.AMOUNT.value]

            if session in session_totals:
                if payment_type in session_totals[session]:
                    if currency not in session_totals[session][payment_type]:
                        session_totals[session][payment_type][currency] = amount
                    else:
                        session_totals[session][payment_type][currency] += amount
                else:
                    session_totals[session].update({payment_type: {currency: amount}})
            else:
                session_totals.update({session: {payment_type: {currency: amount}}})

        session_totals = {k: {payment_type: {currency: round(amount, 2) for currency, amount in v.items()} for payment_type, v in session_totals_inner.items()} for k, session_totals_inner in session_totals.items()}

        return session_totals

    @staticmethod
    def calculate_total_by_subcategory(sales_df: DataFrame) -> dict:
        """
        Calculate the total amount spent by subcategory.

        Parameters:
            sales_df (DataFrame): The DataFrame containing sales data.

        Returns:
            dict: A dictionary where the keys are the session types, and the values are dictionaries 
                containing the subcategories as keys and the total amount spent as values.
        """
        payment_categories = {}

        for _, row in sales_df.iterrows():
            category = row[SalesColumnNames.CATEGORY.value]
            session = row[SalesColumnNames.SESSION.value]
            amount = row[SalesColumnNames.AMOUNT.value]

            if session in payment_categories:
                if category in payment_categories[session]:
                    payment_categories[session][category] += amount
                else:
                    payment_categories[session].update({category: amount})
            else:
                payment_categories.update({session: {category: amount}})
            
        payment_categories = {k: {category: round(amount, 2) for category, amount in v.items()} for k, v in payment_categories.items()}

        return payment_categories
    
    @staticmethod
    def calculate_guests_by_meal_type(sales_df: DataFrame) -> dict:
        """
        Calculate the number of guests by meal type.

        Parameters:
            sales_df (DataFrame): The DataFrame containing sales data.

        Returns:
            dict: A dictionary where the keys are the session types and the values are the total number of guests for each session type.
        """
        guests_by_meal = {}

        filtered_df = sales_df.drop_duplicates(SalesColumnNames.ID.value, keep='first')

        for _, row in filtered_df.iterrows():
            session = row[SalesColumnNames.SESSION.value]
            guests = row[SalesColumnNames.GUESTS.value]

            if isna(guests):
                continue
            
            if session in guests_by_meal:
                guests_by_meal[session] += guests
            else:
                guests_by_meal.update({session: guests})

        return guests_by_meal
    
    @staticmethod
    def calculate_vat(sales_df: DataFrame) -> float:
        """
        Calculate the sum of the VAT column in the given sales DataFrame.

        Args:
            sales_df (DataFrame): The DataFrame containing sales data.

        Returns:
            float: The sum of the VAT column in the sales DataFrame. If the VAT column does not exist, returns 0.
        """
        if SalesColumnNames.VAT.value in sales_df:
            return sales_df[SalesColumnNames.VAT.value].sum()
        return 0
    
    @staticmethod
    def calculate_levy(sales_df: DataFrame) -> float:
        """
        Calculates the total levy amount from the sales DataFrame.

        Parameters:
            sales_df (DataFrame): The DataFrame containing sales data.

        Returns:
            float: The total levy amount from the sales DataFrame.
        """
        if SalesColumnNames.LEVY.value in sales_df:
            return sales_df[SalesColumnNames.LEVY.value].sum()
        return 0

    @staticmethod
    def create_excel_controller(filepath: str) -> ExcelController:
        """
        Creates an instance of the ExcelController class.

        Parameters:
            filepath (str): The filepath to the Excel file.

        Returns:
            ExcelController: An instance of the ExcelController class.
        """
        return ExcelController(filepath)
    
    @staticmethod
    def parse_cell(data_key: str, cell_info: str | dict, controller: ExcelController) -> str:
        """
        Parses a cell in the Excel sheet and returns the cell location.

        Parameters:
            data_key (str): The key to access the data.
            cell_info (str | dict): Either the cell reference, or a dictionary containing other meta information
            controller (ExcelController): The Excel controller to interact with the Excel sheet.

        Returns:
            str: The cell location.

        Raises:
            InvalidReportFormatException: If the title format in the Report_Format.json is invalid.
        """
        if type(cell_info) == dict:
            if "FIELD" in cell_info:
                cell_loc = cell_info["FIELD"]
            if "TITLE" in cell_info:
                title = cell_info["TITLE"]
                if type(title) is dict and "VAL" in title and "REF" in title:
                    controller.insert_data_into_cell(title["VAL"], title["REF"]) 
                elif type(title) == str:
                    controller.insert_data_into_cell(data_key, cell_info["TITLE"])
                else:
                    raise errors.InvalidReportFormatException(f"Invalid title format for {title} in the Report_Format.json. Expected a dictionary with 'VAL' and 'REF', where 'VAL' is a named title, and 'REF' is the cell to store the title in, or a string containing the cell reference.")
            
            if "FIELDS" in cell_info:
                for field_data in cell_info["FIELDS"][:-1]:
                    cell = ReportGeneratorHelper.parse_cell(data_key, field_data, controller)
                    if cell:
                        controller.insert_data_into_cell(cell_info, cell)
                cell_loc = ReportGeneratorHelper.parse_cell(data_key, cell_info["FIELDS"][-1], controller)
        if type(cell_info) == str:
            cell_loc = cell_info

        return cell_loc
    
    @staticmethod
    def fill_matrix(spent_by_sub_category_dict: dict, matrix_form: dict, controller: ExcelController) -> None:
        """
        Fills the matrix with data from the spent_by_sub_category_dict using the matrix_form layout and the provided ExcelController.

        Parameters:
            spent_by_sub_category_dict (dict): A dictionary containing the data to be filled into the matrix.
            matrix_form (dict): A dictionary defining the structure of the matrix.
            controller (ExcelController): An instance of the ExcelController class to interact with the Excel sheet.

        Returns:
            None
        """

        for session, session_data in spent_by_sub_category_dict.items():
            row = matrix_form['Rows'][session]
            for subcategory, cost in session_data.items():
                col = matrix_form['Columns'][subcategory]
                cell = ReportGeneratorHelper.parse_cell(subcategory, f"{col}{row}", controller)
                controller.insert_data_into_cell(cost, cell)
        return None
    
    @staticmethod
    def fill_card_info(spent_by_payment_type_dict: dict, card_form: dict, controller: ExcelController) -> dict:
        """
        Fills the card information based on the spent_by_payment_type_dict, using the card_form layout and the provided ExcelController.

        Parameters:
            spent_by_payment_type_dict (dict): A dictionary containing the payment type data.
            card_form (dict): A dictionary defining the structure of the card form.
            controller (ExcelController): An instance of the ExcelController class to interact with the Excel sheet.

        Returns:
            dict: A dictionary containing the foreign currency information.
        """
        
        foreign_currency: dict = {}

        for payment_type, payment_data in spent_by_payment_type_dict.items():
            if payment_type == "Cash": continue

            total = 0

            for currency, amount in payment_data.items():
                total += amount * generic.get_exch_rate(currency)
                if currency != "BBD":
                    if currency in foreign_currency:
                        foreign_currency[currency] += amount
                    else:
                        foreign_currency[currency] = amount

            cell = ReportGeneratorHelper.parse_cell(payment_type, card_form[payment_type], controller)
            controller.insert_data_into_cell(total, cell)

        return foreign_currency
    
    @staticmethod
    def fill_foreign_currency(foreign_currency_dict: dict, foreign_currency_form: dict, controller: ExcelController) -> None:
        """
        Fills the foreign currency information in the Excel sheet using the provided foreign currency dictionary, foreign currency form, and Excel controller.

        Parameters:
            foreign_currency_dict (dict): A dictionary containing the foreign currency information.
            foreign_currency_form (dict): A dictionary defining the structure of the foreign currency form.
            controller (ExcelController): An instance of the ExcelController class to interact with the Excel sheet.

        Returns:
            None
        """

        for currency, amount in foreign_currency_dict.items():
            cell = foreign_currency_form[currency]

            controller.insert_data_into_cell(amount, cell)
        
        return None
    
    @staticmethod
    def fill_guest_covers(guests_covers_dict: dict, guests_covers_form: dict, controller: ExcelController) -> None:
        """
        Fills the guest covers in the Excel sheet using the provided guests covers dictionary, guests covers form, and Excel controller.

        Parameters:
            guests_covers_dict (dict): A dictionary containing the guest covers information.
            guests_covers_form (dict): A dictionary defining the structure of the guests covers form.
            controller (ExcelController): An instance of the ExcelController class to interact with the Excel sheet.

        Returns:
            None
        """

        for session, count in guests_covers_dict.items():
            cell = guests_covers_form[session]
            controller.insert_data_into_cell(count, cell)

        return None