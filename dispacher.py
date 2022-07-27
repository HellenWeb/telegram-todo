
# Modules

from aiogram import Bot, Dispatcher
import logging
from sqlighter import SQLighter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token

# Log

logging.basicConfig(level=logging.INFO)

# Default Var

storage = MemoryStorage()
bot = Bot(token, parse_mode='html')
dp = Dispatcher(bot, storage=storage)
db = SQLighter("db.db")

