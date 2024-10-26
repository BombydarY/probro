import json
from pprint import pprint

from create_bot import dp, bot
from aiogram import types, Dispatcher

from decorators import admin_check, error_check
from settings import ADMINS


@error_check
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, "Hello\n"
                                                 "/help_story_made\n"
                                                 "/help_person_made")


@error_check
async def text_handler(message: types.Message):
    pprint(message)
    await bot.send_message(message.chat.id, "You want see your person?/yes /no")

@error_check
async def files_handler(message: types.Message):
    if message.chat.type != "private":
        user = await bot.get_chat_member(message.chat.id,ADMINS[0])
        print(user)
        # todo: сделать так, что если админ (юзер переменная) - не является админов, то просто не выполнять дальше код
        # 2. ПРи команде старт - сделать проверку, что если старт написал в группе, то создаём папку с названием "лол123"
        # усложнение: назвать папку с таким же названием, как и называется группа
        file_id = message.photo[-1].file_id if message.photo else message.document.file_id
        file = await bot.get_file(file_id)
        file_name = message.document.file_name if message.document else "picture.jpg"
        await bot.download_file(file.file_path, file_name)

    pprint(message)
    await bot.send_message(message.chat.id, "You want see your person?/yes /no")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(text_handler, content_types=["text"])
    dp.register_message_handler(files_handler, content_types=["photo", "document"])

