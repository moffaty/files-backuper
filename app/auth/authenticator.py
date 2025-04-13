from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config import APP_SETTINGS


class Authenticator:
    def __init__(self):
        self.service_account_file = APP_SETTINGS.service_account_file
        self.scopes = APP_SETTINGS.scopes

    def get_service(self, api_name="drive", api_version="v3"):
        creds = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.scopes
        )
        return build(api_name, api_version, credentials=creds)
