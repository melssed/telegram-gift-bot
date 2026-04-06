print("BOT STARTED")
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from gift_sender import send_gift

import os

TOKEN = os.getenv("TOKEN")
ALLOWED_USER = 7708695143
ADMIN_ID = 651824873

users = {}

GIFT_LIST = "<blockquote>🎄🎅 <code>5922558454332916696</code>\n🧸🎅 <code>5956217000635139069</code>\n🧸❤️ <code>5800655655995968830</code>\n🧸💐 <code>5866352046986232958</code></blockquote>"

async def start(update, context):

    user = update.effective_user
    user_id = user.id

    if user_id not in users:

        username = f"@{user.username}" if user.username else "нет username"

        text_admin = (
            f"👤 Новый пользователь\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}\n"
            f"ID: {user.id}"
        )

        photos = await context.bot.get_user_profile_photos(user_id)

        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id

            await context.bot.send_photo(
                ADMIN_ID,
                photo=file_id,
                caption=text_admin
            )
        else:
            await context.bot.send_message(
                ADMIN_ID,
                text_admin
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


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка, что команду вызвал админ
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ У вас нет доступа к этой команде.")
        return

    # Формируем текст с жирными синими ссылками
    text = (
        "<b>Your</b> order has been <b>completed!</b> 🪪\n\n"
        "<b><a href='tg://stars'>100 Telegram Stars</a></b> were sent to your "
        "<b><a href='tg://settings'>account</a></b>, <b>check</b> the "
        "<b><a href='tg://stars'>balance</a></b>"
    )

    # Клавиатура с двумя кнопками в один ряд
    keyboard = [
        [
            InlineKeyboardButton("Check Balance", url="tg://stars"),
            InlineKeyboardButton("Check the Chat", url="https://t.me/PlacedRelayer")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup,
        protect_content=True,
        link_preview_options=None  # предпросмотр ссылки не скрыт (стандартное поведение)
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gift", gift))
app.add_handler(CommandHandler("confirm", confirm))
app.add_handler(CommandHandler("cancel", cancel))
app.add_handler(CommandHandler("test", test))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))


app.run_polling(drop_pending_updates=True)
