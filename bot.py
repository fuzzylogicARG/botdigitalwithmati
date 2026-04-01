import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
PORTFOLIO_URL = "https://fuzzylogicarg.github.io/PORTFOLIO/"
TELEGRAM_USERNAME = "@digitalwithmati"
EMAIL = "digitalwithmati@gmail.com"
WHATSAPP_URL = "https://wa.me/5492235960733"
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

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
    "• Automation Systems\n"
    "• Telegram Bots\n"
    "• Conversion-Focused Pages"
)

CONTACT_TEXT = (
    "📩 *Contact*\n\n"
    f"Telegram: {TELEGRAM_USERNAME}\n"
    f"Email: {EMAIL}\n"
    "WhatsApp: Use the button below"
)

QUOTE_TEXT = (
    "💬 *Get a Quote*\n\n"
    "Send me a short description of your project:\n\n"
    "• What you need\n"
    "• What your goal is\n"
    "• If you already have a website or idea\n\n"
    "Then contact me directly through Telegram or WhatsApp."
)

ABOUT_TEXT = (
    "🌐 *DigitalWithMati*\n\n"
    "I help brands and businesses build stronger digital systems:\n"
    "websites, landing pages, automation, UX improvements, and revenue-focused solutions."
)


def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🌐 View Portfolio", url=PORTFOLIO_URL)],
        [InlineKeyboardButton("🛠 Services", callback_data="services")],
        [InlineKeyboardButton("📩 Contact", callback_data="contact")],
        [InlineKeyboardButton("💬 Get a Quote", callback_data="quote")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)


def contact_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("💬 WhatsApp", url=WHATSAPP_URL)],
        [InlineKeyboardButton("📨 Email", url=f"mailto:{EMAIL}")],
        [InlineKeyboardButton("🌐 Portfolio", url=PORTFOLIO_URL)],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


def quote_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("💬 Contact on WhatsApp", url=WHATSAPP_URL)],
        [InlineKeyboardButton("🌐 View Portfolio", url=PORTFOLIO_URL)],
        [InlineKeyboardButton("⬅ Back to Menu", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def send_welcome_message(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as logo_file:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=logo_file,
                caption=WELCOME_TEXT,
                reply_markup=main_menu(),
                parse_mode="Markdown"
            )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=WELCOME_TEXT,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await send_welcome_message(update.message.chat_id, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Use /start to open the DigitalWithMati menu.",
            parse_mode="Markdown"
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    if query.data == "services":
        await query.message.reply_text(
            SERVICES_TEXT,
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )

    elif query.data == "contact":
        await query.message.reply_text(
            CONTACT_TEXT,
            reply_markup=contact_menu(),
            parse_mode="Markdown"
        )

    elif query.data == "quote":
        await query.message.reply_text(
            QUOTE_TEXT,
            reply_markup=quote_menu(),
            parse_mode="Markdown"
        )

    elif query.data == "about":
        await query.message.reply_text(
            ABOUT_TEXT,
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )

    elif query.data == "back":
        await query.message.reply_text(
            WELCOME_TEXT,
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error("Exception while handling an update:", exc_info=context.error)


def main() -> None:
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
