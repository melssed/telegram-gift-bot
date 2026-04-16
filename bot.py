print("BOT STARTED")
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Константы (перепроверь свои ID)
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 651824873

# Словарь для хранения списка пользователей (чтобы уведомлять админа только один раз)
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Проверка: если пользователя нет в словаре, уведомляем админа
    if user_id not in users:
        username = f"@{user.username}" if user.username else "нет username"
        
        text_admin = (
            f"👤 Новый пользователь\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}\n"
            f"ID: {user.id}"
        )

        try:
            # Пытаемся получить фото профиля
            photos = await context.bot.get_user_profile_photos(user_id)
            if photos.total_count > 0:
                file_id = photos.photos[0][0].file_id
                await context.bot.send_photo(
                    ADMIN_ID,
                    photo=file_id,
                    caption=text_admin
                )
            else:
                await context.bot.send_message(ADMIN_ID, text_admin)
        except Exception as e:
            # Если возникла ошибка (например, админ заблокировал бота), просто выводим в консоль
            print(f"Ошибка при уведомлении админа: {e}")

        # Добавляем в список, чтобы не спамить админу при повторном нажатии /start
        users[user_id] = True

    # Текст приветствия для пользователя
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

# Создание приложения
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Оставляем только команду /start
    app.add_handler(CommandHandler("start", start))

    print("Бот запущен и готов к работе...")
    app.run_polling(drop_pending_updates=True)
