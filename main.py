import os
import asyncio
from telegram.ext import Application, CommandHandler
import telegram
from apscheduler.schedulers.background import BackgroundScheduler

# Get token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 7022402755  # Your Telegram user ID

# --- Handlers ---
async def start(update, context):
    await update.message.reply_text("👋 Hello! CaseAlert AI bot is running.")

# --- Startup notification ---
async def notify_owner():
    bot = telegram.Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=OWNER_ID, text="✅ CaseAlert AI bot is live on Render!")

# --- Heartbeat ---
async def send_heartbeat():
    bot = telegram.Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=OWNER_ID, text="✅ CaseAlert AI is alive and running on Render")

def schedule_heartbeat():
    scheduler = BackgroundScheduler()
    # 9:00 AM IST = 03:30 UTC
    scheduler.add_job(lambda: asyncio.run(send_heartbeat()), 'cron', hour=3, minute=30)
    scheduler.start()

# --- Main ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Schedule heartbeat
    schedule_heartbeat()

    # Send startup notification
    asyncio.run(notify_owner())

    print("🚀 CaseAlert AI main bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
