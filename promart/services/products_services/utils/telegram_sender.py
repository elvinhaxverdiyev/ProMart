import logging
from telegram import Bot

logger = logging.getLogger(__name__)

# Telegram parametrləri
TELEGRAM_BOT_TOKEN = "7907258912:AAGdsNeXDT2GmccYnYETFhBXFzO-G9ctNkE"
TELEGRAM_CHANNEL_ID = "-1002254100433"

# Asinxron mesaj göndərmə funksiyası
async def send_product_to_telegram(product):
    """
    Məhsul məlumatlarını Telegram kanalına göndərir.
    
    :param product: Yaradılan məhsul obyektinin məlumatları
    """
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        message = (
            f"🔔 *Yeni Məhsul Əlavə Olundu!*\n\n"
            f"🏷️ *Məhsulun Adı*: {product.name}\n"
            f"📝 *Təsvir*: {product.description}\n"
            f"💰 *Qiymət*: {product.price} AZN\n"
            f"📦 *Stok Miqdarı*: {product.stock} ədəd\n"
            f"🔢 *Məhsul ID*: {product.id}"
        )
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message,
            parse_mode='Markdown'
        )
        logger.info(f"Telegram kanalına mesaj göndərildi: {product.name}")
    except Exception as e:
        logger.error(f"Telegrama mesaj göndərilmədi: {e}")
