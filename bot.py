import asyncio
import re
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types

# 1. BOT SOZLAMALARI
TOKEN = "8715520167:AAFPa-1OBsEQJVuwfWtCDF6oYHxlxGQqpDg"
ADMIN_ID = 8541985358

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlamoqda..."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. BOT FUNKSIYALARI
@dp.message(lambda message: message.text == "/start")
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Savolingizni yozing.")

@dp.message()
async def handle_messages(message: types.Message):
    # Foydalanuvchi yozsa
    if message.from_user.id != ADMIN_ID:
        user_name = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
        
        admin_text = (
            f"Yangi xabar!\n"
            f"Ism: {message.from_user.full_name}\n"
            f"User_ID: {message.from_user.id}\n"
            f"Username: {user_name}\n"
            f"----------\n"
            f"Xabar: {message.text}\n"
            f"----------\n"
            f"Javob berish uchun Reply qiling."
        )
        
        await bot.send_message(chat_id=ADMIN_ID, text=admin_text)
        await message.answer("✅ Xabaringiz yuborildi.")

    # Admin javob bersa
    elif message.reply_to_message:
        try:
            text = message.reply_to_message.text
            match = re.search(r"User_ID: (\d+)", text)
            if match:
                user_id = int(match.group(1))
                await bot.send_message(chat_id=user_id, text=f"Bahriyya💙\n\n{message.text}")
                await message.answer("✅ Javob yuborildi.")
        except:
            pass

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
