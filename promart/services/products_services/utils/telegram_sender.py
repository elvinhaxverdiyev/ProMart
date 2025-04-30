import os
import logging
from telegram import Bot

# Configure logging
logger = logging.getLogger(__name__)

# Load Telegram configuration from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

async def send_product_to_telegram(product):
    """
    Sends product details to the specified Telegram channel.

    This asynchronous function formats and sends the given product's information,
    such as name, description, price, stock, and ID, to a Telegram channel.

    Args:
        product (object): The product instance containing its details.

    Returns:
        None
    """
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    message = (
        f"🔔 *New Product Added!*\n\n"
        f"🏷️ *Name*: {product.name}\n"
        f"📝 *Description*: {product.description}\n"
        f"💰 *Price*: {product.price} AZN\n"
        f"📦 *Stock*: {product.stock} units\n"
        f"🔢 *Product ID*: {product.id}"
    )
    await bot.send_message(
        chat_id=TELEGRAM_CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )
    logger.info(f"Message sent to Telegram channel for product: {product.name}")
