import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_google_api():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        # upload_files(service, "bo.png", "test3_08_11_2024_-4535479786/08_11_2024_22_35_02_853977_picture.jpg")
        # create_folder(service, "test3_08_11_2024")  # Создаем папку с текущим датой и временем
        return service
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
        return None


def upload_files(service, file_name, based_file) -> bool:
    file_metadata = {'name': file_name}
    media = MediaFileUpload(based_file, resumable=True)

    # Загружаем файл
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f'Файл загружен на Google Диск. ID файла: {file.get("id")}')
        return True
    except Exception as err:
        print(f"Ошибка в download_files:{err}")
        return False


def create_folder(service, folder_name):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    try:
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f'Папка создана на Google Диск. ID папки: {folder.get("id")}')
        return True
    except Exception as error:
        print(f"An error occurred: {error}")
        return False


def exists_folder(service, folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])

    if files:
        print(f"Found {len(files)} folder(s) named '{folder_name}':")
        for file in files:
            print(f"Folder ID: {file['id']}, Folder Name: {file['name']}")
        return True
    else:
        print(f"No folder named '{folder_name}' found.")
        return False


def get_more_inf(service):
    results = (
        service.files()
        .list(pageSize=5,
              fields="nextPageToken, files(id, name,mimeType,createdTime,size,webViewLink,webContentLink,shared,owners)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found.")
        return
    print("Files:")

    for item in items:
        # if  item["mimeType"] != "image/png":
        print(item)
        # print(f"{item['name']} ({item['id']})")





if __name__ == "__main__":
    service = get_google_api()
    exists_folder(service,folder_name = "test2_22_11_2024_-10023691228223")
