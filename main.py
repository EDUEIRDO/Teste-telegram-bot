import asyncio
import logging
from telegram import Update
from telegram.ext import CallbackContext, ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
import random, qrcode
import _asyncio
from io import BytesIO
from pytube import YouTube

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="O fafoso ta na área!!,\n/start inicia o sistema,\n/caps transforma um texto em maiusculo,\n/caps_low transforma um texto em minusculo,\n/all_image envia uma imagem aleatoria,\n/qrcode gera um qrcode com o link inserido da seguinte forma /qrcode exemplo.com,\n/music para baixar uma música")

async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def caps_low(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_low = ''.join(context.args).lower()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_low)

async def all_image(update: Update, context: CallbackContext):
    t1 = random.randint(0, 1000)
    t2 = random.randint(0, 1000)
    meme_url = f'https://picsum.photos/{t1}/{t2}'
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

async def music(update: Update, context: CallbackContext):
    link_get = ''.join(context.args)
    url = YouTube(link_get)
    
    try:
        stream = url.streams.get_audio_only()
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=stream.url)
    except TimeoutError:
        await asyncio.sleep(5)
        await music(update, context)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ocorreu um erro: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token('My-token').build()
    
    start_handler = CommandHandler('start', start)
    teste_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), teste)
    all_image_handler = CommandHandler('all_image', all_image)
    caps_handler = CommandHandler('caps', caps)
    qrcode_handler = CommandHandler('qrcode', qrcode_create)
    music_handler = CommandHandler('music', music)
    
    application.add_handler(start_handler)
    application.add_handler(teste_handler)
    application.add_handler(all_image_handler)
    application.add_handler(caps_handler)
    application.add_handler(qrcode_handler)
    application.add_handler(music_handler)
    
    application.run_polling()
