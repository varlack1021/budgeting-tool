import warnings
warnings.filterwarnings("ignore", message=".*Python version 3.9.*")
warnings.filterwarnings("ignore", message=".*non-supported Python version.*")
from get_and_process_data import getAndProcessData
from write_to_sheets import writeToSheets
from google_sheets_service import GoogleSheets
from google_drive_service import GoogleDrive
from datetime import datetime
import argparse
import calendar

def get_spread_sheet_id(driveService, month):
    now = datetime.now()
    year = now.year
    month = month

    folder_id = driveService.find_folder_by_name(year)
    file_id = driveService.find_file_by_name(month, folder_id)
    return file_id

def get_command_line_args():
    parser = argparse.ArgumentParser(description="Get the month name from its number (1-12)")
    parser.add_argument("month", nargs="?", default=None, type=int, help="Month number (1-12)")
    args = parser.parse_args()

    if args.month is None:
        parser.error("No month provided. Please enter a number between 1 and 12.")
    
    if not 1 <= args.month <= 12:
        parser.error(f"Invalid month: {args.month}. Please enter a number between 1 and 12.")
    return args

def main():
    args = get_command_line_args()
    sheetsService = GoogleSheets()
    driveService = GoogleDrive()    
                     
    data = getAndProcessData()

    file_id = get_spread_sheet_id(driveService, calendar.month_name[args.month])
    
    writeToSheets(sheetsService, data, file_id)
    print("Done")
main()