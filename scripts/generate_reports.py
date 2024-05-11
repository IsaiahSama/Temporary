"""This file will be responsible for handling the generation of Daily reports."""
import pandas as pd
from pandas import DataFrame
from datetime import datetime

from utils import *

class ReportGenerator:
    def __init__(self, restaurant_name: RestaurantNames ):
        self.restaurant_name = restaurant_name
        self.helper = ReportGeneratorHelper

    def generate_daily_report(self, date: datetime=None) -> None:

        final_results = {}

        # Step 0: Prepare the date, and load in the correct formats.
        target_date = date or datetime.now()
        
        # Step 1: Load the csv with either the provided date, or the current one into dataframes.

        # Step 2: Run calculations on the dataframes

        # Step 3: Save the results into the correct spreadsheeet

        # Step 4: Store data in database

        # Step 5: Create the Rolling 8 Week Report

        # Step 6: Export data to QuickBooks Format.

    def get_df_from_csv(self, filepath: str, format: dict) -> DataFrame:
        pass

    def calculations(self, sales_df: DataFrame, billing_df: DataFrame) -> dict:
        pass

    def render_daily_template(self, data: dict, filename: str) -> bool:
        pass

    def update_database(self, data:dict) -> None:
        pass

    def update_running_report(self, data: dict) -> None:
        pass

    def export_to_quickbooks(self, data: dict) -> None:
        pass