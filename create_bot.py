from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from settings import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
