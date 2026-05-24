import warnings
warnings.filterwarnings("ignore", message=".*Python version 3.9.*")
warnings.filterwarnings("ignore", message=".*non-supported Python version.*")
from get_and_process_data import getAndProcessData
from write_to_sheets import writeToSheets
from google_sheets_service import GoogleSheets
from google_drive_service import GoogleDrive
from datetime import datetime

def get_spread_sheet_id(driveService):
    now = datetime.now()
    year = now.year
    month = now.strftime("%B")

    folder_id = driveService.find_folder_by_name(year)
    file_id = driveService.find_file_by_name(month, folder_id)
    return file_id

def main():
    sheetsService = GoogleSheets()
    driveService = GoogleDrive()    
                     
    data = getAndProcessData()

    file_id = get_spread_sheet_id(driveService)
    
    writeToSheets(sheetsService, data, file_id)
    print("Done")
main()