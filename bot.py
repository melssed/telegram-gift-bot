import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- КОНФИГУРАЦИЯ ---
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 651824873  # Твой ID

print("BOT STARTED")

# --- ОБРАБОТЧИКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ пользователю на команду /start и уведомление админу"""
    user = update.effective_user
    
    # 1. Приветствие пользователя
    text = (
        "<b>Welcome!</b> Open our Mini App to continue."
    )
    keyboard = [
        [InlineKeyboardButton("Open Mini App", url="http://t.me/PlacedMarketBot?startapp")]
    ]
    await update.message.reply_text(
        text, 
        parse_mode="HTML", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # 2. Уведомление админу о новом старте
    admin_msg = (
        f"🚀 <b>Новый старт бота!</b>\n\n"
        f"👤 Имя: {user.first_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"🔗 Юзер: @{user.username if user.username else 'нет'}"
    )
    await context.bot.send_message(ADMIN_ID, admin_msg, parse_mode="HTML")


async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылка любого текстового сообщения админу"""
    if not update.message or not update.message.text:
        return

    user = update.effective_user
    user_text = update.message.text

    # Формируем отчет для админа
    report = (
        f"📩 <b>Новое сообщение!</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 От: {user.first_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"🔗 Юзер: @{user.username if user.username else 'нет'}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💬 Текст:\n<i>{user_text}</i>"
    )

    # Отправляем админу
    await context.bot.send_message(ADMIN_ID, report, parse_mode="HTML")


# --- ЗАПУСК ---

if __name__ == "__main__":
    # Проверка токена
    if not TOKEN:
        print("ОШИБКА: Токен не найден в переменных окружения!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()

        # Команда /start
        app.add_handler(CommandHandler("start", start))

        # Любое текстовое сообщение (кроме команд) отправляется админу
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

        print("Бот успешно запущен...")
        app.run_polling(drop_pending_updates=True)
