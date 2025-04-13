import os
import json
from datetime import datetime
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "service_account.json"


def load_config(path=".env.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            config = json.load(f)
        return config
    return {}


def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def create_drive_folder(service, folder_name, parent_id=None):
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        file_metadata["parents"] = [parent_id]

    folder = service.files().create(body=file_metadata, fields="id").execute()
    return folder["id"]


def upload_file(service, file_path, parent_id):
    file_name = os.path.basename(file_path)
    media = MediaFileUpload(file_path, resumable=True)
    file_metadata = {"name": file_name, "parents": [parent_id]}
    uploaded_file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    return uploaded_file["id"]


def delete_old_world_folders(service, parent_id, max_folders):
    # Ищем папки с именем начинающимся на "world-" в указанной родительской папке
    query = (
        f"'{parent_id}' in parents and "
        "mimeType = 'application/vnd.google-apps.folder' and "
        "name contains 'world-' and trashed = false"
    )

    results = (
        service.files().list(q=query, fields="files(id, name, createdTime)").execute()
    )
    folders = results.get("files", [])

    # Сортировка по дате создания (старые — первыми)
    folders.sort(key=lambda x: x["createdTime"])

    if len(folders) >= max_folders:
        to_delete = folders[: len(folders) - max_folders + 1]
        for folder in to_delete:
            service.files().delete(fileId=folder["id"]).execute()
            print(f"Deleted old folder: {folder['name']}")


def upload_folder(service, folder_path, parent_id=None, max_files=None):
    folder_name = os.path.basename(folder_path) + datetime.now().strftime(
        "-%Y%m%d-%H%M%S"
    )
    folder_id = create_drive_folder(service, folder_name, parent_id)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            upload_folder(service, item_path, folder_id)
        else:
            upload_file(service, item_path, folder_id)


def main():
    parser = argparse.ArgumentParser(
        description="Upload a local folder to Google Drive using a service account."
    )
    parser.add_argument("folder", help="Path to the local folder to upload")
    parser.add_argument(
        "--parent",
        help="Google Drive Folder ID to upload into (optional)",
        default=None,
    )
    parser.add_argument(
        "--max-files",
        type=int,
        help="Maximum number of files to upload (optional)",
        default=None,
    )
    args = parser.parse_args()

    config = load_config()
    max_files = config.get("max_files", args.max_files)
    parent_id = config.get("parent_id", args.parent)

    folder_path = args.folder
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a directory")
        return

    service = authenticate()

    if args.parent:
        delete_old_world_folders(service, parent_id=parent_id, max_folders=max_files)

    upload_folder(service, folder_path, parent_id=parent_id)
    print(f'Uploaded "{folder_path}" to Google Drive.')


if __name__ == "__main__":
    main()
