# payments/services/paypal_service.py
from payments.paypal_client import paypalrestsdk

def create_paypal_payment(order_id, total_amount, return_url, cancel_url):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
        },
        "transactions": [{
            "amount": {
                "total": f"{total_amount:.2f}",
                "currency": "USD"
            },
            "description": f"Order ID: {order_id}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return link.href  # Bu linki frontendə göndər
    else:
        raise Exception(payment.error)
