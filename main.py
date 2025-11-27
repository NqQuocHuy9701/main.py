from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7700824508:AAGk2jYcj30Cao7UPk25YyNlEj89WA2WDzA"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        text = data["message"].get("text", "")
        chat_id = data["message"]["chat"]["id"]

        # Gửi thử tin nhắn về nhóm xem bot hoạt động ko
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                     params={"chat_id": chat_id, "text": f"Bot nhận được: {text}"})

    return "ok"

if __name__ == "__main__":
    app.run()
