import os
from datetime import datetime
from googleapiclient.http import MediaFileUpload

from app.config import APP_SETTINGS
from app.logger import logger


class Uploader:
    def __init__(self, service):
        self.service = service

    def create_drive_folder(self, folder_name, parent_id=None):
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            metadata["parents"] = [parent_id]

        folder = self.service.files().create(body=metadata, fields="id").execute()
        return folder["id"]

    def upload_file(self, file_path, parent_id):
        file_name = os.path.basename(file_path)
        media = MediaFileUpload(file_path, resumable=True)
        metadata = {"name": file_name, "parents": [parent_id]}

        uploaded = (
            self.service.files()
            .create(body=metadata, media_body=media, fields="id")
            .execute()
        )

        logger.info(f"Uploaded: {file_path}")
        return uploaded["id"]

    def upload_folder(
        self, local_path, parent_id=None, max_keep=APP_SETTINGS.max_files, is_root=True
    ):
        base_name = os.path.basename(local_path.rstrip("/\\"))

        folder_name = (
            base_name + datetime.now().strftime("-%Y%m%d-%H%M%S")
            if is_root
            else base_name
        )

        if is_root:
            self.cleanup_old_versions(base_name, parent_id, max_keep)

        logger.info(f"Created folder: {folder_name}")

        folder_id = self.create_drive_folder(folder_name, parent_id)

        for item in os.listdir(local_path):
            item_path = os.path.join(local_path, item)
            if os.path.isdir(item_path):
                self.upload_folder(item_path, folder_id, is_root=False)
            else:
                self.upload_file(item_path, folder_id)

    def cleanup_old_versions(self, base_name, parent_id, max_keep):
        query = (
            f"mimeType = 'application/vnd.google-apps.folder' and name contains '{base_name}' "
            f"and trashed = false and '{parent_id}' in parents"
        )

        response = (
            self.service.files()
            .list(
                q=query,
                fields="files(id, name, createdTime)",
                orderBy="createdTime desc",
            )
            .execute()
        )

        folders = response.get("files", [])
        if len(folders) > max_keep:
            for folder in folders[max_keep:]:
                self.service.files().delete(fileId=folder["id"]).execute()
                logger.info(f"Deleted old folder: {folder['name']}")
