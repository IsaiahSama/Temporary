"""File to hold custom errors""" 

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