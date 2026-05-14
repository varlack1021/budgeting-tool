from get_and_process_data import getAndProcessData
from write_to_sheets import writeToSheets

# TO DO
# handle writing when sheets exist
# handle negative numbers
# handle creating a spreadsheet when none exists
def main():
    data = getAndProcessData()
    writeToSheets(data)

main()