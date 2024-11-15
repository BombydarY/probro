import datetime
import json
from pprint import pprint
from create_bot import dp, bot
from aiogram import types, Dispatcher
import os
from decorators import admin_check, error_check
from settings import ADMINS


@error_check
async def send_welcome(message: types.Message):
    print (message)

    if message.chat.type != "private":
        user = await bot.get_chat_member(message.chat.id, ADMINS[0])
        if user.status != "left":
            now = datetime.datetime.now()
            new_file_path = now.strftime(f"{message.chat.title}_%d_%m_%Y_{message.chat.id}")
            if not os.path.exists(new_file_path):
                os.mkdir(new_file_path)



            # todo: здесь происходит ошибка, на неё всё равно, потому что декоратор твой работает норм
            # но, бот отправляет логи (тех. информацию) в чаты с клиентами, так делать не надо, сделать так:
            # создать новую группу, она будет служить чисто для отправки разныех ошибок, вот именно туда и отправлять ошибки




@error_check
async def text_handler(message: types.Message):
    pprint(message)
    await bot.send_message(message.chat.id, "You want see your person?/yes /no")

@error_check
async def files_handler(message: types.Message):
    if message.chat.type != "private":
        user = await bot.get_chat_member(message.chat.id,ADMINS[0])
        if user.status != "left":
            now = datetime.datetime.now()
            chat_id = message.chat.id
            s = ""
            for a in os.listdir():
                if os.path.isdir(a):
                    if str(chat_id) in a:
                        s = a
                        break

            file_id = message.photo[-1].file_id if message.photo else message.document.file_id

            file = await bot.get_file(file_id)
            file_name = message.document.file_name if message.document else "picture.jpg"
            new_file_path = now.strftime(f"{s}/%d_%m_%Y_%H_%M_%S_%f_{file_name}")
            await bot.download_file(file.file_path, new_file_path)

            await bot.send_message(message.chat.id, f"Файл {file_name} загружен.")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(text_handler, content_types=["text"])
    dp.register_message_handler(files_handler, content_types=["photo", "document"])

