"""This module will contain generic utility functions, such as date parsing."""

def get_session_classification(hour: int) -> str:
    if hour > 4 and hour < 11:
        return "Breakfast"
    elif hour < 16:
        return "Lunch"
    else:
        return "Dinner"
