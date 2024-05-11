import os

folders = [
    "documents",
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
    "scripts",
    "scripts/Report_Templates",
]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
