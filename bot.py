from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TOKEN = "PON_TU_TOKEN_AQUI"

PORTFOLIO_URL = "https://fuzzylogicarg.github.io/PORTFOLIO/"
TELEGRAM_USERNAME = "@digitalwithmati"
EMAIL = "digitalwithmati@gmail.com"
WHATSAPP = "+54 223 596 0733"


def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🌐 View Portfolio", url=PORTFOLIO_URL)],
        [InlineKeyboardButton("🛠 Services", callback_data="services")],
        [InlineKeyboardButton("📩 Contact", callback_data="contact")],
        [InlineKeyboardButton("💬 Get a Quote", callback_data="quote")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "🚀 Welcome to DigitalWithMati\n\n"
        "I build landing pages, automation systems, and revenue-focused digital solutions.\n\n"
        "Choose an option:",
        reply_markup=reply_markup
    )


def button(update, context):
    query = update.callback_query
    query.answer()

    if query.data == "services":
        text = (
            "🛠 Services:\n\n"
            "• Landing Pages\n"
            "• Website Fixes\n"
            "• UI/UX Improvements\n"
            "• Automation Systems\n"
            "• Telegram Bots\n"
        )

    elif query.data == "contact":
        text = (
            "📩 Contact:\n\n"
            f"Telegram: {TELEGRAM_USERNAME}\n"
            f"Email: {EMAIL}\n"
            f"WhatsApp: {WHATSAPP}"
        )

    elif query.data == "quote":
        text = (
            "💬 Get a Quote:\n\n"
            "Send me:\n"
            "• What you need\n"
            "• Your goal\n\n"
            f"Contact me here: {TELEGRAM_USERNAME}"
        )

    keyboard = [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == "back":
        start(query, context)
    else:
        query.edit_message_text(text=text, reply_markup=reply_markup)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
