"""This will be the driver used to create the comp summary report for each restaurant."""
from datetime import datetime

from utils import *

class CompSummaryGenerator:
    def __init__(self, root: str=".."):
        self.root = root
        pass

    def generate_comp_summary(self, restaurant_key: str, date: datetime) -> str:
        filepath = ""

        # Get the restaurnt name
        name_obj: RestaurantNames = RestaurantNames.get_restaurant_by_key(restaurant_key)
        name = '_'.join(name_obj.value[0].split(" "))
        abr = name_obj.value[1]

        # Get the filepath of the report
        report_filepath = generic.get_report_filename(date, name, abr, self.root)
        
        # Pull the summary from the lunch summary.
        format = generic.parse_json_file(f"{self.root}/scripts/Report_Format.json")
        target = format["LDSP"]
        excel_controller = ExcelController(report_filepath, True)

        excel_controller.change_sheet(target["SHEET"])

        for i in range(int(target["START"]), int(target["END"])+1):
            data = excel_controller.read_from_cell(f"{target['TOTALS']}{i}")
            print(f"{target['TOTALS']}{i}: {data}")

        # Create or open restaurnt_name_comp_summary.xlsx

        # Insert column containing data from the summary

        # Save and close the file.

        # Return filepath

        return filepath
    
if __name__ == "__main__":
    generator = CompSummaryGenerator()
    generator.generate_comp_summary("BISTRO", datetime(2024, 5, 16))