from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import httpx
import os

from keyboards import subscription_keyboard, pay_keyboard

BACKEND_URL = os.getenv("BACKEND_URL")

router = Router()

@router.message(Command("subscription"))
async def subscription_status(message: Message):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{BACKEND_URL}/api/subscriptions/status",
            params={"tg_id": message.from_user.id}
        )
    data = r.json()

    if data["status"] == "active":
        text = f"✔ Подписка активна до: {data['expires_at']}"
    elif data["status"] == "lifetime":
        text = "✔ У вас Lifetime‑подписка."
    else:
        text = "❌ Подписка не активна.\n\nВыберите тариф:"
    await message.answer(text, reply_markup=subscription_keyboard())

@router.callback_query(lambda c: c.data.startswith("sub_"))
async def subscription_choose(call: CallbackQuery):
    tariff = call.data.split("_", 1)[1]

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BACKEND_URL}/api/billing/create_invoice",
            json={"tg_id": call.from_user.id, "tariff": tariff}
        )
    data = r.json()
    pay_url = data["pay_url"]

    await call.message.answer(
        f"💳 Ваш чек готов.\n\nТариф: {data['tariff_name']}\nСумма: {data['amount']} {data['asset']}",
        reply_markup=pay_keyboard(pay_url)
    )
    await call.answer()

def register_subscription_handlers(dp):
    dp.include_router(router)