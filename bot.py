from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests

def get_usd_rate():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url).json()
    return response["Valute"]["USD"]["Value"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет покупатель👋!\n\nДля взаимодействия с ботом используйте следующие команды:\n/start — Начать диалог\n/usd — Курс доллара')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Вы сказали: {update.message.text}')

async def usd(update, context):
    rate = get_usd_rate()
    await update.message.reply_text(f"💵 По данным Центробанка РФ, курс доллара: {rate:.2f} руб.")

def main():
    import os
    TOKEN = os.getenv('TELEGRAM_TOKEN')  # токен берём из переменной окружения

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('usd',usd))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
