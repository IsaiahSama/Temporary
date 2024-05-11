"""This module will contain the necessary Enums used for typehinting"""
from enum import Enum 


class RestaurantNames(Enum):
    """
    An enum for the names of the 4AM restaurants, along with their corresponding abbreviations.

    Example: TIDES = ('Tides', 'TPS')
    """

    TIDES = ("Tides", "TPS")
    BISTRO = ("QP Bistro", "QPB")
    CLIFF = ("The Cliff", "QPC")
    CAFE = ("Cafe de Paris", "CDP")

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
    PAYMENT_TYPE = "Type"
    AMOUNT = "Amt"
    CURRENCY = "Curr."
    EXCHANGE = "Exch"
    GROSS = "Order Gross"
