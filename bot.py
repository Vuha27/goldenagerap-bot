import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import pytz
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("BOT_TOKEN", "8127075282:AAF7BzLkeSbZuLR2DjGManTY9J4Mn8LEWU0")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", -1002126624272))  # числовий ID каналу

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Отримано команду /start")
    await update.message.reply_text("Привіт! Я готовий публікувати пости у канал!")

# --- /post <текст> ---
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Отримано команду /post")
    if context.args:
        text = " ".join(context.args)
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        await update.message.reply_text("Пост опубліковано у канал!")
    else:
        await update.message.reply_text("Введіть текст для посту після команди /post")

# --- Автоматичний пост щодня о 17:00 за Києвом ---
async def auto_post(app: Application):
    kyiv_tz = pytz.timezone('Europe/Kiev')
    while True:
        now = datetime.now(kyiv_tz)
        target = now.replace(hour=17, minute=0, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        print(f"Чекаю до {target.strftime('%Y-%m-%d %H:%M:%S')} для автопосту...")
        await asyncio.sleep(wait_seconds)
        try:
            await app.bot.send_message(chat_id=CHANNEL_ID, text="Це автоматичний пост о 17:00!")
            print("Автоматичний пост відправлено!")
        except Exception as e:
            print(f"Помилка автопосту: {e}")

# --- Основний запуск ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))
    # Запускаємо автопост у фоновому режимі
    asyncio.create_task(auto_post(app))
    print("Бот запущено!")
    app.run_polling()

if __name__ == "__main__":
    main()