"""This module will contain the necessary Enums used for typehinting"""
from enum import Enum 


class RestaurantNames(Enum):
    """Enum mapping restaurant keys, to their names and abbreviations.
    
    Example: TIDES = ('Tides', 'TPS')
    
    Attributes:
        TIDES

        BISTRO

        CLIFF
        
        CAFE
    """

    TIDES = ("Tides", "TPS")
    BISTRO = ("QP Bistro", "QPB")
    CLIFF = ("The Cliff", "QPC")
    CAFE = ("Cafe de Paris", "CDP")