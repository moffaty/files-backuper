import os
import io
from googleapiclient.http import MediaIoBaseDownload
from app.logger import logger


class Downloader:
    def __init__(self, service):
        self.service = service

    def download_file(self, file_id, dest_path):
        request = self.service.files().get_media(fileId=file_id)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        with io.FileIO(dest_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        logger.info(f"Downloaded: {dest_path}")

    def list_files_in_folder(self, folder_id):
        query = f"'{folder_id}' in parents and trashed = false"
        result = []
        page_token = None

        while True:
            response = (
                self.service.files()
                .list(
                    q=query,
                    fields="nextPageToken, files(id, name, mimeType)",
                    pageToken=page_token,
                )
                .execute()
            )
            result.extend(response.get("files", []))
            page_token = response.get("nextPageToken")
            if not page_token:
                break
        return result

    def find_folder_by_name(self, name, parent_id=None):
        parent_clause = f" and '{parent_id}' in parents" if parent_id else ""
        query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder'{parent_clause} and trashed = false"

        response = (
            self.service.files()
            .list(q=query, fields="files(id, name)", spaces="drive")
            .execute()
        )
        files = response.get("files", [])
        return files[0]["id"] if files else None

    def download_and_replace(self, folder_name, local_path, parent_id=None):
        folder_id = self.find_folder_by_name(folder_name, parent_id)
        if not folder_id:
            raise FileNotFoundError(f"Drive folder '{folder_name}' not found")

        if os.path.exists(local_path):
            logger.info(f"Removing existing folder: {local_path}")
            for root, dirs, files in os.walk(local_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

        self.download_drive_folder(folder_id, local_path)

    def download_drive_folder(self, folder_id, dest_path):
        os.makedirs(dest_path, exist_ok=True)
        items = self.list_files_in_folder(folder_id)

        for item in items:
            item_path = os.path.join(dest_path, item["name"])
            if item["mimeType"] == "application/vnd.google-apps.folder":
                self.download_drive_folder(item["id"], item_path)
            else:
                self.download_file(item["id"], item_path)
