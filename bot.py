import asyncio
import re
import os
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --- SOZLAMALAR ---
# Tokeningizni @BotFather dan olingan yangi tokenga almashtirishingiz mumkin
TOKEN = "8715520167:AAFPa-1OBsEQJVuwfWtCDF6oYHxlxGQqpDg"
ADMIN_ID = 6516654407

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask('')

# --- RENDER UCHUN SERVER (UYG'OQ USHLASH) ---
@app.route('/')
def home():
    return "Bot status: Active"

def run():
    # Render portni avtomatik beradi, bo'lmasa 8080 ishlatiladi
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()

# --- TUGMALAR (ASOSIY MENYU) ---
def main_menu():
    buttons = [
        [KeyboardButton(text="🆘 Yordam"), KeyboardButton(text="ℹ️ Bot haqida")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- BOT LOGIKASI ---

# /start buyrug'i
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    welcome_text = (
        f"Assalomu alaykum, {message.from_user.full_name}!\n\n"
        "Bahriyya botiga xush kelibsiz. Savolingiz bo'lsa yozib qoldiring, "
        "admin sizga tez orada javob beradi."
    )
    await message.answer(welcome_text, reply_markup=main_menu())

# Tugmalar bosilganda
@dp.message(lambda m: m.text in ["🆘 Yordam", "ℹ️ Bot haqida"])
async def menu_handler(message: types.Message):
    if message.text == "🆘 Yordam":
        await message.answer("Xabaringizni shunchaki matn shaklida yuboring, men uni adminga yetkazaman.")
    else:
        await message.answer("Ushbu bot 'Bahriyya' loyihasi uchun maxsus ishlab chiqilgan.")

# Umumiy xabarlar (Foydalanuvchi va Admin uchun)
@dp.message()
async def message_handler(message: types.Message):
    # 1. Foydalanuvchi adminga yozsa
    if message.from_user.id != ADMIN_ID:
        # Username bor-yo'qligini tekshirish
        username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
        
        admin_text = (
            f"📩 **Yangi xabar!**\n\n"
            f"👤 Ism: {message.from_user.full_name}\n"
            f"🆔 User_ID: `{message.from_user.id}`\n"
            f"🔗 Username: {username}\n"
            f"------------------------------\n"
            f"💬 Xabar: {message.text if message.text else '[Fayl/Rasm]'}\n"
            f"------------------------------\n"
            f"Javob berish uchun xabarga 'Reply' qiling."
        )
        
        try:
            await bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
            await message.answer("✅ Xabaringiz adminga yuborildi.")
        except Exception as e:
            # Agar Markdown xato bersa, oddiy matnda yuborish
            await bot.send_message(ADMIN_ID, admin_text.replace("**", "").replace("`", ""))
            await message.answer("✅ Xabaringiz yuborildi.")

    # 2. Admin foydalanuvchiga javob yozsa (Reply qilib)
    elif message.reply_to_message:
        try:
            # Reply qilingan xabardan User_ID ni qidirib topish
            user_id_match = re.search(r"User_ID: `(\d+)`", message.reply_to_message.text)
            if not user_id_match:
                # Agar Markdown'siz xabar bo'lsa
                user_id_match = re.search(r"User_ID: (\d+)", message.reply_to_message.text)

            if user_id_match:
                target_id = int(user_id_match.group(1))
                await bot.send_message(target_id, f"**Bahriyya**💙\n\n{message.text}", parse_mode="Markdown")
                await message.answer("✅ Javobingiz foydalanuvchiga yuborildi.")
            else:
                await message.answer("❌ Xato: Foydalanuvchi ID raqami topilmadi.")
        except Exception as e:
            await message.answer(f"❌ Xatolik yuz berdi: {e}")

# --- ASOSIY QISM ---
async def main():
    keep_alive() # Serverni fonda yurgizish
    print("Bot muvaffaqiyatli ishga tushdi...")
    # skip_updates=True bot o'chib yonganida eski xabarlarga tiqilib qolmasligi uchun
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi.")
