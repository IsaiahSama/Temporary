"""This module will contain generic utility functions, such as date parsing."""

import openpyxl
from datetime import datetime, timedelta
from json import load

def get_session_classification(hour: int) -> str:
    """
    A function that classifies the session based on the hour provided.

    Args:
        hour (int): The hour to be classified.

    Returns:
        str: The session classification which can be "Breakfast", "Lunch", or "Dinner".
    """
    if hour > 4 and hour < 11:
        return "Breakfast"
    elif hour < 16:
        return "Lunch"
    else:
        return "Dinner"
    
def diff_days(date1: datetime, offset: int) -> datetime:
    return date1 - timedelta(days=offset)

def add_days(date1: datetime, offset:int) -> datetime:
    return date1 + timedelta(days=offset)
    
days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
def get_report_filename(date: datetime, restaruant_name: str, root:str) -> str:
    """
    Generates a filename string based on the week of the provided date.

    Parameters:
        date (datetime): The input date to determine the week period.

    Returns:
        str: The filename string formatted as 'start_day_to_end_day_Report.xlsx'.
    """
    # prev_date = diff_days(date, 1)
    prev_date = date

    day = prev_date.weekday()

    start_day = diff_days(prev_date, day)
    end_day = add_days(prev_date, 6 - day)

    filename = f"{root}/documents/Generated_Reports/{restaruant_name.replace(' ', '_')}/{date.strftime('%Y')}/{start_day.strftime('%d_%b')}_to_{end_day.strftime('%d_%b')}_Report.xlsx"
    return filename


def parse_json_file(file_path: str) -> dict:
    """
    Parses a JSON file and returns a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The parsed JSON data.
    """
    with open(file_path, 'r') as f:
        return load(f)
    
exch_rate = {
    "BBD": 1,
    "USD": 1.98
}

def get_exch_rate(key: str) -> float:
    return exch_rate.get(key, 1.0)