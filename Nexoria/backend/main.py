import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

from billing import CreateInvoiceRequest, create_invoice_logic
from database import engine, Base

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Создаём таблицы при старте
Base.metadata.create_all(bind=engine)


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Бот работает на Render Worker + aiogram 3.x!")


@dp.message(Command("buy"))
async def buy_cmd(message: types.Message):
    req = CreateInvoiceRequest(
        tg_id=message.from_user.id,
        tariff="month"
    )

    try:
        invoice = create_invoice_logic(req)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
        return

    await message.answer(f"Счёт создан!\nОплатить: {invoice['pay_url']}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
