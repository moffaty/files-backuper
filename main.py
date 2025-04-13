import argparse
from app.auth import Authenticator
from app.uploader import Uploader
from app.downloader import Downloader
from app.config import APP_SETTINGS


def main():
    parser = argparse.ArgumentParser(description="Google Drive sync utility")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Upload command
    upload_parser = subparsers.add_parser(
        "upload", help="Upload folder to Google Drive"
    )
    upload_parser.add_argument(
        "--local_path",
        default=APP_SETTINGS.world_folder,
        help="Local folder path to upload",
    )
    upload_parser.add_argument(
        "--parent",
        default=APP_SETTINGS.parent_dir,
        help="Drive folder ID to upload into",
    )
    upload_parser.add_argument(
        "--limit",
        type=int,
        default=APP_SETTINGS.max_files,
        help="Max uploads to keep in Drive",
    )

    # Download command
    download_parser = subparsers.add_parser(
        "download", help="Download folder from Google Drive"
    )
    download_parser.add_argument(
        "drive_folder_name", help="Name of the Drive folder to download"
    )
    download_parser.add_argument(
        "local_target",
        default=APP_SETTINGS.world_folder,
        help="Local path to save downloaded folder",
    )
    download_parser.add_argument(
        "--parent",
        default=APP_SETTINGS.parent_dir,
        help="Drive parent folder ID to search within",
    )

    args = parser.parse_args()
    service = Authenticator().get_service()

    if args.command == "upload":
        uploader = Uploader(service)
        uploader.upload_folder(
            local_path=args.local_path, parent_id=args.parent, max_keep=args.limit
        )

    elif args.command == "download":
        downloader = Downloader(service)
        downloader.download_and_replace(
            folder_name=args.drive_folder_name,
            local_path=args.local_target,
            parent_id=args.parent,
        )


if __name__ == "__main__":
    main()
