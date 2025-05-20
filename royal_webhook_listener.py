# royal_webhook_listener.py — TradingView Webhook Gateway 🔮

from flask import Flask, request, jsonify
import asyncio
from oracle_voice_utils import send_telegram, send_voice, log_signal

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get("message", "📡 Webhook received without message.")
    pair = data.get("pair", "TRADINGVIEW")

    asyncio.run(send_telegram(message))
    asyncio.run(send_voice(message, pair))
    log_signal(pair, message)

    return jsonify({"status": "success", "message": message}), 200

if __name__ == "__main__":
    print("🛰️ Royal Webhook Oracle Listening on http://localhost:5000/webhook")
    app.run(host="0.0.0.0", port=5000)
