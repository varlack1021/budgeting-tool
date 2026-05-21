import warnings
warnings.filterwarnings("ignore", message=".*Python version 3.9.*")
warnings.filterwarnings("ignore", message=".*non-supported Python version.*")
from get_and_process_data import getAndProcessData
from write_to_sheets import writeToSheets
from google_sheets_service import GoogleSheets
from google_drive_service import GoogleDrive
# TO DO
# handle creating a spreadsheet when none exists
# auto get date range
def main():
    sheetsService = GoogleSheets()
    driveService = GoogleDrive()

    data = getAndProcessData()
    folder_id = driveService.find_folder_by_name("2026")
    file_id = driveService.find_file_by_name("May", folder_id)
    
    writeToSheets(sheetsService, data, file_id)
    print("Done")
main()