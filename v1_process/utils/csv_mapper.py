from v1_process.models import GrossUp
from v1_process.dictionaries.dictionary import *
from os import makedirs, path


def map_gross_up_to_csv(gross_up_list: list[GrossUp], company_nit: str, payroll_date: str) -> str:
    file_name = f"{OUTPUT_FILE_GENERAL_NAME}-{company_nit}-{payroll_date}.csv"
    file_path = OUTPUT_FOLDER_PATH + file_name

    if not path.exists(OUTPUT_FOLDER_PATH):
        makedirs(OUTPUT_FOLDER_PATH)

    with open(file_path, "w") as file:
        file.write(f"{DOCUMENT},{FINAL_GROSS_UP_VALUE}\n")
        for gross_up_object in gross_up_list:
            file.write(f'{gross_up_object.document},{gross_up_object.gross_up}\n')

    return file_name


def map_output_csv_to_return_data(file_name) -> str:
    file_path = OUTPUT_FOLDER_PATH + file_name
    try:
        with open(file_path, "r") as file:
            file_data = file.read()
        return file_data

    except IOError:
        print("file not exist")
