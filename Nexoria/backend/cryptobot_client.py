import os
import httpx

CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
API_URL = "https://pay.crypt.bot/api"

def create_invoice(amount: float, asset: str, description: str, payload: dict):
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}

    r = httpx.post(
        f"{API_URL}/createInvoice",
        json={
            "amount": amount,
            "asset": asset,
            "description": description,
            "payload": payload
        },
        headers=headers
    )

    data = r.json()["result"]

    return {
        "invoice_id": data["invoice_id"],
        "pay_url": data["pay_url"]
    }
