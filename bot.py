import re
import logging
import qrcode
import os

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="ready to receive forests")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    message = update.message.text

    url = re.search("(?P<url>https?://[^\s]+)", message)
    if not url:
        url = "Sorry, this is not a proper forest message"
    else:
        url = url.group("url")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,)
        qr.add_data(url)

        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("url.png")

        url = "updated qr code"
    await update.message.reply_text(url)


if __name__ == '__main__':
    application = ApplicationBuilder().token(f'{os.environ[TELEGRAM_TOKEN]}').build()
    
    start_handler = CommandHandler('start', start)
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()
