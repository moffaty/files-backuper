from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config import APP_SETTINGS
import os
import functools


class Authenticator:
    def __init__(self):
        self.service_account_file = APP_SETTINGS.service_account_file
        self.scopes = APP_SETTINGS.scopes

    @functools.cache
    def get_service(self, api_name="drive", api_version="v3"):
        if not os.path.exists(self.service_account_file):
            raise FileNotFoundError(
                f"Service account file '{self.service_account_file}' not found."
            )

        creds = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.scopes
        )
        service = build(api_name, api_version, credentials=creds)
        return service
