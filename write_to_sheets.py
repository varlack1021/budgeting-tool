from google_sheets_service import GoogleSheets, SheetExistsError
from type_annotations import CategorySummary
from google_sheets_service import ColumnProperty

SPREADSHEET_ID = "1CQqQ7XW-LuDEVAJ-NZkK6blGTefX8vmtL9Do6hXGg-w"
TOTAL='Total'
SUM_FORMULA='=SUM(INDIRECT(ADDRESS(1,COLUMN())&":"&ADDRESS(ROW()-1,COLUMN())))'

SUMMARY_SHEET_COLUMN_PROPERTIES:list[ColumnProperty] = [
{
                        "columnName": "Category",
                        "columnIndex": 0 
                    },
                    {
                        "columnName": "Amount",
                        "columnIndex": 1 
                    },
    
                ]

CATEGORY_SHEET_COLUMN_PROPERTIES: list[ColumnProperty] = [
                    {
                        "columnName": "Description",
                        "columnIndex": 0
                    },
                    {
                        "columnName": "Date",
                        "columnIndex": 1
                    },
                    {
                        "columnName": "Amount",
                        "columnIndex": 2
                    },
    
                ]

def create_formatted_sheet(sheetsService: GoogleSheets, column_properties, sheet_name, col_width):
    try:
        sheet_id=sheetsService.create_new_sheet(SPREADSHEET_ID, sheet_name)
        sheetsService.add_table(SPREADSHEET_ID, sheet_id, column_properties, sheet_name)
        sheetsService.adjust_column_width(SPREADSHEET_ID, sheet_id, 0, col_width)
    except SheetExistsError:
        pass


def writeToSheets(data:dict[str, CategorySummary]):
    sheetsService = GoogleSheets()
    summary_table_values: list[list[str | float]] = []

    for categoryName in data:
        summary_table_values.append([
            categoryName,
            f"""=QUERY({categoryName}!A:C, "SELECT SUM(C) WHERE A != 'Total' LABEL SUM(C) ''")"""
        ])
    
    for i in range(2):
        summary_table_values.append([])
    summary_table_values.append(["Total Spend", "=SUM(B2:B7)"])
    
    # do this first to ensure the sheet is placed first in the sheet order
    create_formatted_sheet(sheetsService, SUMMARY_SHEET_COLUMN_PROPERTIES, "Summary", 150)

    for categoryName, summary in data.items():
        table_values = [] 
        
        for transaction in summary['transactions']:
            amount = transaction['amount']
            date = transaction['date']
            description = transaction['description']
            table_values.append([description, date.isoformat(), amount])
        table_values.append([])
        table_values.append([TOTAL, "",SUM_FORMULA])
        
        create_formatted_sheet(sheetsService, CATEGORY_SHEET_COLUMN_PROPERTIES, categoryName, 250)
        sheetsService.writeToSheet(SPREADSHEET_ID, categoryName, table_values)

    # Do this last. Otherwise the REF's in the query will be null as they don't exist until all other sheets are created.
    print(summary_table_values)
    sheetsService.writeToSheet(SPREADSHEET_ID, "Summary", summary_table_values)

    
