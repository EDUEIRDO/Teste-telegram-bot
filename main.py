import logging
from telegram import Update
from telegram.ext import CallbackContext, ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
import random, qrcode
from io import BytesIO

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="O fafoso ta na área!!,\n/start inicia o sistema,\n/caps transforma um texto em maiusculo,\n/caps_low transforma um texto em minusculo,\n/meme envia um meme aleatorio,\n/qrcode gera um qrcode com o link inserido da seguinte forma /qrcode exemplo.com")

async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def caps_low(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_low = ''.join(context.args).lower()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_low)

async def meme(update: Update, context: CallbackContext):
    meme_url = 'https://ichef.bbci.co.uk/news/976/cpsprodpb/16620/production/_91408619_55df76d5-2245-41c1-8031-07a4da3f313f.jpg'
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=meme_url)

async def qrcode_create(update: Update, context: CallbackContext):
    link_get = ''.join(context.args)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(link_get)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = BytesIO()
    bio.name = 'qrcode.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=bio)


if __name__ == '__main__':
    application = ApplicationBuilder().token('MY_TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    teste_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), teste)
    meme_handler = CommandHandler('meme', meme)
    caps_handler = CommandHandler('caps', caps)
    qrcode_handler = CommandHandler('qrcode', qrcode_create)
    
    application.add_handler(start_handler)
    application.add_handler(teste_handler)
    application.add_handler(meme_handler)
    application.add_handler(caps_handler)
    application.add_handler(qrcode_handler)
    
    application.run_polling()
