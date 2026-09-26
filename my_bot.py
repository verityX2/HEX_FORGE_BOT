# ===== بخش ۱: import ها =====
import os
from pathlib import Path
from dotenv import load_dotenv
import pyrobale
from pyrobale.objects import Message, InlineKeyboardMarkup, CopyTextButton, InputFile
from pyrobale.objects.enums import UpdatesTypes
import sqlite3

# ===== بخش ۲: تنظیمات اولیه =====
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
token = os.getenv("BOT_TOKEN")

client = pyrobale.Client(token)

# ===== بخش ۳: دیتابیس (اختیاری) =====
conn = sqlite3.connect("bot_data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# ===== بخش ۴: دستور /start با دکمه شیشه‌ای =====
@client.on_command("start")
async def start(message: Message):
    # ذخیره کاربر توی دیتابیس
    if message.user:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (message.user.id, message.user.username)
        )
        conn.commit()
    
    # ساخت دکمه‌ها
    buttons = InlineKeyboardMarkup()
    buttons.add_button("🌐 وبسایت", url="https://pyrobale.ir")
    buttons.add_button("📋 کپی", copy_text_button=CopyTextButton("متن کپی شده"))
    buttons.add_row()
    buttons.add_button("🔘 دکمه تست", callback_data="my_callback")
    
    await message.reply("سلام! خوش اومدی 👋\nیه دکمه انتخاب کن:", reply_markup=buttons)

# ===== بخش ۵: هندل کردن دکمه‌ها =====
@client.on_callback_query()
async def callback(callback_query):
    await callback_query.answer("کلیک شد!")

# ===== بخش ۶: Echo (پاسخ به پیام‌های متنی) =====
@client.on_message()
async def echo(message: Message):
    if message.text and not message.text.startswith("/"):
        await message.reply(message.text)

# ===== بخش ۷: ارسال عکس (دستور /photo) =====
@client.on_command("photo")
async def send_photo(message: Message):
    # از file_id یا آدرس استفاده کن
    await message.reply_photo("FILE_ID_HERE", caption="این یه عکسه")

# ===== بخش ۸: مکالمه (دستور /name) =====
@client.on_command("name")
async def ask_name(message: Message):
    await message.reply("اسمت چیه؟")
    
    answer = await client.wait_for(
        UpdatesTypes.MESSAGE,
        lambda upd: upd.user.id == message.user.id and bool(upd.text)
    )
    await answer.reply(f"خوشحالم {answer.text}! 👋")

# ===== بخش ۹: اجرای ربات =====
client.run()