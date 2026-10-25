from flask import Flask, request, jsonify
import requests
import os
import hashlib
import hmac
import base64

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("8970176039:AAF7-EkOr1iOZiMU6fROBgZY-VfNqy764kc")
TELEGRAM_CHAT_ID = os.getenv("6863257643")
CONSUMER_SECRET = os.getenv("QeaU4GNdMIyxdZsJiwNleCTfWXJEcjUFpgm5T3WidbkAqrXOAS")

KEYWORDS = [
    "cheap laptop", "budget laptop", "laptop deals", "laptop sale",
    "laptop discount", "laptop clearance", "laptop under $200", "laptop under $300",
    "Amazon deals", "Amazon discounts", "Amazon coupon", "50% off", "60% off", "70% off",
    "flash sale", "lightning deal", "limited time deal", "refurbished laptop",
    "renewed laptop", "gaming laptop deal", "ThinkPad deal", "HP laptop", "Dell laptop",
    "Lenovo laptop", "ASUS laptop", "Acer laptop", "Chromebook deal", "tech deals",
    "electronics deals", "price drop", "price error"
]

def contains_keyword(text):
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in KEYWORDS)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        crc_token = request.args.get("crc_token")
        if crc_token and CONSUMER_SECRET:
            sha256_hash = hmac.new(
                CONSUMER_SECRET.encode("utf-8"),
                crc_token.encode("utf-8"),
                hashlib.sha256
            ).digest()
            response_token = "sha256=" + base64.b64encode(sha256_hash).decode("utf-8")
            return jsonify({"response_token": response_token})
        return "OK", 200

    # POST - eventos de X
    data = request.json
    if data and "data" in data:
        post = data["data"]
        text = post.get("text", "")
        user = post.get("author", {}).get("username", "")

        if contains_keyword(text):
            message = f"🛒 *Deal encontrado* (@{user})\n\n{text}\n\nhttps://x.com/{user}/status/{post.get('id')}"
            requests.post(
                f"https://api.telegram.org/bot{8970176039:AAF7-EkOr1iOZiMU6fROBgZY-VfNqy764kc}/sendMessage",
                json={
                    "chat_id": 6863257643,
                    "text": message,
                    "parse_mode": "Markdown"
                }
            )

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
