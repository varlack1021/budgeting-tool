from get_and_process_data import getAndProcessData
from write_to_sheets import writeToSheets

def main():
    data = getAndProcessData()
    writeToSheets(data)

main()