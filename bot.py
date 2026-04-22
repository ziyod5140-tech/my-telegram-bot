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
@dp.message()
async def handle_messages(message: types.Message):
    # Agar xabar Admindan kelmagan bo'lsa (ya'ni foydalanuvchi yozsa)
    if message.from_user.id != ADMIN_ID:
        # Username bor yoki yo'qligini tekshirish
        user_name = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
        
        # Siz xohlagan chiroyli format (rasmdagidek)
        admin_message = (
            f"📩 **Yangi xabar!**\n"
            f"👤 **Ism:** {message.from_user.full_name}\n"
            f"🆔 **User_ID:** `{message.from_user.id}`\n"
            f"🔗 **Username:** {user_name}\n"
            f"------------------------------\n"
            f"💬 **Xabar:** {message.text}\n"
            f"------------------------------\n"
            f"Javob berish uchun xabarga <<Reply>> qiling."
        )
        
        # Adminga yuborish
        await bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")
        # Foydalanuvchiga tasdiq xabari
        await message.answer("✅ Javobingiz yuborildi.")

    # Agar Admin foydalanuvchiga javob yozsa (Reply qilsa)
    elif message.reply_to_message:
        try:
            # Xabar ichidan User_ID ni qidirib topish
            import re
            match = re.search(r"User_ID: `(\d+)`", message.reply_to_message.text)
            if match:
                user_id = int(match.group(1))
                # Foydalanuvchiga admin javobini yuborish
                await bot.send_message(chat_id=user_id, text=f"**Bahriyya**💙\n\n{message.text}", parse_mode="Markdown")
                await message.answer("✅ Javob yuborildi.")
            else:
                await message.answer("⚠️ Javob berish uchun 'Reply' qiling.")
        except Exception as e:
            await message.answer(f"❌ Xatolik yuz berdi: {e}")
async def main():
    keep_alive() # Serverni ishga tushirish
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
