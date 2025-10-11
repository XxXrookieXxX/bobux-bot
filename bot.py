from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет покупатель👋!\n\nСколько робуксов хочешь купить?')
    context.user_data["waiting_for_number"]=True

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Вы сказали: {update.message.text}')


ChatGPT
Вы сказали:
как сделать чтобы тг бот ожидал ввода данных а когда пользователь ввел данные то проверил если это число то например умножил на 1.43 с округлением в большую сторону вот код бота: 
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет покупатель👋!\n\nСколько робуксов хочешь купить?')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Вы сказали: {update.message.text}')

def main():
    import os
    TOKEN = os.getenv('TELEGRAM_TOKEN')  # токен берём из переменной окружения

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
ChatGPT сказал:
Хорошо 👍
Ты почти всё сделал правильно — нужно лишь немного доработать логику, чтобы бот ждал ввода числа, проверял, действительно ли это число, и затем выполнял нужное действие (например, умножал на 1.43 и округлял в большую сторону).

Вот полностью рабочий пример:

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import math
import os


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет покупатель👋!\n\nСколько робуксов хочешь купить?\n(Введи только число)"
    )
    # сохраняем состояние ожидания числа
    context.user_data["waiting_for_number"] = True


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Проверяем, ожидаем ли мы число от пользователя
    if context.user_data.get("waiting_for_number"):
        try:
            number = float(text)
            result = math.ceil(number * 1.43)
            await update.message.reply_text(
                f"Тогда вам необходимо создать геймпасс на сумму: {result} робуксов!"
            )

            # Можно сбросить состояние, если больше не ждём ввод
            context.user_data["waiting_for_number"] = False

        except ValueError:
            await update.message.reply_text(
                "❌ Пожалуйста, введи корректное число (например: 100)"
            )
    else:
        await update.message.reply_text("Напиши /start, чтобы начать сначала 😊")
def main():
    import os
    TOKEN = os.getenv('TELEGRAM_TOKEN')  # токен берём из переменной окружения

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
