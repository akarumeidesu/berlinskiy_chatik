import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Максимальное количество сообщений для хранения
MAX_MESSAGES = 5

# Хранилище сообщений
messages_store = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение."""
    await update.message.reply_text("Привет! Я бот, который собирает последние 5 сообщений.")

async def get_last_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет последние 5 сообщений."""
    if not messages_store:
        await update.message.reply_text("Нет сохраненных сообщений.")
        return
    
    response = "\n".join([f"{msg['from_user']}: {msg['text']}" for msg in messages_store])
    await update.message.reply_text(response or "Нет сохраненных сообщений.")

async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сохраняет сообщение в хранилище."""
    message = update.message
    if message.text:
        messages_store.append({
            'from_user': message.from_user.username or message.from_user.first_name,
            'text': message.text
        })
        
        # Ограничение количества сообщений до MAX_MESSAGES
        if len(messages_store) > MAX_MESSAGES:
            messages_store.pop(0)

def main(token: str) -> None:
    """Запуск бота."""
    application = Application.builder().token(token).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lastmessages", get_last_messages))

    # Регистрация обработчика всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_message))

    # Запуск бота через длинные опросы
    application.run_polling()

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN environment variable found!")
        exit(1)
    main(token)
