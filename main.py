import os
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import telegram
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 7022402755  # your Telegram user ID

# Simple database in memory (replace with real DB later)
users = {}

# --- Handlers ---
async def start(update, context):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"alerts_used": 0, "upgraded": False}
    await update.message.reply_text(
        "👋 Welcome to CaseAlert AI!\n\n"
        "🎁 You get 2 free case alerts.\n"
        "After that, upgrade for just ₹199/month.\n\n"
        "Type /getalert to receive your case update."
    )

async def get_alert(update, context):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"alerts_used": 0, "upgraded": False}

    if users[user_id]["upgraded"]:
        await update.message.reply_text("📜 [PAID] Your case update: (dummy data for now).")
    else:
        if users[user_id]["alerts_used"] < 2:
            users[user_id]["alerts_used"] += 1
            await update.message.reply_text(f"📜 [FREE] Your case update #{users[user_id]['alerts_used']}.")
            if users[user_id]["alerts_used"] == 2:
                await update.message.reply_text(
                    "⚠️ You’ve used your 2 free alerts!\n\n"
                    "💳 Upgrade now for ₹199/month.\n"
                    "UPI ID: 7795125704@ptyes\n\n"
                    "After payment, send screenshot to admin."
                )
        else:
            await update.message.reply_text(
                "❌ Free trial ended!\n\n"
                "💳 Please upgrade for ₹199/month.\n"
                "UPI ID: 7795125704@ptyes"
            )

async def upgrade(update, context):
    await update.message.reply_text(
        "💳 To upgrade, pay ₹199/month via UPI:\n"
        "UPI ID: 7795125704@ptyes\n\n"
        "After payment, send screenshot to admin."
    )

# --- Broadcast (Owner only) ---
async def broadcast(update, context):
    if update.effective_user.id != OWNER_ID:
        return
    message = " ".join(context.args)
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 Broadcast:\n{message}")
        except:
            pass
    await update.message.reply_text("✅ Broadcast sent!")

# --- Startup & Heartbeat ---
async def notify_owner():
    bot = telegram.Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=OWNER_ID, text="✅ CaseAlert AI bot is live with marketing funnel!")

async def send_heartbeat():
    bot = telegram.Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=OWNER_ID, text="✅ CaseAlert AI heartbeat check — still running.")

def schedule_heartbeat():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(send_heartbeat()), 'cron', hour=3, minute=30)  # 9 AM IST
    scheduler.start()

# --- Main ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getalert", get_alert))
    app.add_handler(CommandHandler("upgrade", upgrade))
    app.add_handler(CommandHandler("broadcast", broadcast))

    schedule_heartbeat()
    asyncio.run(notify_owner())

    print("🚀 CaseAlert AI bot with marketing started")
    app.run_polling()

if __name__ == "__main__":
    main()
