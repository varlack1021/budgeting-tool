from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import TypedDict
from googleapiclient.errors import HttpError
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = "service_account.json"
BUDGETING_FOLDER_ID='1XPKQecIqtb3zxkc7bPQN3GZtlMNSPN1R?'

class ColumnProperty(TypedDict, total=False):
    columnName: str
    columnIndex: int

class SheetExistsError(Exception):
    pass

class GoogleSheets:
    def __init__(self):
        # Load credentials directly from your local JSON key file
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        self.service = build("sheets", "v4", credentials=creds).spreadsheets()
    
    def clearSheets(self, spreadsheet_id, sheets: list[str]):
        tabs_to_reset = sheets

        request_body = {
            "ranges": tabs_to_reset
        }

        self.service.values().batchClear(
            spreadsheetId=spreadsheet_id,
            body=request_body
        ).execute()

    def create_new_sheet(self, spreadsheet_id, sheet_name) -> str:
        batch_update_request = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": sheet_name,
                            "gridProperties": {
                                "rowCount": 100,  
                                "columnCount": 20     
                            }
                        }
                    }
                }
            ]
        }

        try:
            result = self.service.batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=batch_update_request
            ).execute()
            return result['replies'][0]['addSheet']['properties']['sheetId']

        except HttpError as error:
        # 1. Parse the JSON bytes into a dictionary
            error_data = json.loads(error.content.decode('utf-8'))
            message = error_data.get('error', {}).get('message', 'No message found')
            if ("Please enter another name" in message):
                raise SheetExistsError
            
            raise error


    def get_sheet_id_by_name(self, spreadsheet_id, sheet_name):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = spreadsheet.get('sheets', [])

        for sheet in sheets:
            properties = sheet.get('properties', {})
            if properties.get('title') == sheet_name:
                return properties.get('sheetId')
        raise ValueError("sheet name could not be found")

    def add_table(self, spreadsheet_id, sheet_id, column_properties: list[ColumnProperty], table_name):
        requests = [
    {
    # Create table
        "addTable": {
            "table": {
                "name": table_name,
                "range": {
                    "sheetId": sheet_id,           
                    "startRowIndex": 0,    
                    "endRowIndex": 50,    
                    "startColumnIndex": 0, 
                    "endColumnIndex":len(column_properties),
                },
                "columnProperties": column_properties
            }
        },
    },
    # Center align items
    {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0, "endRowIndex": 70,
                "startColumnIndex": 0, "endColumnIndex": len(column_properties)
            },
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment": "CENTER"
                }
            },
            "fields": "userEnteredFormat.horizontalAlignment"
            }
        },
    # Format amount col as number. Requieres amount col to be last col.
    {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startColumnIndex": len(column_properties)-1,
                "endColumnIndex": len(column_properties)
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": "NUMBER",
                        "pattern": "#,##0.00"
                    }
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    }
    ]
        self.service.batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={'requests': requests}
).execute()
    
    def adjust_column_width(self, spreadsheet_id, sheet_id, colNumber, size):
        requests=[
              {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": colNumber,  # Starting at Column A
                "endIndex": colNumber + 1     # Ending before Column B (so, just Column A)
            },
            "properties": {
                "pixelSize": size
            },
            "fields": "pixelSize"
        }
    }
        ]
        self.service.batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
            ).execute()

    def writeToSheet(self, spreadsheet_id, sheet_name, table_values):
        self.service.values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A2",
            valueInputOption="USER_ENTERED",
            body={"values": table_values}
        ).execute()
    