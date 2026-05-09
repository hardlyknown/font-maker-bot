from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters, InlineQueryHandler
import uuid

BOT_TOKEN = "8205845727:AAHlggh1CNUesoTSd6NIEkUx98IgRRk9cmk"

# Small caps font map
FONT_MAP = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ',
    'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ',
    'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ',
    'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
    'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ',
    'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
    'y': 'ʏ', 'z': 'ᴢ'
}

FOOTER = "ᴍᴀᴅᴇ ʙʏ @ʜᴀʀᴅʟʏ_ᴋɴᴏᴡɴ"

def convert_font(text: str) -> str:
    return "".join(FONT_MAP.get(c.lower(), c) for c in text)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_text = (
        "Welcome to the Made Font Converter Bot\n\n"
        "Send any normal text and get it converted "
        "into a clean and stylish made font instantly.\n\n"
        "Fast • Clean • Professional"
    )
    converted_intro = convert_font(intro_text)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/hardly_known")]
    ])

    await update.message.reply_text(
        converted_intro,
        reply_markup=keyboard
    )

# Normal message conversion with Copy button
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    converted = convert_font(text)

    message = f"✨ Converted Text ✨\n\n{converted}\n\n──────────────\n{FOOTER}"

    # Copy button (text auto-filled in chat input)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Copy", switch_inline_query_current_chat=converted)]
    ])

    await update.message.reply_text(
        message,
        reply_markup=keyboard
    )

# Inline query handler
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    converted = convert_font(query) + f"\n\n{FOOTER}"

    result = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Convert to Made Font",
            input_message_content=InputTextMessageContent(converted),
            description="Send MADE FONT version"
        )
    ]

    await update.inline_query.answer(result, cache_time=1)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert))
    app.add_handler(InlineQueryHandler(inline_query))

    print("🤖 Bot with Inline Mode & Copy Button is running...")
    app.run_polling()

if __name__ == "__main__":
    main()