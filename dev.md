# 4AM Automated Reporting (Dev Version)

This document serves as my core area for notes, and information relating to the structure and functionality of the application.

# ToDo
1. Setup Folder Structure
2. Setup Email File Extraction
3. Develop scripts to generate Reports
4. Create web interface for uploading and downloading reports.
5. Test and Verify Generated Reporting Data
6. Create a database to store generated data.
7. Develop script to load data into QuickBooks
8. Test and Verify data loaded in QuickBooks
9. Document Everything

## Task Breakdown
This section will breakdown the above 8 tasks into their core components and deliverables.

### Setup Folder Structure
For now, the tentative folder structure is as follows:

Root
├── controller.py
├── documents
│   ├── Generated_Reports
│   │   ├── Cafe de Paris
│   │   │   └── 2024
│   │   ├── QP Bistro
│   │   │   └── 2024
│   │   │       └── January
│   │   │           └── 31st_Feb_to_6th_Jan_Report.xlsx
│   │   ├── Tides
│   │   │   └── 2024
│   │   └── The Cliff
│   │       └── 2024
│   └── Upload
│       ├── Cafe de Paris
│       │   ├── DD_MM_YYYY_Sales.csv
│       │   └── DD_MM_YYYY_Payments.csv
│       ├── QP Bistro
│       ├── Tides
│       └── The Cliff    
└── scripts
    └── Report Templates
        ├── CafeDeParis_Sales_Report_Template.xlsx
        ├── Cliff_Sales_Report_Template.xlsx
        ├── QPBistro_Sales_Report_Template.xlsx
        └── Tides_Sales_Report_Template.xlsx


### Setup Email File Extraction
A script should be created to do the following:
- Be registered to a specific email address
- Locate email containing most recent reports
- Download the attached excel files
- Place the files into their correct folders, doing any renaming as necessary.

### Develop Scripts to Generate Reports
Upon retriveing the Sales and Billing reports from the emails, and them being placed in their correct folder, the script should then do the following:

1. For each company, read the data from the latest Sales and Billing excel spreadsheets.
2. Run calculations and store the following information:
    - Total US and BBD spent by Payment Type (Visa, Master, Prepaid, Cash, etc)
    - Total US and BBD spent by Payment Type by Meal Type (Breakfast, Lunch, Dinner).
    - Total BBD spent by sub-category by Meal Type (non-alcoholic, wine, water, food, etc) by Breakfast, Lunch and Dinner
    - The number of guests by Meal Type (Breakfast, Lunch, Dinner)
    - Service Charge, VAT, Government Levy, Deposit
3. This stored information should then be written to a spreadsheet following the restaurant's respective Report Template.
4. Store data in a database designed for easy querying.
5. Create the rolling 8 week report.
6. Export the data to their QuickBook Format.

### Create Web Interface
The web interface should be a simple website designed to do the following:
- Allow users to manually upload Sales and Payments files for a restaurant.
- Download the generated reports.
- View and Filter all generated Reports.
- When database is designed, view the 8 week running total.

### Test and Verify Generated Reporting Data
This will involve sending the generated data back to the company for review and comparison with a previously manually tabulated one to ensure data accuracy and integrity.

Any necessary Revisions will then take place in this phase.

### Create Database
At this point, a database will be created designed to store a copy of the information placed within each Generated Report File. This is to provide easy access without having to reopen each file, when performing calculations like the 8 week running total.

The database will be structured as follows:

#### Tables
- QP Bistro
- Cafe De Paris
- Tides
- The Cliff

#### Columns
- ID
- Restaurant
- Date
- Total_Amount
- Amount_Spent_By_Visa
- Amount_Spent_By_Master
- Amount_Spent_By_Prepaid
- Amount_Spent_By_Cash
- Amount_Spent_By_Other
- Total_Amount_Spent_By_Meal_Type (Breakfast, Lunch, Dinner)
- Amount_Spent_By_Breakfast
- Amount_Spent_By_Lunch
- Amount_Spent_By_Dinner
- Total_Number_Of_Guests
- Number_Of_Breakfast_Guests
- Number_Of_Lunch_Guests
- Number_Of_Dinner_Guests
- Total_Amount_Spent_By_Sub_Meal_Type
- Amount_Spent_By_Non_Alcoholic_At_Breakfast
- Amount_Spent_By_Non_Alcoholic_At_Lunch
- Amount_Spent_By_Non_Alcoholic_At_Dinner
- Amount_Spent_By_Wine_At_Breakfast
- Amount_Spent_By_Wine_At_Lunch
- Amount_Spent_By_Wine_At_Dinner
- Amount_Spent_By_Water_At_Breakfast
- Amount_Spent_By_Water_At_Lunch
- Amount_Spent_By_Water_At_Dinner
- Amount_Spent_By_Food_At_Breakfast
- Amount_Spent_By_Food_At_Lunch
- Amount_Spent_By_Food_At_Dinner
- Total_Service_Charge
- Total_VAT_Cost
- Total_Government_Levy
- Total_Deposit

### Develop QuickBooks Script
This script will be responsible for loading the generated report data into QuickBooks by Account Number.

More Information Pending

### Test and Verify Data Loaded in Quickbooks
More Information Pending

### Document Everything.

DOCUMENT IT ALL!