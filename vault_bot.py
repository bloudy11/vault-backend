
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram import F
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '7457096718:AAHi7K1mdEVxq5BiGXDPXOBCa4kT9XhWZUE'
WEBAPP_URL = 'https://build-fngztl9wb-edgars-projects-34cc2e66.vercel.app'

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Правильная инициализация клавиатуры:
web_app_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [ KeyboardButton(text="Open Vault", web_app=WebAppInfo(url=WEBAPP_URL)) ]
    ],
    resize_keyboard=True
)

@dp.message(F.text == "/start")
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Нажми на кнопку, чтобы открыть свой сейф:",
        reply_markup=web_app_keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())