from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "service_account.json"
BUDGETING_FOLDER_ID='1XPKQecIqtb3zxkc7bPQN3GZtlMNSPN1R'

class FolderNotFoundError(Exception):
    pass

class FileNotFoundError(Exception):
    pass

class GoogleDrive:

    def __init__(self):
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        self.service = build("drive", "v3", credentials=creds)
    
    def find_file_by_name(self, name: str, folder_id: str) -> str:        
        response = self.service.files().list(
            q=f"name='{name}' and mimeType='application/vnd.google-apps.spreadsheet' and '{folder_id}' in parents and trashed=false",
            fields="files(id, name)"
        ).execute()
        
        files = response.get("files", [])
        if not files:
            raise FileNotFoundError
        
        return files[0]["id"]
    
    def find_folder_by_name(self, name: str) -> str:        
        query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        query += f" and '{BUDGETING_FOLDER_ID}' in parents"
        
        response = self.service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        
        files = response.get("files", [])
        if not files:
            raise FolderNotFoundError
        
        return files[0]["id"]

   