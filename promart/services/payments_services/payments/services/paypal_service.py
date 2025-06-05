import requests
from django.conf import settings

def get_paypal_access_token():
    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_paypal_order(cart_items, total_amount, currency="USD"):
    access_token = get_paypal_access_token()

    url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    item_list = []
    for item in cart_items:
        item_list.append({
            "name": item["product_name"],
            "quantity": str(item["quantity"]),
            "unit_amount": {
                "currency_code": currency,
                "value": str(item["price"])
            }
        })

    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": currency,
                    "value": str(total_amount),
                    "breakdown": {
                        "item_total": {
                            "currency_code": currency,
                            "value": str(total_amount)
                        }
                    }
                },
                "items": item_list
            }
        ],
        "application_context": {
            "return_url": "https://yourdomain.com/paypal/success",
            "cancel_url": "https://yourdomain.com/paypal/cancel"
        }
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
