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
                    InlineKeyboardButton("🔁 Ввести сумму заново", callback_data="again"),
                    InlineKeyboardButton("ℹ️ Как создать геймпасс", callback_data="help"),
                ],
                [
                    InlineKeyboardButton("🏠 Главное меню", callback_data="menu"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"Теперь вам необходимо создать геймпасс на сумму: {result} робуксов!",
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
        await query.edit_message_text("Хорошо! Введите сумму робуксов которую хотите купить 👇")
        context.user_data["waiting_for_number"] = True

    elif query.data == "help":
        await query.edit_message_text(
            "📖 Инструкция по созданию геймпасса в роблокс:\n\nШаг 1: Откройте сайт роблокса roblox.com\nШаг 2: В верхней панели выберите «Create» или «Создать»\nШаг 3: Выберите свою игру\nШаг 4: Нажмите на 3 полоски сверху слева и в списке выберите во вкладке «Monetization» или «Монетизация» выберите «Passes» или «Пропуска» или «Проходит»\nШаг 5: Нажмите на синюю кнопку «Create A Pass» или «Создать Пропуск»\nШаг 6: Вводите имя геймпасса и нажимаете снизу на синюю кнопку\nШаг 7: На странице в списке находите свой геймпасс и нажимаете на его название\nШаг 8: Нажмите слева сверху на 3 полоски и выберите в списке «Sales» или «Продажи»\nШаг 9: Включите опцию «Item for sale» или «Товар на продажу» и установите цену, которую я указал и нажмите на синюю кнопку\nШаг 10: Нажмите на 3 полоски сверху слева и затем на 3 точки справа названия геймпасса, затем на кнопку которая появилась и в конце введите скопированный номер\n\nПо отдельным вопросам обращаться к продавцу!"
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
