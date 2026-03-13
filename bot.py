from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from gift_sender import send_gift

TOKEN = "8332166589:AAH_jwVBhFdQ3O9L4ip7GNlx_0vRbQHv6zs"
ALLOWED_USER = 7708695143
ADMIN_ID = 651824873

users = {}

GIFT_LIST = "<blockquote>🎄🎅 <code>5922558454332916696</code>\n🧸🎅 <code>5956217000635139069</code>\n🧸❤️ <code>5800655655995968830</code>\n🧸💐 <code>5866352046986232958</code></blockquote>"

async def start(update, context):

    user = update.effective_user
    user_id = user.id

    # если пользователь новый — отправляем уведомление
    if user_id not in users:

        await context.bot.send_message(
            ADMIN_ID,
            f"👤 Новый пользователь\n\n"
            f"Username: @{user.username}\n"
            f"ID: {user.id}"
        )

        users[user_id] = {}

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
    
async def check_user(update):
    if update.effective_user.id != ALLOWED_USER:
        return False
    return True


async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_user(update):
        return

    users[update.effective_user.id] = {"step": "form"}

    await update.message.reply_text(
        f"Fill in the Data\n\n{GIFT_LIST}\n\nGift ID\nUsername",
        parse_mode="HTML"
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in users:
        return

    data = users[user_id]

    if data["step"] == "form":

        lines = text.split("\n")

        if len(lines) < 2:
            await update.message.reply_text("Нужно отправить:\nID\nusername")
            return

        gift_id = lines[0].strip()
        username = lines[1].strip()

        data["gift_id"] = gift_id
        data["username"] = username
        data["step"] = "confirm"

        await update.message.reply_text(
            f"Форма отправки:\n\n"
            f"ID подарка: `{gift_id}`\n"
            f"Получатель: {username}\n\n"
            f"/confirm для отправки\n"
            f"/cancel для отмены",
            parse_mode="Markdown"
        )


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_user(update):
        return

    user_id = update.effective_user.id

    if user_id not in users:
        return

    data = users[user_id]

    if data["step"] != "confirm":
        return

    data["step"] = "sending"

    gift_id = data["gift_id"]
    username = data["username"]

    await update.message.reply_text("Подарок отправляется...")

    result = await send_gift(gift_id, username)

    if result:
        await update.message.reply_text("✅ Подарок успешно отправлен")
    else:
        await update.message.reply_text("❌ Ошибка отправки подарка")

    users.pop(user_id)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_user(update):
        return

    user_id = update.effective_user.id

    if user_id in users:
        users.pop(user_id)

    await update.message.reply_text("❌ Отправка отменена")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gift", gift))
app.add_handler(CommandHandler("confirm", confirm))
app.add_handler(CommandHandler("cancel", cancel))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

app.run_polling(drop_pending_updates=True)