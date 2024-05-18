"""This module will act as a wrapper for the ReportGenerator class."""
from tempfile import SpooledTemporaryFile
from os.path import exists
from scripts.generate_reports import *
from create_folder_structure import create_folder_structure

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
        return self.generator.generate_daily_report()

    def upload_file(self, file: SpooledTemporaryFile, filemode: str ):
        if filemode not in ["Sales", "Payments"]:
            raise ValueError("File mode must be either 'Sales' or 'Payments'.")
        
        with open(f"./documents/Upload/{self.generator.restaurant_name.replace(' ', '_')}/{self.generator.restaurant_abrv}-{filemode}-{self.generator.date.strftime('%Y%m%d')}.csv", "wb") as f:
            f.write(file.read())

if __name__ == "__main__":
    controller = GeneratorController()
    controller.set_generator("BISTRO", "05/14/2024")
    controller.generate_report()