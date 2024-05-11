import os

folders = [
    "documents",
    "documents/Generated_Reports",
    "documents/Generated_Reports/Cafe de Paris",
    "documents/Generated_Reports/Cafe de Paris/2024",
    "documents/Generated_Reports/QP Bistro",
    "documents/Generated_Reports/QP Bistro/2024",
    "documents/Generated_Reports/Tides",
    "documents/Generated_Reports/Tides/2024",
    "documents/Generated_Reports/The Cliff",
    "documents/Generated_Reports/The Cliff/2024",
    "documents/Upload",
    "documents/Upload/Cafe de Paris",
    "documents/Upload/QP Bistro",
    "documents/Upload/Tides",
    "documents/Upload/The Cliff",
    "scripts",
    "scripts/Report Templates",
    "scripts/Report Templates/CafeDeParis_Sales_Report_Template.xlsx",
    "scripts/Report Templates/Cliff_Sales_Report_Template.xlsx",
    "scripts/Report Templates/QPBistro_Sales_Report_Template.xlsx",
    "scripts/Report Templates/Tides_Sales_Report_Template.xlsx"
]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
