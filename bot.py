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

# --- RENDER UCHUN SERVER (UYG'OQ USHLASH) ---
@app.route('/')
def home():
    return "Bot is running..."

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()

# --- TUGMALAR (MENYU) ---
def get_main_menu():
    buttons = [
        [KeyboardButton(text="🆘 Yordam"), KeyboardButton(text="ℹ️ Bot haqida")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- BOT FUNKSIYALARI ---

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\nSavolingizni yozing, admin javob beradi.",
        reply_markup=get_main_menu()
    )

@dp.message(lambda m: m.text in ["🆘 Yordam", "ℹ️ Bot haqida"])
async def menu_handler(message: types.Message):
    if message.text == "🆘 Yordam":
        await message.answer("Xabaringizni yozib yuboring, admin tez orada javob beradi.")
    else:
        await message.answer("Ushbu bot admin bilan bog'lanish uchun xizmat qiladi.")

@dp.message()
async def message_handler(message: types.Message):
    # Foydalanuvchi adminga yozsa
    if message.from_user.id != ADMIN_ID:
        admin_info = (
            f"📩 **Yangi xabar!**\n\n"
            f"👤 Ism: {message.from_user.full_name}\n"
            f"🆔 User_ID: `{message.from_user.id}`\n"
            f"💬 Xabar: {message.text if message.text else '[Fayl]'}\n\n"
            f"Javob berish uchun xabarga Reply qiling."
        )
        try:
            await bot.send_message(ADMIN_ID, admin_info, parse_mode="Markdown")
            await message.answer("✅ Xabaringiz adminga yuborildi.")
        except:
            await bot.send_message(ADMIN_ID, admin_info.replace("`", ""))
            await message.answer("✅ Xabaringiz yuborildi.")

    # Admin javob bersa
    elif message.reply_to_message:
        try:
            # User_ID ni qidirish
            user_id_match = re.search(r"User_ID: `(\d+)`", message.reply_to_message.text)
            if not user_id_match:
                user_id_match = re.search(r"User_ID: (\d+)", message.reply_to_message.text)

            if user_id_match:
                target_id = int(user_id_match.group(1))
                await bot.send_message(target_id, f"**Bahriyya**💙\n\n{message.text}", parse_mode="Markdown")
                await message.answer("✅ Javobingiz yuborildi.")
            else:
                await message.answer("❌ Xato: User_ID topilmadi.")
        except Exception as e:
            await message.answer(f"❌ Xatolik: {e}")

async def main():
    keep_alive()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
