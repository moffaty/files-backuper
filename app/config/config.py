from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List, Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    max_files: Optional[int] = Field(
        default=5,
        description="Maximum number of files to upload to Google Drive",
    )
    parent_dir: Optional[str] = Field(
        default="",
        description="Parent directory ID in Google Drive",
    )
    scopes: Optional[List[str]] = Field(
        default=["https://www.googleapis.com/auth/drive"],
        description="Google Drive API scopes",
    )
    service_account_file: Optional[str] = Field(
        default="service_account.json",
        description="Path to the Google Drive API credentials file",
    )
    world_folder: Optional[str] = Field(
        default="",
        description="World folder name in Google Drive",
    )


APP_SETTINGS = Settings()

if __name__ == "__main__":
    print(APP_SETTINGS.model_dump())
