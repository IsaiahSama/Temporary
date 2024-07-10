"""File to hold custom exceptions""" 

class InvalidRestaurantNameException(Exception):
    """Raised when the restaurant name is invalid"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
    
class InvalidReportFormatException(Exception):
    """Raised when the report format contains an invalid value"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
    
class BadlyFormattedCSVException(Exception):
    """Raised when the report is badly formatted."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class UnknownCardTypeException(Exception):
    """Raised when the card type is unknown, or does not match what's defined in Report_Format.json."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)