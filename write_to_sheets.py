from google_sheets_service import GoogleSheets, SheetExistsError
from google_sheets_service import ColumnProperty
from type_annotations import Transaction, Categories

TOTAL='Total'
SUM_FORMULA='=SUM(INDIRECT(ADDRESS(1,COLUMN())&":"&ADDRESS(ROW()-1,COLUMN())))'

SUMMARY_SHEET_COLUMN_PROPERTIES:list[ColumnProperty] = [
{
                        "columnName": "Category",
                        "columnIndex": 0 
                    },
                    {
                        "columnName": "Spent",
                        "columnIndex": 1 
                    },
                    {
                        "columnName": "Budgeted",
                        "columnIndex": 2 
                    },
                                        {
                        "columnName": "Remaining",
                        "columnIndex": 3 
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

CATEGORY_BUDGETS: dict[str, int] = {
    Categories.Comics: 100,
    Categories.Groceries: 800,
    Categories.GuiltFree: 1408,
    Categories.Insurance: 230,
    Categories.Phone: 103,
    Categories.Miscellaneous: 665,
    Categories.Subscriptions: 150,
    Categories.Transportation: 200
}

def create_formatted_sheet(sheetsService: GoogleSheets, spread_sheet_id: str, column_properties, sheet_name, col_width, index):
    try:
        sheet_id=sheetsService.create_new_sheet(spread_sheet_id, sheet_name, index)
        sheetsService.add_table(spread_sheet_id, sheet_id, column_properties, sheet_name)
        sheetsService.adjust_column_width(spread_sheet_id, sheet_id, 0, col_width)
    except SheetExistsError:
        sheetsService.clearSheets(spread_sheet_id, [sheet_name])
        pass


def writeToSheets(sheetsService: GoogleSheets, data:dict[str, list[Transaction]], spread_sheet_id):
    summary_table_values: list[list[str | float]] = []
    
    # do this first to ensure the sheet is placed first in the sheet order
    create_formatted_sheet(sheetsService, spread_sheet_id, SUMMARY_SHEET_COLUMN_PROPERTIES, "Summary", 150, 0)
    # Create Category Sheets
    for categoryName, summary in data.items():
        table_values = [] 
        
        for transaction in summary:
            amount = transaction['amount']
            date = transaction['date']
            description = transaction['description']
            table_values.append([description, date.isoformat(), amount])
        table_values.append([])
        table_values.append([TOTAL, "",SUM_FORMULA])
        
        create_formatted_sheet(sheetsService, spread_sheet_id, CATEGORY_SHEET_COLUMN_PROPERTIES, categoryName, 250, 1)
        sheetsService.writeToSheet(spread_sheet_id, categoryName, table_values)
    # Create Summary Sheet
    # Do this last. Otherwise the REF's in the query will be null as they don't exist until all other sheets are created.
    for categoryName in data:
        budgetedAmount = CATEGORY_BUDGETS[categoryName]
        summary_table_values.append([
            categoryName,
            f"""=QUERY({categoryName}!A:C, "SELECT SUM(C) WHERE A != 'Total' LABEL SUM(C) ''")""",
            budgetedAmount,
            f"""={budgetedAmount}-QUERY({categoryName}!A:C, "SELECT SUM(C) WHERE A != 'Total' LABEL SUM(C) ''")""",
        ])
    
    for i in range(2):
        summary_table_values.append([])
    totalSpent = sum(CATEGORY_BUDGETS.values())
    summary_table_values.append(["Totals", "=SUM(B2:B7)", totalSpent, f"""={totalSpent}-SUM(B2:B7)""" ])
    sheetsService.writeToSheet(spread_sheet_id, "Summary", summary_table_values)

    
