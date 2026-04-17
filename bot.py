import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- SETTINGS ---
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 651824873 

print("BOT STARTED")

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    text = (
        "<b>Welcome!</b> Open a "
        "<b><a href='https://t.me/PlacedMarketBot'>Mini Application</a></b> "
        "to bought <b>Telegram Stars</b> and more"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "Open the Placed Market Application",
                url="http://t.me/PlacedMarketBot?startapp"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup,
        protect_content=True
    )

    admin_log = (
        f"🚀 <b>New bot start!</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 Name: {user.first_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"🔗 Username: @{user.username if user.username else 'none'}"
    )
    await context.bot.send_message(ADMIN_ID, admin_log, parse_mode="HTML")


async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text or update.effective_user.id == ADMIN_ID:
        return

    user = update.effective_user
    user_text = update.message.text

    report = (
        f"📩 <b>Message from user</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 From: {user.first_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"🔗 Username: @{user.username if user.username else 'none'}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💬 Text:\n<i>{user_text}</i>"
    )

    await context.bot.send_message(ADMIN_ID, report, parse_mode="HTML")


# --- RUN BOT ---

if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: TOKEN not set in Railway variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

        print("Bot successfully started and ready.")
        app.run_polling(drop_pending_updates=True)