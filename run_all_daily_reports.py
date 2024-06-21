import daily_gen
from os import listdir, path
from datetime import datetime

uploads = "./documents/Upload/"

FOLDERS = ["QP_Bistro", "The_Cliff", "Tides", "Cafe_De_Paris"]

for i, folder in enumerate(FOLDERS):
    files = [file for file in listdir(uploads + folder) if "Payments" in file]
    for file in files:
        key = file.split("-")[0]
        date_str = file.split("-")[-1].split(".")[0]

        if not path.exists(f"{uploads}{folder}/{key}-Sales-{date_str}.csv"):
            continue

        date_obj = datetime.strptime(date_str, "%Y%m%d")
        parsed_date_str = date_obj.strftime("%m/%d/%Y")

        controller = daily_gen.GeneratorController()
        controller.set_generator(daily_gen.folders[i], parsed_date_str)
        try:
            controller.generate_report()
        except daily_gen.CustomExceptions.BadlyFormattedCSVException as e:
            print(e)
        except Exception as e:
            print(e)
