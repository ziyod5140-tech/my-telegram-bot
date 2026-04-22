import asyncio
import re
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. BOT SOZLAMALARI
TOKEN = "8715520167:AAFPa-1OBsEQJVuwfWtCDF6oYHxlxGQqpDg"
ADMIN_ID = 8541985358 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 2. SERVERNI "UYG'OQ" USHLASH UCHUN (FLASK)
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlamoqda..."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. BOT FUNKSIYALARI
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Savolingizni yozing.")

@dp.message()
async def handle_messages(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        user_info = f"👤 Ism: {message.from_user.full_name}\n🆔 User_ID: {message.from_user.id}\n💬 Xabar: {message.text}\n\n⚠️ Javob berish uchun 'Reply' qiling."
        await bot.send_message(chat_id=ADMIN_ID, text=user_info)
    elif message.from_user.id == ADMIN_ID and message.reply_to_message:
        original_text = message.reply_to_message.text
        match = re.search(r"User_ID:\s(\d+)", original_text)
        if match:
            user_id = int(match.group(1))
            await bot.send_message(chat_id=user_id, text=f"Admin javobi:\n\n{message.text}")
            await message.answer("✅ Javob yuborildi.")

async def main():
    keep_alive() # Serverni ishga tushirish
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())