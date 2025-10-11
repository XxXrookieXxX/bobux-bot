from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
import math
import os


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет покупатель👋!\n\nСколько робуксов хочешь купить?\n(Введи только число)"
    )
    context.user_data["waiting_for_number"] = True


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if context.user_data.get("waiting_for_number"):
        try:
            number = float(text)
            result = math.ceil(number * 1.43)

            # создаем меню после обработки числа
            keyboard = [
                [
                    InlineKeyboardButton("🔁 Посчитать снова", callback_data="again"),
                    InlineKeyboardButton("ℹ️ Помощь", callback_data="help"),
                ],
                [
                    InlineKeyboardButton("🏠 Главное меню", callback_data="menu"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"💰 После умножения на 1.43 и округления вверх получается: {result}",
                reply_markup=reply_markup,
            )

            context.user_data["waiting_for_number"] = False

        except ValueError:
            await update.message.reply_text("❌ Введи корректное число (например: 100)")
    else:
        await update.message.reply_text("Напиши /start, чтобы начать 😊")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки."""
    query = update.callback_query
    await query.answer()  # обязательно, чтобы Telegram не показывал «загрузка...»

    if query.data == "again":
        await query.edit_message_text("Хорошо! Введи новое число 👇")
        context.user_data["waiting_for_number"] = True

    elif query.data == "help":
        await query.edit_message_text(
            "📖 Просто введи число — я умножу его на 1.43 и округлю вверх.\n\n"
            "Например: 100 → 143"
        )

    elif query.data == "menu":
        await query.edit_message_text(
            "🏠 Главное меню:\n"
            "— /start чтобы начать заново\n"
            "— Введи число для расчета\n"
            "— Или воспользуйся кнопками 👇"
        )


def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
