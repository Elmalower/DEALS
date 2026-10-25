from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# === CONFIGURACIÓN ===
TELEGRAM_TOKEN = os.getenv("8970176039:AAF7-EkOr1iOZiMU6fROBgZY-VfNqy764kc")      # Ponlo en variables de entorno
TELEGRAM_CHAT_ID = os.getenv("6863257643")  # Tu chat ID

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

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # X Activity API envía el post en data["data"]
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