import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

from handlers_subscription import register_subscription_handlers
from handlers_osint import register_osint_handlers

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет. Это NEXORIA.\n\n"
        "🔐 /subscription – подписка\n"
        "🕵️ /osint – OSINT‑анализ"
    )

def main():
    register_subscription_handlers(dp)
    register_osint_handlers(dp)
    asyncio.run(dp.start_polling(bot))

if __name__ == "__main__":
    main()
