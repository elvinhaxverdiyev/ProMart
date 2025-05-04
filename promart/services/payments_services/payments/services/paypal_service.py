import paypalrestsdk
from django.conf import settings
from payments.models.payments_models import Payment
from payments.models.product_cache import ProductCache
import requests
import logging

logger = logging.getLogger(__name__)

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def get_product_price(product_id):
    """Get the product price from ProductCache or the products service API."""
    try:
        product = ProductCache.objects.get(product_id=product_id)
        return float(product.price)
    except ProductCache.DoesNotExist:
        try:
            response = requests.get(f"http://products_service:8001/api/v1/products/{product_id}/")
            if response.status_code == 200:
                return float(response.json()["price"])
            logger.error(f"Product price not retrieved product_id={product_id}: {response.status_code}")
            return None
        except requests.RequestException as e:
            logger.error(f"Error retrieving product price product_id={product_id}: {e}")
            return None

def process_payment_event(order_data: dict):
    """Process the Kafka message to initiate or cancel the PayPal payment."""
    user_id = order_data.get("user_id")
    product_id = order_data.get("product_id")
    cart_id = order_data.get("cart_id")
    action = order_data.get("action")

    if not all([user_id, product_id, cart_id]):
        logger.error(f"Missing data: user_id={user_id}, product_id={product_id}, cart_id={cart_id}")
        return {"error": "Missing required data"}

    if action == "added":
        price = get_product_price(product_id)
        if not price:
            logger.error(f"Product price not found product_id={product_id}")
            return {"error": "Product price not found"}

        price_str = f"{price:.2f}"
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": f"http://localhost:8004/api/v1/orders/payment/success?cart_id={cart_id}",
                "cancel_url": f"http://localhost:8004/api/v1/orders/payment/cancel?cart_id={cart_id}"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"Product {product_id}",
                        "sku": f"{product_id}",
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
            db_payment.paypal_payment_id = payment.id
            db_payment.status = "pending"
            db_payment.save()
            for link in payment.links:
                if link.method == "REDIRECT":
                    logger.info(f"Payment created cart_id={cart_id}, redirect: {link.href}")
                    return {"status": "pending", "approval_url": link.href, "cart_id": cart_id}
        else:
            logger.error(f"Payment creation failed cart_id={cart_id}: {payment.error}")
            db_payment.status = "failed"
            db_payment.save()
            return {"error": "Payment creation failed"}

    elif action == "removed":
        Payment.objects.filter(order_id=cart_id, user_id=user_id).update(status="cancelled")
        logger.info(f"Payment cancelled cart_id={cart_id}")
        return {"status": "cancelled", "cart_id": cart_id}

    return {"error": "Invalid action"}
