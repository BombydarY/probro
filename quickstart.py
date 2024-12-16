import os.path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_google_api():   # todo: сделать тайпхинты
    """Создание экземпляра Google API"""
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
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def upload_files(service: Resource, file_name: str, based_file: str, folder_id: str) -> bool:
    """Загрузка файлов на гугл драйв (АПИ)"""
    file_metadata = {'name': file_name, "parents": [folder_id]}
    media = MediaFileUpload(based_file, resumable=True)

    # Загружаем файл
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        logging.debug(f'Файл загружен на Google Диск. ID файла: {file.get("id")}')
        return True
    except Exception as err:
        logging.error(f"Ошибка в download_files:{err}")
        return False


def create_folder(service:Resource, folder_name:str)->bool:
    """Создание папки на гугл драqв (АПИ)"""
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ['1Fx09qIryiKi3Nj1CtWMqomh14Xc_BfX1'],
    }
    try:
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f'Папка создана на Google Диск. ID папки: {folder.get("id")}')
        return True
    except Exception as error:
        print(f"An error occurred: {error}")
        return False


def exists_folder(service:Resource, folder_name:str)->bool:
    """Проверка наличия папки на гугл драив (АПИ)"""
    chat_id = -4535479786
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


# def exists_folder_id(service:Resource, chat_id: str): # todo: сделать тайпхинты
#     """проверяет наличие ID папки"""
#     results = service.files().list(pageSize=5,
#                                    fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
#     items = results.get('files', [])
#     if not items:
#         return False
#     for item in items:
#         if chat_id in item["name"]:
#             print(item["id"])
#             return item["id"]



def exists_folder_id(service, chat_id: str, parent_folder_id: str = "1Fx09qIryiKi3Nj1CtWMqomh14Xc_BfX1") -> str:
    query = (
        f"'{parent_folder_id}' in parents and "
        f"name contains '{chat_id}' and "
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"trashed = false")
    try:
        results = service.files().list(
            q=query,
            pageSize=10,
            fields="files(id, name)"
        ).execute()

        items = results.get('files', [])
        if not items:
            print("No files found")
            return False

        folder_id = items[0]["id"]
        print(f"ID папки с фрагментом названия '{chat_id}' найдена: {folder_id}")
        return folder_id
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None



def get_more_inf(service:Resource): # todo: избавиться или закомментировать функцию
    """Получает информацию о всех загруженных файлах на диске"""
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

    for item in items:
        print(item)

    return None



if __name__ == "__main__":
    service = get_google_api()
    # print(exists_folder(service,folder_name = "test2_22_11_2024"))
    # exists_folder_id(service, chat_id="")
    # upload_files(service, "test2_02_12_2024_-4535479786/02_12_2024_22_14_04_754261_picture.jpg",
    #              "test3_08_11_2024_-4535479786/02_12_2024_22_14_04_754261_picture.jpg", folder_id="")
    # print(exists_folder_id2(service, chat_id="-4535479786"))
    # list_folders(service)
    # print(exists_folder_with_name_fragment(service, name_fragment="-4535479780"))

# todo: везде, где принты - писать logging.debug() or logging.error() + не забыть написать import logging в том файле, где мы пишем