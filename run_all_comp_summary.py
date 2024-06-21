from datetime import datetime, timedelta
from scripts.generate_comp import CompSummaryGenerator
from os import listdir

report_base = "./documents/Generated_Reports/"
FOLDERS = ["QP_Bistro", "The_Cliff", "Tides", "Cafe_De_Paris"]
keys = ["BISTRO", "CLIFF", "TIDES", "CAFE"]
year = "2024"

results = {
    "BISTRO": [],
    "CLIFF": [],
    "TIDES": [],
    "CAFE": []
}

generator = CompSummaryGenerator(".")

for i, folder in enumerate(FOLDERS):
    filepath = f"{report_base}{folder}/{year}/"
    reports = listdir(filepath)

    dates = ['_'.join(report.split("_")[1:3])+f"_{year}" for report in reports]

    start_dates = [datetime.strptime(date, "%d_%b_%Y") for date in dates]

    results[keys[i]] = start_dates

for key, datetimes in results.items():
    for date in sorted(datetimes):
        try:
            date += timedelta(days=1)
            generator.generate_comp_summary(key, date)
        except Exception as e:
            print(e)