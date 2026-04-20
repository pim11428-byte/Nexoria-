from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def subscription_keyboard():
    kb = [
        [InlineKeyboardButton(text="1 день -- 1.49$", callback_data="sub_day")],
        [InlineKeyboardButton(text="30 дней -- 14.99$ (рекомендуем)", callback_data="sub_month")],
        [InlineKeyboardButton(text="365 дней -- 59.99$", callback_data="sub_year")],
        [InlineKeyboardButton(text="Lifetime -- 89.99$ (самый выгодный)", callback_data="sub_lifetime")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def pay_keyboard(url: str):
    kb = [
        [InlineKeyboardButton(text="Оплатить через CryptoBot", url=url)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)