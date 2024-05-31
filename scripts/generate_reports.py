"""This file will be responsible for handling the generation of Daily reports."""
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from json import dumps

from .utils import *

class ReportGenerator:
    def __init__(self, restaurant_name: RestaurantNames, date: datetime=None, root: str=".."):
        """
        Initializes a new instance of the ReportGenerator class.

        Parameters:
            restaurant_name (RestaurantNames): The name of the restaurant for which the reports are generated.
            date (datetime, optional): The date for which the reports are generated. Defaults to the current date.

        Returns:
            None
        """

        self.restaurant_name: str                   = restaurant_name.value[0]
        self.restaurant_abrv: str                   = restaurant_name.value[1]
        self.date:            datetime              = date or datetime.now()
        self.helper:          ReportGeneratorHelper = ReportGeneratorHelper
        self.root:            str                   = root

    def generate_daily_report(self) -> str:
        # Step 0: Prepare the date, and load in the correct format.

        target_date_string = self.date.strftime("%Y%m%d")

        # Step 1: Load the csv with either the provided date, or the current one into dataframes.
        sales_filepath = f"{self.root}/documents/Upload/{self.restaurant_name.replace(' ', '_')}/{self.restaurant_abrv}-Sales-{target_date_string}.csv"
        payments_filepath = f"{self.root}/documents/Upload/{self.restaurant_name.replace(' ', '_')}/{self.restaurant_abrv}-Payments-{target_date_string}.csv"

        sales_df_dirty = self.get_df_from_csv(sales_filepath, [SalesColumnNames.DATE.value])
        payments_df_dirty= self.get_df_from_csv(payments_filepath, [PaymentColumnNames.DATE.value]) 

        # Step 2 Part 1: Perform any cleanup operations on dataframes
        sales_df = self.helper.clean_sales(sales_df_dirty)
        payments_df = self.helper.clean_payments(payments_df_dirty)

        # Step 2 Part 2: Run calculations on the dataframes
        calculated_results = self.calculations(sales_df, payments_df)

        # Step 3: Save the results into the correct spreadsheeet
        output_path = self.render_daily_template(calculated_results)
        print("Report generated and stored in " + output_path)

        # Step 4: Store data in database

        # Step 5: Create the Rolling 8 Week Report

        # Step 6: Export data to QuickBooks Format.
        return output_path

    def get_df_from_csv(self, filepath: str, date_fields: list=[]) -> DataFrame:
        """
        Reads a CSV file from the given filepath and returns a pandas DataFrame.

        Parameters:
            filepath (str): The path to the CSV file.
            date_fields (list, optional): A list of column names to parse as dates. Defaults to an empty list.

        Raises:
            CustomExceptions.BadlyFormattedCSVException: If the CSV file is badly formatted.

        Returns:
            DataFrame: The pandas DataFrame containing the data from the CSV file.
        """
        self.helper.validate_file_exists(filepath)
        try:
            df = pd.read_csv(filepath, parse_dates=date_fields, date_format="%Y-%m-%d")
        except pd.errors.ParserError as e:
            raise CustomExceptions.BadlyFormattedCSVException(f"Error parsing CSV File in {filepath}. CSV is most likely corrupted. More details: {e}")
        except ValueError as e:
            raise CustomExceptions.BadlyFormattedCSVException(f"Error parsing CSV File in {filepath}. Some data may be missing. More details: {e}")

        return df

    def calculations(self, sales_df: DataFrame, payments_df: DataFrame) -> dict:
        """
        Calculate various financial metrics based on the sales and payments data.
        
        Args:
            sales_df (DataFrame): The DataFrame containing sales data.
            payments_df (DataFrame): The DataFrame containing payments data.
        
        Returns:
            dict: A dictionary containing the calculated metrics including total spent by payment type, 
                total spent by meal type, total spent by meal type sub-categories, number of guests by meal type,
                VAT, and Government Levy.
        """
        result_dict = {}

        # Calculate total USD and BBD spent by Payment Type
        spent_by_payment_type = self.helper.calculate_total_by_payment_type(payments_df)
        
        # Calculate total USD and BBD spent by Meal Type
        spent_by_session_type = self.helper.calculate_total_by_meal_and_payment_type(payments_df)
        
        # Calculate total BBD spent by Meal Type sub-categories
        spent_by_sub_categories = self.helper.calculate_total_by_subcategory(sales_df)

        # Calculate number of Guests by Meal Type
        guests_by_meal_type = self.helper.calculate_guests_by_meal_type(sales_df)

        # Calculate VAT
        vat = self.helper.calculate_vat(sales_df)

        # Calculate Government Levy
        levy = self.helper.calculate_levy(sales_df)

        # Put it all together!

        result_dict['PAYMENT_TYPE'] = spent_by_payment_type
        result_dict['SESSION_TYPE'] = spent_by_session_type
        result_dict['SUB_CATEGORY'] = spent_by_sub_categories
        result_dict['GUESTS'] = guests_by_meal_type
        result_dict['VAT'] = vat
        result_dict['LEVY'] = levy

        return result_dict

    def render_daily_template(self, data: dict) -> str:
        """
        Render the daily template for the sales report.

        Parameters:
            data (dict): A dictionary containing various data for the report.

        Returns:
            str: The path to the generated workbook.
        """
        # Establish a string for the current week. Example: 31_Feb_to_6_Jan_Report.xlsx
        template_path = f"{self.root}/scripts/Report_Templates/{self.restaurant_name.replace(' ', '_')}_Sales_Report_Template.xlsx"
        
        report_filename = generic.get_report_filename(self.date, self.restaurant_name, self.restaurant_abrv, self.root)

        controller : ExcelController | None = None
        
        # Load the workbook for the week, or create from template
        if self.helper.validate_file_exists(report_filename, False):
            controller = self.helper.create_excel_controller(report_filename)
        else:
            controller = self.helper.create_excel_controller(template_path)

        # Get the correct day for the sheet name
        report_day = generic.diff_days(self.date, 1)
        sheet_name = report_day.strftime("%a").upper()

        controller.change_sheet(sheet_name)

        # Get the Spreadsheet Format
        form = generic.parse_json_file(f'{self.root}/scripts/Report_Format.json')

        # Add the data to their correct fields
        ## Set Date
        controller.insert_data_into_cell(report_day.strftime("%m/%d/%Y"), form['Date'])

        ## Fill in the Matrix (Makes use of Sub_Category and Session fields. Prices in Barbados)
        self.helper.fill_matrix(data['SUB_CATEGORY'], form['Matrix'], controller)

        ## Set Card Information
        foreign_currency = self.helper.fill_card_info(data['PAYMENT_TYPE'], form['Cards'], controller)
        
        ## Set Foreign Currencies
        self.helper.fill_foreign_currency(foreign_currency, form['Foreign_Currency'], controller)

        ## Guest Covers
        self.helper.fill_guest_covers(data['GUESTS'], form['Guests'], controller)

        ## Set Government Levy
        controller.insert_data_into_cell(data['LEVY'], form['Others']['Levy'])

        # Save the workbook to a new file with the previously established filename.
        controller.save(report_filename)

        # Return the path to the workbook
        return report_filename

    def update_database(self, data:dict) -> None:
        pass

    def update_running_report(self, data: dict) -> None:
        pass

    def export_to_quickbooks(self, data: dict) -> None:
        pass

if __name__ == "__main__":
    target_date = datetime(2024, 5, 9)
    rg = ReportGenerator(RestaurantNames.BISTRO, target_date)
    rg.generate_daily_report()