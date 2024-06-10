"""This code will be responsible for creating a comp summary report."""

from datetime import datetime, timedelta
from scripts.generate_comp import CompSummaryGenerator

last_week = datetime.now() - timedelta(days = 2)

generator = CompSummaryGenerator()

restaurants = ["CAFE", "CLIFF", "TIDES", "BISTRO"]

for restaurant in restaurants:
    generator.generate_comp_summary(restaurant, last_week)