import os
import json
import requests
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

KAFKA_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
PRODUCT_TOPIC = os.getenv("KAFKA_PRODUCT_TOPIC")

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_API_BASE = os.getenv("PAYPAL_API_BASE")

def get_paypal_access_token():
    auth = (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(f"{PAYPAL_API_BASE}/v1/oauth2/token", headers=headers, data=data, auth=auth)
    response.raise_for_status()
    return response.json()["access_token"]

def create_paypal_order(product):
    access_token = get_paypal_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(float(product["price"]) * product["quantity"])
                },
                "description": f"Product ID {product['product_id']}"
            }
        ],
        "application_context": {
            "return_url": "https://your-frontend.com/paypal/success",
            "cancel_url": "https://your-frontend.com/paypal/cancel"
        }
    }

    response = requests.post(f"{PAYPAL_API_BASE}/v2/checkout/orders", headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_approval_url(order_response):
    for link in order_response["links"]:
        if link["rel"] == "approve":
            return link["href"]
    return None

def consume_product_topic():
    consumer = KafkaConsumer(
        PRODUCT_TOPIC,
        bootstrap_servers=KAFKA_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id="payment_service"
    )

    for message in consumer:
        product = message.value
        print("Received product:", product)

        if product.get("action") != "added":
            continue

        try:
            paypal_order = create_paypal_order(product)
            approval_url = get_approval_url(paypal_order)
            print(f"Redirect user to: {approval_url}")
        except Exception as e:
            print("PayPal error:", e)

if __name__ == "__main__":
    consume_product_topic()
