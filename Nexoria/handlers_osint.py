from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import httpx
import os

BACKEND_URL = os.getenv("BACKEND_URL")

router = Router()

@router.message(Command("osint"))
async def osint_start(message: Message):
    await message.answer("Отправь сущность (email, телефон, домен, IP, username, ФИО).")

@router.message()
async def osint_entity(message: Message):
    entity = message.text.strip()

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BACKEND_URL}/api/osint/analyze",
            json={"tg_id": message.from_user.id, "entity": entity}
        )
    data = r.json()

    if data.get("error"):
        await message.answer(f"⚠ {data['error']}")
        return

    await message.answer(f"🕵️ Результат анализа:\n\n{data['summary']}")

def register_osint_handlers(dp):
    dp.include_router(router)