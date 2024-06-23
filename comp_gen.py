"""This code will be responsible for creating a comp summary report."""

from datetime import datetime, timedelta
from scripts.generate_comp import CompSummaryGenerator
from scripts.utils import Logger

last_week = datetime.now() - timedelta(days = 2)

generator = CompSummaryGenerator(root=".")

restaurants = ["CAFE", "CLIFF", "TIDES", "BISTRO"]

for restaurant in restaurants:
    try:
        generator.generate_comp_summary(restaurant, last_week)
    except Exception as e:
        Logger.error(e)
        print(e)