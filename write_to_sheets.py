from authorize_google import GoogleSheets
from type_annotations import Categories, CategorySummary
from authorize_google import ColumnProperty
import json

SPREADSHEET_ID = "1CQqQ7XW-LuDEVAJ-NZkK6blGTefX8vmtL9Do6hXGg-w"
HEADER_CATEGORY='Category'
HEADER_AMOUNT='Amount'
HEADER_DESCRIPTION='Description'
TOTAL='Total'
SUM_FORMULA='=SUM(INDIRECT(ADDRESS(1,COLUMN())&":"&ADDRESS(ROW()-1,COLUMN())))'

SUMMARY_SHEET_COLUMN_PROPERTIES = [
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

    table_values: list[list[str | float]] = [
        [HEADER_CATEGORY, HEADER_AMOUNT]
    ]

    for categoryName in data:
        table_values.append([
            categoryName,
            data[categoryName]['total']
        ])
    
    for i in range(4):
        table_values.append([])
    table_values.append(["Total Spend", "=SUM(B2:B7)"] )
    

    # sheetsService.create_new_sheet(SPREADSHEET_ID, "Summary")
    # sheetsService.writeToSheet(SPREADSHEET_ID, "Summary", table_values)
    # sheetsService.add_table(SPREADSHEET_ID, "")

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
        sheetsService.auto_resize_columns(SPREADSHEET_ID, sheet_id, len(CATEGORY_SHEET_COLUMN_PROPERTIES))



    
