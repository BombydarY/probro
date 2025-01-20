import datetime
import json
import re
from pprint import pprint
from create_bot import dp, bot
from aiogram import types, Dispatcher
import os
from decorators import admin_check, error_check
from settings import ADMINS, ID_MISTAKES
import quickstart
import logging
from aiogram.utils.exceptions import FileIsTooBig
# Настройка базового логгера
logging.basicConfig(level=logging.DEBUG,  # Уровень логирования
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщений
                    datefmt='%Y-%m-%d %H:%M:%S',  # Формат даты и времени
                    filename='app.log',  # Файл, в который будут писаться логи
                    filemode='w')  # Режим записи в файл

service = quickstart.get_google_api()


def remove_emojis(text):
    """Удаляет все эмоджи и нестандартные символы из строки"""
    # Удаляем все символы, которые не являются буквами, цифрами, пробелами или стандартными знаками
    return re.sub(r'[^\w\s\-_\.\(\)]', '', text)


@error_check
async def send_welcome(message: types.Message):
    """приветствие и проверка группы на достоверность(нахождение в ней админа),содание папки"""
    print(message)

    if message.chat.type != "private":
        user = await bot.get_chat_member(message.chat.id, ADMINS[0])
        if user.status != "left":
            now = datetime.datetime.now()

            safe_chat_title = remove_emojis(message.chat.title)

            new_file_path = now.strftime(f"{safe_chat_title}_06_%m_%Y_{message.chat.id}")
            id_chat = message.chat.id
            folder_id = quickstart.exists_folder_id(service, str(id_chat))
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
            try:
                file = await bot.get_file(file_id)
            except FileIsTooBig as e:
                await bot.send_message(ID_MISTAKES,
                                       f"Файл очень большой, инфо:\n\nНазвание группы: {message.chat.title}\nАйди: {message.chat.id}")
                await bot.forward_message(ID_MISTAKES,id_chat,message.message_id)
                return


            try:
                file_name = message.document.file_name if message.document else "picture.jpg"
            except Exception as e:
                await bot.send_message(ID_MISTAKES,
                                       f"⚠️ Обработанная ошибка, связанная с названием файла в функции files_handler! Описание: {e}")
                file_name = 'unknown.jpg'

            new_file_path = now.strftime(f"%d_%m_%Y_%H_%M_%S_%f_{file_name}")

            try:
                await bot.download_file(file.file_path, new_file_path)

                quickstart.upload_files(service=service, file_name=new_file_path, based_file=new_file_path,
                                        folder_id=folder_id)
                logging.debug(f"{file_name} был клёво сохранён. Всё чики-пуки")
                await bot.send_message(message.chat.id,
                                       f"Файл {file_name} загружен.")  # todo: нужно ли сообщать в чат, что файл был загружен? узнать у дяди
                # todo: для Паши. обязательно удалять локал файлы после скачивания
            except Exception as e:
                await bot.send_message(ID_MISTAKES,
                                       f"❗❗Неизвестная ошибка при загрузке файла в функции files_handler! Описание: {e}")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(files_handler, content_types=["photo", "document"])
