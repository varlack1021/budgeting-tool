from google_sheets_service import GoogleSheets
from type_annotations import Categories, CategorySummary
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

def writeToSheets(data:dict[Categories, CategorySummary]):
    sheetsService = GoogleSheets()
    # spreadsheet = sheetsService.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()

    table_values: list[list[str | float]] = []

    for categoryName in data:
        table_values.append([
            categoryName,
            f"""=QUERY({categoryName}!A:C, "SELECT SUM(C) WHERE A != 'Total' LABEL SUM(C) ''")"""
        ])
    
    for i in range(2):
        table_values.append([])
    table_values.append(["Total Spend", "=SUM(B2:B7)"])
    

    sheet_id=sheetsService.create_new_sheet(SPREADSHEET_ID, "Summary")
    sheetsService.add_table(SPREADSHEET_ID, sheet_id, SUMMARY_SHEET_COLUMN_PROPERTIES, "Summary")
    sheetsService.adjust_column_width(SPREADSHEET_ID, sheet_id, 0, 150)

    for categoryName, summary in data.items():
        table_values = [] 
        
        for transaction in summary['transactions']:
            amount = transaction['amount']
            date = transaction['date']
            description = transaction['description']
            table_values.append([description, date.isoformat(), amount])
        table_values.append([])
        table_values.append([TOTAL, "",SUM_FORMULA])
        
        sheet_id = sheetsService.create_new_sheet(SPREADSHEET_ID, categoryName)
        sheetsService.add_table(SPREADSHEET_ID, sheet_id, CATEGORY_SHEET_COLUMN_PROPERTIES, categoryName)
        sheetsService.writeToSheet(SPREADSHEET_ID, categoryName, table_values)
        sheetsService.adjust_column_width(SPREADSHEET_ID, sheet_id, 0, 250)

    # Do this last. Otherwise the REF's in the query will be null as they don't exist until all other sheets are created.
    sheetsService.writeToSheet(SPREADSHEET_ID, "Summary", table_values)

    
