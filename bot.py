import asyncio
import re
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- SOZLAMALAR ---
TOKEN = "8715520167:AAFPa-1OBsEQJVuwfWtCDF6oYHxlxGQqpDg"
ADMIN_ID = 8541985358

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask('')

# --- SERVERNI UYG'OQ USHLASH (RENDER UCHUN) ---
@app.route('/')
def home():
    return "Bot is running..."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# --- TUGMALAR (MENU) ---
def get_main_menu():
    buttons = [
        [KeyboardButton(text="🆘 Yordam"), KeyboardButton(text="ℹ️ Bot haqida")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- BOT FUNKSIYALARI ---

# /start buyrug'i
@dp.message(Command("start"))
async def start_command(message: types.Message):
    welcome_text = (
        f"Assalomu alaykum, {message.from_user.full_name}!\n\n"
        "Men orqali adminga savollaringizni yuborishingiz mumkin.\n"
        "Xabaringizni yozing va men uni yetkazaman."
    )
    await message.answer(welcome_text, reply_markup=get_main_menu())

# Tugmalar bosilganda
@dp.message(lambda m: m.text in ["🆘 Yordam", "ℹ️ Bot haqida"])
async def menu_handler(message: types.Message):
    if message.text == "🆘 Yordam":
        await message.answer("Xabaringizni shunchaki yozib yuboring, admin tez orada javob beradi.")
    else:
        await message.answer("Bu bot Bahriyya loyihasi uchun maxsus yaratilgan.")

# Umumiy xabarlarga ishlov berish
@dp.message()
async def handle_all_messages(message: types.Message):
    # Agar foydalanuvchi yozsa (Admindan boshqa hamma)
    if message.from_user.id != ADMIN_ID:
        admin_info = (
            f"📩 **Yangi xabar!**\n\n"
            f"👤 Ism: {message.from_user.full_name}\n"
            f"🆔 User_ID: {message.from_user.id}\n"
            f"🔗 Username: @{message.from_user.username if message.from_user.username else 'yoq'}\n"
            f"------------------------------\n"
            f"💬 Xabar: {message.text}\n"
            f"------------------------------\n"
            f"Javob berish uchun xabarga 'Reply' qiling."
        )
        try:
            await bot.send_message(ADMIN_ID, admin_info, parse_mode="Markdown")
            await message.answer("✅ Xabaringiz adminga yuborildi.")
        except Exception as e:
            # Agar Markdown xato bersa, oddiy matnda yuborish
            await bot.send_message(ADMIN_ID, admin_info.replace("**", ""))
            await message.answer("✅ Xabaringiz yuborildi.")

    # Agar Admin "Reply" qilib javob yozsa
    elif message.reply_to_message:
        try:
            # Xabar ichidan User_ID ni qidirib topish
            text = message.reply_to_message.text
            match = re.search(r"User_ID: (\d+)", text)
            if match:
                target_id = int(match.group(1))
                await bot.send_message(target_id, f"**Bahriyya**💙\n\n{message.text}", parse_mode="Markdown")
                await message.answer("✅ Javobingiz foydalanuvchiga yetkazildi.")
            else:
                await message.answer("❌ Xato: Xabar ichidan User_ID topilmadi.")
        except Exception as e:
            await message.answer(f"❌ Yuborishda xato: {e}")

# --- ASOSIY ISHGA TUSHIRISH ---
async def main():
    keep_alive()
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
