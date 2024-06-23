"""This module will act as a wrapper for the ReportGenerator class."""
from tempfile import SpooledTemporaryFile
from os.path import exists
from scripts.generate_reports import *
from create_folder_structure import create_folder_structure
from datetime import timedelta
from sys import argv

class GeneratorController:
    def __init__(self) -> None:
        self.generator : ReportGenerator | None = None 

        if not exists("./documents"):
            create_folder_structure()

    def set_generator(self, restaurant_key: str, date_str: str):
        """
        Sets the generator for the current instance of GeneratorController.

        Args:
            restaurant_key (str): The key of the restaurant for which the generator is being set.
            date_str (str): The date for which the generator is being set, in the format "MM/DD/YYYY".

        Returns:
            None
        """

        restaruant_name: RestaurantNames = RestaurantNames.get_restaurant_by_key(restaurant_key)

        # Date should be in format "MM/DD/YYYY"
        date = datetime.strptime(date_str, "%m/%d/%Y")
        self.generator = ReportGenerator(restaruant_name, date, ".")

    def generate_report(self):
        """
        Generates a daily report using the generator instance stored in the current instance of GeneratorController.

        Returns:
            str: The path to the generated workbook.
        """
        return self.generator.generate_daily_report()

    def upload_file(self, file: SpooledTemporaryFile, filemode: str ):
        """
        Uploads a file to the specified file mode.

        Parameters:
            file (SpooledTemporaryFile): The file to be uploaded.
            filemode (str): The mode of the file. Must be either "Sales" or "Payments".

        Raises:
            ValueError: If the file mode is not "Sales" or "Payments".

        Returns:
            None
        """
        if filemode not in ["Sales", "Payments"]:
            Logger.error(f"File mode must be either 'Sales' or 'Payments'.")
            raise ValueError("File mode must be either 'Sales' or 'Payments'.")
        
        with open(f"./documents/Upload/{self.generator.restaurant_name.replace(' ', '_')}/{self.generator.restaurant_abrv}-{filemode}-{self.generator.date.strftime('%Y%m%d')}.csv", "wb") as f:
            f.write(file.read())

FOLDERS = ["QP_Bistro", "The_Cliff", "Tides", "Cafe_De_Paris"]
folders = ["BISTRO", "CLIFF", "TIDES", "CAFE"]

def test():
    """Used for testing"""

    start_date = datetime(2024, 5, 13)
    t_date = start_date
    end_date = datetime(2024, 5, 20)

    controller = GeneratorController()
    print("Working for", t_date.strftime("%m/%d/%Y"))
    while t_date <= end_date:
        for folder in folders:
            controller.set_generator(folder, t_date.strftime("%m/%d/%Y"))
            try:
                controller.generate_report()
            except CustomExceptions.BadlyFormattedCSVException as e:
                print(e)
            except Exception as e:
                print(e)
        t_date += timedelta(days=1)

def run_for_date(date: datetime):
    controller = GeneratorController()

    today = date

    for folder in folders:
        controller.set_generator(folder, today.strftime("%m/%d/%Y"))
        try:
            controller.generate_report()
        except Exception as e:
            Logger.error(e)
            print(e)

def run_for_today():
    today = datetime.now()

    run_for_date(today)

if __name__ == "__main__":
    if len(argv) > 1:
        date_str = argv[-1] # dd/mm/yyyy
        date = datetime.strptime(date_str, "%d/%m/%Y")
        run_for_date(date)
    else:
        run_for_today()