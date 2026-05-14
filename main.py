import warnings
from pprint import pprint
warnings.filterwarnings("ignore", message=".*Python version 3.9.*")
warnings.filterwarnings("ignore", message=".*non-supported Python version.*")
from get_and_process_data import getAndProcessData
from write_to_sheets import writeToSheets

# TO DO
# handle negative numbers
# handle creating a spreadsheet when none exists
def main():
    data = getAndProcessData()
    writeToSheets(data)

main()