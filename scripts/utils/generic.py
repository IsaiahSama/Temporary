"""This module will contain generic utility functions, such as date parsing."""

def get_session_classification(hour: int) -> str:
    """
    A function that classifies the session based on the hour provided.

    Args:
        hour (int): The hour to be classified.

    Returns:
        str: The session classification which can be "Breakfast", "Lunch", or "Dinner".
    """
    if hour > 4 and hour < 11:
        return "Breakfast"
    elif hour < 16:
        return "Lunch"
    else:
        return "Dinner"
