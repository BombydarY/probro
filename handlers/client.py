import datetime
import json
from pprint import pprint
from create_bot import dp, bot
from aiogram import types, Dispatcher
import os
from decorators import admin_check, error_check
from settings import ADMINS
import quickstart

service = quickstart.get_google_api()


@error_check
async def send_welcome(message: types.Message):
    print(message)

    if message.chat.type != "private":
        user = await bot.get_chat_member(message.chat.id, ADMINS[0])
        if user.status != "left":
            now = datetime.datetime.now()
            new_file_path = now.strftime(f"{message.chat.title}_06_%m_%Y_{message.chat.id}")
            id_chat = message.chat.id
            folder_id = quickstart.exists_folder_id(service,str(id_chat))
            if not folder_id:
                quickstart.create_folder(service=service, folder_name=new_file_path)







@error_check
async def text_handler(message: types.Message):
    pprint(message)
    await bot.send_message(message.chat.id, "You want see your person?/yes /no")


@error_check
async def files_handler(message: types.Message):
    if message.chat.type != "private":
        user = await bot.get_chat_member(message.chat.id, ADMINS[0])
        if user.status != "left":
            id_chat = message.chat.id
            folder_id = quickstart.exists_folder_id(service, str(id_chat))
            if not folder_id:
                return
            file_id = message.photo[-1].file_id if message.photo else message.document.file_id
            now = datetime.datetime.now()
            file = await bot.get_file(file_id)
            file_name = message.document.file_name if message.document else "picture.jpg" # todo: в разные процессы (мб)
            new_file_path = now.strftime(f"%d_%m_%Y_%H_%M_%S_%f_{file_name}")
            await bot.download_file(file.file_path, new_file_path)
            quickstart.upload_files(service=service, file_name=new_file_path,based_file=new_file_path, folder_id=folder_id)







            await bot.send_message(message.chat.id, f"Файл {file_name} загружен.")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(text_handler, content_types=["text"])
    dp.register_message_handler(files_handler, content_types=["photo", "document"])
