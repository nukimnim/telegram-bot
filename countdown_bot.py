from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import asyncio
import os
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Вставьте ваш токен
TOKEN = '6809926186:AAEMjgK_A02EY30rU1neAJuiRboaY96dGAc'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Команда /start получена от пользователя %s", update.effective_user.username)
    await update.message.reply_text('Привет! Введи /countdown для начала.')

async def countdown_task(update: Update, context: ContextTypes.DEFAULT_TYPE, target_date: datetime) -> None:
    message = await update.message.reply_text("Запуск...")

    while True:
        current_date = datetime.now()
        delta = target_date - current_date

        if delta.total_seconds() <= 0:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message.message_id,
                text="я приехала, сучка!"
            )

            # Укажите путь к вашему GIF-файлу
            gif_path = r'c:\Users\Аня\OneDrive\Documents\illusion\animation.gif.gif'

            if not os.path.exists(gif_path):
                await update.message.reply_text("GIF файл не найден.")
                logger.error("GIF файл не найден по пути: %s", gif_path)
                break

            try:
                with open(gif_path, 'rb') as gif_file:
                    await context.bot.send_animation(
                        chat_id=update.effective_chat.id,
                        animation=gif_file
                    )
            except Exception as e:
                await update.message.reply_text(f"Ошибка при отправке GIF: {e}")
                logger.error("Ошибка при отправке GIF: %s", e)

            break

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        countdown_message = f'{days} дней, {hours} часов, {minutes} минут и {seconds} секунд.'

        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text=countdown_message
        )

        await asyncio.sleep(1)  # Обновление каждую секунду

async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Команда /countdown получена от пользователя %s", update.effective_user.username)
    target_date = datetime(2024, 7, 3, 12, 0, 0)  # Целевая дата
    asyncio.create_task(countdown_task(update, context, target_date))

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("countdown", countdown))

    logger.info("Запуск бота")
    app.run_polling()

if __name__ == '__main__':
    main()