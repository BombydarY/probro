import datetime
import json
from pprint import pprint
from create_bot import dp, bot
from aiogram import types, Dispatcher
import os
from decorators import admin_check, error_check
from settings import ADMINS
import quickstart
import logging

# Настройка базового логгера
logging.basicConfig(level=logging.DEBUG,  # Уровень логирования
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщений
                    datefmt='%Y-%m-%d %H:%M:%S',  # Формат даты и времени
                    filename='app.log',  # Файл, в который будут писаться логи
                    filemode='w')  # Режим записи в файл




service = quickstart.get_google_api()


@error_check
async def send_welcome(message: types.Message):
    """приветствие и проверка групы на достоверность(нахождение в ней админа),содание папки"""
    # print(message)


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
async def files_handler(message: types.Message):
    """отслеживавние и загрузка файлов"""
    if message.chat.type != "private":
        user = await bot.get_chat_member(message.chat.id, ADMINS[0])
        
        if user.status != "left":
            id_chat = message.chat.id
            folder_id = quickstart.exists_folder_id(service, str(id_chat))

            # если папки не существует (если не нажата /start в чате) - выбрасываем из функции 
            if not folder_id:   
                return

            file_id = message.photo[-1].file_id if message.photo else message.document.file_id
            now = datetime.datetime.now()
            file = await bot.get_file(file_id)
            file_name = message.document.file_name if message.document else "picture.jpg" # todo: в разные процессы (мб)
            new_file_path = now.strftime(f"%d_%m_%Y_%H_%M_%S_%f_{file_name}")
            await bot.download_file(file.file_path, new_file_path)

            quickstart.upload_files(service=service, file_name=new_file_path,based_file=new_file_path, folder_id=folder_id)
            logging.debug(f"{file_name} был клёво сохранён. Всё чики-пуки")
            await bot.send_message(message.chat.id, f"Файл {file_name} загружен.")  # todo: нужно ли сообщать в чат, что файл был загружен? узнать у дяди
            # todo: для Паши. обязательно удалять локал файлы после скачивания

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(files_handler, content_types=["photo", "document"])
