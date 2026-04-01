import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8227795621:AAEqrG82J5h8WSgYVYrM63Z7YCRGKgA5lQw"

PORTFOLIO_URL = "https://fuzzylogicarg.github.io/PORTFOLIO/"
TELEGRAM_USERNAME = "@digitalwithmati"
EMAIL = "digitalwithmati@gmail.com"
WHATSAPP = "+54 223 596 0733"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

WELCOME_TEXT = (
    "🚀 *Welcome to DigitalWithMati*\n\n"
    "I build landing pages, website improvements, automation systems, "
    "and conversion-focused digital solutions.\n\n"
    "Choose an option below."
)

SERVICES_TEXT = (
    "🛠 *Services*\n\n"
    "• Landing Pages\n"
    "• Website Fixes\n"
    "• UI/UX Improvements\n"
    "• Automation Ideas\n"
    "• Telegram Bot Setups\n"
    "• Conversion-Focused Pages"
)

CONTACT_TEXT = (
    "📩 *Contact*\n\n"
    f"Telegram: {TELEGRAM_USERNAME}\n"
    f"Email: {EMAIL}\n"
    f"WhatsApp: {WHATSAPP}"
)

QUOTE_TEXT = (
    "💬 *Get a Quote*\n\n"
    "Send me a short description of your project:\n\n"
    "• What you need\n"
    "• Your goal\n"
    "• If you already have a website or idea\n\n"
    "You can contact me directly here:\n"
    f"{TELEGRAM_USERNAME}"
)


def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🌐 View Portfolio", url=PORTFOLIO_URL)],
        [InlineKeyboardButton("🛠 Services", callback_data="services")],
        [InlineKeyboardButton("📩 Contact", callback_data="contact")],
        [InlineKeyboardButton("💬 Get a Quote", callback_data="quote")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            WELCOME_TEXT,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    if query.data == "services":
        await query.edit_message_text(
            SERVICES_TEXT,
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )
    elif query.data == "contact":
        await query.edit_message_text(
            CONTACT_TEXT,
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )
    elif query.data == "quote":
        await query.edit_message_text(
            QUOTE_TEXT,
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )
    elif query.data == "back":
        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )


def run_bot() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()