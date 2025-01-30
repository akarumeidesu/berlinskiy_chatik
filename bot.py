import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение."""
    await update.message.reply_text("Привет! Я бот, который собирает последние 5 сообщений.")

async def get_last_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Читает последние 5 сообщений из чата и отправляет их в ответ."""
    chat_id = update.message.chat_id

    try:
        # Получаем последние 5 сообщений из чата
        messages = await context.bot.get_chat_history(chat_id=chat_id, limit=5)

        # Собираем текст сообщений
        response = "\n".join([
            f"{msg.from_user.username or msg.from_user.first_name}: {msg.text}"
            for msg in reversed(messages) if msg.text  # Игнорируем сообщения без текста
        ])

        # Отправляем собранный текст в чат
        if response:
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("Нет текстовых сообщений для отображения.")
    except Exception as e:
        logger.error(f"Ошибка при получении истории сообщений: {e}")
        await update.message.reply_text("Не удалось получить последние сообщения.")

def main() -> None:
    """Запуск бота."""
    # Получаем токен из переменной окружения
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN environment variable found!")
        exit(1)

    application = Application.builder().token(token).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_last_messages", get_last_messages))

    # Запуск бота через длинные опросы
    application.run_polling()

if __name__ == '__main__':
    main()
