"""This file will be responsible for handling the generation of Daily reports."""
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from json import dumps

from utils import *

class ReportGenerator:
    def __init__(self, restaurant_name: RestaurantNames, date: datetime=None):
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

    def generate_daily_report(self) -> None:

        final_results = {}

        # Step 0: Prepare the date, and load in the correct format.

        target_date_string = self.date.strftime("%Y%m%d")

        # Step 1: Load the csv with either the provided date, or the current one into dataframes.
        sales_filepath = f"../documents/Upload/{self.restaurant_name.replace(' ', '_')}/{self.restaurant_abrv}-Sales-{target_date_string}.csv"
        payments_filepath = f"../documents/Upload/{self.restaurant_name.replace(' ', '_')}/{self.restaurant_abrv}-Payments-{target_date_string}.csv"

        sales_df_dirty = self.get_df_from_csv(sales_filepath, [SalesColumnNames.DATE.value])
        payments_df_dirty= self.get_df_from_csv(payments_filepath, [PaymentColumnNames.DATE.value]) 

        # Step 2 Part 1: Perform any cleanup operations on dataframes
        sales_df = self.helper.clean_sales(sales_df_dirty)
        payments_df = self.helper.clean_payments(payments_df_dirty)

        # Step 2 Part 2: Run calculations on the dataframes
        self.calculations(sales_df, payments_df)

        # Step 3: Save the results into the correct spreadsheeet

        # Step 4: Store data in database

        # Step 5: Create the Rolling 8 Week Report

        # Step 6: Export data to QuickBooks Format.

    def get_df_from_csv(self, filepath: str, date_fields: list=[]) -> DataFrame:
        self.helper.validate_file_exists(filepath)
        df = pd.read_csv(filepath, parse_dates=date_fields, date_format="%Y-%m-%d", )
        return df

    def calculations(self, sales_df: DataFrame, payments_df: DataFrame) -> dict:
        # Calculate total USD and BBD spent by Payment Type
        spent_by_payment_type = self.helper.calculate_total_by_payment_type(payments_df)
        
        # Calculate total USD and BBD spent by Meal Type
        
        # Calculate total BBD spent by Meal Type sub-categories

        # Calculate number of Guests by Meal Type

        # Calculate Service Charge

        # Calculate VAT

        # Calculate Government Levy

        # Calculate Deposit
        pass

    def render_daily_template(self, data: dict, filename: str) -> bool:
        pass

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