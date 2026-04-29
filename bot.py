import asyncio
import re
import os
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- SOZLAMALAR ---
TOKEN = "8715520167:AAFPa-1OBsEQJVuwfWtCDF6oYHxlxGQqpDg"
ADMIN_ID = 6516654407

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask('')

# --- RENDER UCHUN DOIMIY ALOQA ---
@app.route('/')
def home():
    return "Bot is active and running!"

def run():
    # Render avtomatik port beradi, shuni ishlatish xavfsizroq
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()

# --- TUGMALAR ---
def get_menu():
    buttons = [[KeyboardButton(text="🆘 Yordam"), KeyboardButton(text="ℹ️ Bot haqida")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- XABARLAR ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Assalomu alaykum! Savolingizni yozing, admin javob beradi.", reply_markup=get_menu())

@dp.message()
async def all_handler(message: types.Message):
    try:
        # Agar foydalanuvchi yozsa
        if message.from_user.id != ADMIN_ID:
            msg_text = message.text if message.text else "[Fayl yoki Rasm]"
            admin_msg = (
                f"📩 **Yangi xabar!**\n\n"
                f"👤 Ism: {message.from_user.full_name}\n"
                f"🆔 User_ID: `{message.from_user.id}`\n"
                f"🔗 Username: @{message.from_user.username if message.from_user.username else 'yoq'}\n"
                f"------------------------------\n"
                f"💬 Xabar: {msg_text}\n"
                f"------------------------------\n"
                f"Javob berish uchun xabarga Reply qiling."
            )
            await bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
            await message.answer("✅ Xabaringiz yuborildi.")

        # Admin javob bersa
        elif message.reply_to_message:
            # User_ID ni qidirish
            match = re.search(r"User_ID: `(\d+)`", message.reply_to_message.text)
            if match:
                user_id = int(match.group(1))
                await bot.send_message(user_id, f"**Bahriyya**💙\n\n{message.text}", parse_mode="Markdown")
                await message.answer("✅ Javobingiz foydalanuvchiga ketdi.")
    except Exception as e:
        print(f"Xatolik: {e}")

async def main():
    keep_alive()
    # skip_updates=True bot o'chib yonganida eski xabarlarga tiqilib qolmasligi uchun
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
