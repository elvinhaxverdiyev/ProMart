import paypalrestsdk
from django.conf import settings
from payments.models.payments_models import Payment
from payments.models.product_cache import ProductCache
import logging

logger = logging.getLogger(__name__)

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def process_payment_event(order_data: dict):
    user_id = order_data.get("user_id")
    product_id = order_data.get("product_id")
    cart_id = order_data.get("cart_id")
    action = order_data.get("action")

    if not all([user_id, product_id, cart_id, action]):
        logger.error(f"Missing required data: {order_data}")
        return None

    try:
        product = ProductCache.objects.get(product_id=product_id)
        price = float(product.price)
    except ProductCache.DoesNotExist:
        logger.error(f"Product {product_id} not found in cache")
        return None

    if action == "added":
        logger.info(f"Creating PayPal payment for user {user_id}, cart {cart_id}")
        price_str = f"{price:.2f}"

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": f"{settings.PAYMENT_BASE_URL}/api/v1/orders/payment/success?cart_id={cart_id}",
                "cancel_url": f"{settings.PAYMENT_BASE_URL}/api/v1/orders/payment/cancel?cart_id={cart_id}"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": product.name,
                        "sku": f"product_{product_id}",
                        "price": price_str,
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {"total": price_str, "currency": "USD"},
                "description": f"Payment for cart item {cart_id}"
            }]
        })

        db_payment = Payment.objects.create(
            order_id=cart_id,
            user_id=user_id,
            amount=price,
            status="pending",
            payment_method="paypal"
        )

        if payment.create():
            logger.info(f"PayPal payment created: {payment.id}")
            db_payment.paypal_payment_id = payment.id
            db_payment.save()
            for link in payment.links:
                if link.rel == "approval_url":
                    logger.info(f"Approval URL: {link.href}")
                    return link.href
        else:
            logger.error(f"PayPal payment creation failed: {payment.error}")
            db_payment.status = "failed"
            db_payment.save()
            return None

    elif action == "removed":
        logger.info(f"Cancelling payment for cart {cart_id}")
        Payment.objects.filter(order_id=cart_id, user_id=user_id).update(status="cancelled")
        return None

    logger.error(f"Unknown action: {action}")
    return None