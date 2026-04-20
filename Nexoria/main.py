import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# -----------------------------
#        ХЕНДЛЕРЫ
# -----------------------------

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Бот работает на aiogram 3.x и полностью совместим с Render!")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Команды:\n/start -- запуск\n/help -- помощь")


# -----------------------------
#        ЗАПУСК БОТА
# -----------------------------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
