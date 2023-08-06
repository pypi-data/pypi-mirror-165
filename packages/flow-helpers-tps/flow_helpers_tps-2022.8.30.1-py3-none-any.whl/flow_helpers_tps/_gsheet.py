from google.oauth2 import service_account
from apiclient.discovery import build
import pandas as pd


class GSheet:
    def __init__(self, key):
        self.key=key
        credentials = service_account.Credentials.from_service_account_info(self.key)
        self.service = build('sheets', 'v4', credentials=credentials)

    def pull(self,spreadsheet_id,sheet_id):
        sheet = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_id).execute()
        return sheet

    def to_dataframe(sheet):
        df = pd.DataFrame(sheet.get("values")[1:], columns=sheet.get("values")[0])
        return df