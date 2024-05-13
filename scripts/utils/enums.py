"""This module will contain the necessary Enums used for typehinting"""
from enum import Enum 
from .errors import InvalidRestaurantNameException

class RestaurantNames(Enum):
    """
    An enum for the names of the 4AM restaurants, along with their corresponding abbreviations.

    Example: TIDES = ('Tides', 'TPS')
    """

    TIDES = ("Tides", "TPS")
    BISTRO = ("QP Bistro", "QPB")
    CLIFF = ("Cliff", "QPC")
    CAFE = ("Cafe de Paris", "CDP")

    @staticmethod
    def get_restaurant_by_name(name: str):
        restaurant = None 

        for _, value in RestaurantNames.__members__.items():
            if value.value[0] == name:
                restaurant = value
                break

        if restaurant is None:
            raise InvalidRestaurantNameException(f"Found no restaurant with name: {name}")

        return restaurant

    @staticmethod
    def get_restaurant_by_key(key: str):
        try:
            return RestaurantNames[key]
        except KeyError:
            raise InvalidRestaurantNameException(f"Found no restaurant with Key: {key}")


class SalesColumnNames(Enum):
    """
    An enum for the column names used in the Sales spreadsheet.

    This enum is used to ensure that the correct column names are used when generating reports.
    """

    ID = "Order ID"
    DATE = "Date"
    SESSION = "Session"
    CATEGORY = "Category"
    GUESTS = "Guests"
    AMOUNT = "Sale Net"
    LEVY = "Levy"
    VAT = "Vat"

class PaymentColumnNames(Enum):
    """
    An enum for the column names used in the Payment spreadsheet.

    This enum is used to ensure that the correct column names are used when generating reports.
    """
    
    ID = "Order ID"
    STORE = "Store"
    DATE = "Order Approved"
    PAYMENT_TYPE = "Type"
    AMOUNT = "Amt"
    CURRENCY = "Curr."
    EXCHANGE = "Exch"
    GROSS = "Order Gross"
    SESSION = "Session"