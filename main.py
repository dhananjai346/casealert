from scraper import get_case_updates
from payments import handle_payment

print("🚀 CaseAlert AI main bot started")

# Placeholder main loop
if __name__ == "__main__":
    print("Bot is ready. This would connect to Telegram and start the bot.")
from apscheduler.schedulers.background import BackgroundScheduler
import telegram
import asyncio

OWNER_ID = 7022402755  # your Telegram user ID

async def send_heartbeat():
    bot = telegram.Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=OWNER_ID, text="✅ CaseAlert AI is alive and running on Render")

def schedule_heartbeat():
    scheduler = BackgroundScheduler()
    # Send heartbeat every day at 9:00 AM IST
    scheduler.add_job(lambda: asyncio.run(send_heartbeat()), 'cron', hour=3, minute=30)
    # Note: Render server is in UTC, so 03:30 UTC = 09:00 IST
    scheduler.start()

schedule_heartbeat()
