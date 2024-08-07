"""This will be the driver used to create the comp summary report for each restaurant."""
from datetime import datetime
from os.path import exists
try:
    from utils import *
except ModuleNotFoundError:
    from .utils import *

class CompSummaryGenerator:
    def __init__(self, root: str=".."):
        self.root = root

    def generate_comp_summary(self, restaurant_key: str, date: datetime) -> str:
        Logger.log(f"Generating comp summary for {restaurant_key} for week including {date.strftime('%m/%d/%Y')} ")
        # Get the restaurnt name
        name_obj: RestaurantNames = RestaurantNames.get_restaurant_by_key(restaurant_key)
        name = '_'.join(name_obj.value[0].split(" "))
        abr = name_obj.value[1]

        # Get the filepath of the report
        report_filepath = generic.get_report_filename(date, name, abr, self.root)
        
        # Pull the summary from the lunch summary.
        format = generic.parse_json_file(f"{self.root}/scripts/Report_Format.json")
        lunch_format = format["LDSP"]
        summary_format = format["COMP_SUMMARY"]
        report_controller = ExcelController(report_filepath, True)

        report_controller.change_sheet(lunch_format["SHEET"])

        entries = []
        for i in range(lunch_format["START"], lunch_format["END"] + 1):
            data = report_controller.read_from_cell(f"{lunch_format['TOTALS']}{i}")
            title = report_controller.read_from_cell(f"A{i}")
            entries.append(data)

        for i in range(lunch_format["SUMMARY_START"], lunch_format["SUMMARY_END"] + 1):
            try:
                data = round(report_controller.read_from_cell(f"{lunch_format['SUMMARY']}{i}"), 2)
            except:
                data = report_controller.read_from_cell(f"{lunch_format['SUMMARY']}{i}")
            title = report_controller.read_from_cell(f"A{i}")
            entries.append(data)

        # Create or open restaurnt_name_comp_summary.xlsx
        template_file_path = f"{self.root}/scripts/Report_Templates/Summaries/{abr}_Comp_Summary_Template.xlsx"
        summary_file_path = f"{self.root}/documents/Summaries/{abr}_Comp_Summary.xlsx"
        
        if exists(summary_file_path):
            summary_controller = ExcelController(summary_file_path)
            Logger.log("Inserting into existing summary at {summary_file_path}")
        else:
            summary_controller = ExcelController(template_file_path)
            Logger.log(f"Creating new summary at {summary_file_path}")
        summary_controller.change_sheet(summary_format["SHEET"])

        # Insert column containing data from the summary
        _, end_day = generic.get_week_period(generic.diff_days(date, 1))
        header = f"WE {end_day.strftime('%b-%d')}"

        check_start = "B"
        col = None

        # Checks if the data was entered before. If so, will use that column and overwrite it.
        for i in range(0, 10):
            value = summary_controller.read_from_cell(f"{check_start}5")
            if value != header:
                check_start = f"{chr(ord(check_start) + 1)}"
            else:
                col = check_start
                break
        
        if not col:
            summary_controller.insert_col(2)
            col = summary_format["COL"]
        start = summary_format["START"]

        summary_controller.insert_data_into_cell(header, f"{col}{summary_format['WEEK']}")

        # Calculating bar only covers (Alcohol, Non-Alcohol, Water)
        
        bars = (17, 18, 19)
        for i, entry in enumerate(entries):
            field = summary_controller.read_from_cell(f"A{start}")
            if start > 14:
                summary_controller.make_cell_accounting(f"{col}{start}")
            summary_controller.copy_cell_style_to(f"A{start}", f"{col}{start}")

            if i in bars:
                summary_controller.insert_data_into_cell((summary_controller.read_from_cell(f"{col}{start}") if i != bars[0] else 0) + entry, f"{col}{start}")
                if i == bars[-1]:
                    start += 1
            else:
                summary_controller.insert_data_into_cell(entry, f"{col}{start}")
                start += 1

        # Save and close the file.
        summary_controller.save(summary_file_path)

        # Return filepath
        Logger.log(f"Summary generated and stored in {summary_file_path}")
        print("Summary generated and stored in " + summary_file_path)
        return summary_file_path
    
if __name__ == "__main__":
    generator = CompSummaryGenerator()
    generator.generate_comp_summary("BISTRO", datetime(2024, 5, 31))