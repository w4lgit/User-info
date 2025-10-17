from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import json
import os
import datetime

TOKEN = "88424718692:AAHG4NE2dVTh8WygAIaxzzfsZsGsl1SYWJ8"
USER_DATA_FILE = "users.json"

# ایجاد فایل کاربری در صورت عدم وجود
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

def save_user(user):
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data[str(user.id)] = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "joined": datetime.datetime.now().isoformat()
    }
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# زبان‌ها
MESSAGES = {
    "fa": {
        "welcome": "👋 سلام {name}!\n\n🆔 ID: `{id}`\n💬 Username: @{username}\n📛 Name: {full_name}\n📅 Joined: {joined}",
        "help": "📌 دستورات موجود:\n/start - شروع ربات و نمایش اطلاعات کاربر\n/help - نمایش این راهنما\n/info - دریافت اطلاعات بیشتر",
        "profile_info": "💼 این کارت پروفایل توست:"
    },
    "en": {
        "welcome": "👋 Hello {name}!\n\n🆔 ID: `{id}`\n💬 Username: @{username}\n📛 Name: {full_name}\n📅 Joined: {joined}",
        "help": "📌 Available commands:\n/start - start bot and show your info\n/help - show this guide\n/info - get more info",
        "profile_info": "💼 This is your profile card:"
    }
}

# انتخاب زبان کاربر (فعلاً بر اساس فارسی یا انگلیسی ساده)
def get_lang(user_id):
    # اینجا می‌تونی سیستم تشخیص زبان پیشرفته اضافه کنی
    return "fa"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user)
    lang = get_lang(user.id)
    msg = MESSAGES[lang]["welcome"].format(
        name=user.first_name,
        id=user.id,
        username=user.username if user.username else "نداره",
        full_name=f"{user.first_name} {user.last_name if user.last_name else ''}",
        joined=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    keyboard = [
        [InlineKeyboardButton("💡 Help / راهنما", callback_data='help')],
        [InlineKeyboardButton("🌐 Visit Website", url='https://example.com')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update.effective_user.id)
    await update.message.reply_text(MESSAGES[lang]["help"])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_lang(query.from_user.id)
    if query.data == 'help':
        await query.message.reply_text(MESSAGES[lang]["help"])

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_lang(user.id)
    msg = MESSAGES[lang]["profile_info"] + "\n"
    msg += f"👤 Name: {user.first_name} {user.last_name if user.last_name else ''}\n"
    msg += f"🆔 ID: {user.id}\n"
    msg += f"💬 Username: @{user.username if user.username else 'نداره'}"
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("info", info_command))
app.add_handler(CallbackQueryHandler(button_handler))

print("ربات جهانی حرفه‌ای روشن شد ✅")
app.run_polling()
