"""This module will act as a wrapper for the ReportGenerator class."""
from scripts.generate_reports import *

class GeneratorController:
    def __init__(self) -> None:
        self.generator : ReportGenerator | None = None 

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
        self.generator.generate_daily_report()

if __name__ == "__main__":
    controller = GeneratorController()
    controller.set_generator("BISTRO", "05/09/2024")
    controller.generate_report()