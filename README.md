# Files Backuper

## How to Obtain `service_account.json` from Google

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Credentials**.
4. Click **Create Credentials** and select **Service Account**.
5. Fill in the required details and click **Create**.
6. Assign the necessary roles (e.g., **Editor** or **Owner**) and click **Continue**.
7. Skip granting users access and click **Done**.
8. In the **Credentials** tab, find your service account and click the **Edit** icon.
9. Go to the **Keys** tab and click **Add Key > Create New Key**.
10. Select **JSON** as the key type and click **Create**.
11. Save the downloaded `service_account.json` file securely.

## Installation Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/moffaty/files-backuper.git
   cd files-backuper
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Place the `service_account.json` file in the project root directory.

4. Run the application:

   ```bash
   python main.py {upload/download} local_path --options
   # to see more run `python main.py -h`
   ```
