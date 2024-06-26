import os

folders = [
    "documents",
    "documents/Summaries",
    "documents/Generated_Reports",
    "documents/Generated_Reports/Cafe_de_Paris",
    "documents/Generated_Reports/Cafe_de_Paris/2024",
    "documents/Generated_Reports/QP_Bistro",
    "documents/Generated_Reports/QP_Bistro/2024",
    "documents/Generated_Reports/Tides",
    "documents/Generated_Reports/Tides/2024",
    "documents/Generated_Reports/The_Cliff",
    "documents/Generated_Reports/The_Cliff/2024",
    "documents/Upload",
    "documents/Upload/Cafe_de_Paris",
    "documents/Upload/QP_Bistro",
    "documents/Upload/Tides",
    "documents/Upload/The_Cliff",
    "documents/Logs/",
    "scripts",
    "scripts/Report_Templates",
]

def create_folder_structure():
    """
    Creates a folder structure based on the list of folders provided.

    This function iterates over each folder in the `folders` list and checks if it exists in the current directory. If a folder does not exist, it creates the folder using the `os.makedirs()` function.

    Parameters:
        None

    Returns:
        None
    """
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

if __name__ == "__main__":
    create_folder_structure()