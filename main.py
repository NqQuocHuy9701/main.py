from flask import Flask, request
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

app = Flask(__name__)

# ---------------- BOT ----------------
BOT_TOKEN = "7700824508:AAGk2jYcj30Cao7UPk25YyNlEj89WA2WDzA"

# ------------- Google Sheets --------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1k6Tyyy8MQTulM9v1K8jiKWmYtJQ2Iv4dBCAILWijJig"  # Thay bằng ID file Google Sheet của bạn
CREDS = Credentials.from_service_account_file(
    "caramel-banner-479518-c9-111cee878a32.json",  # hoặc tên file JSON bạn tải về
    scopes=SCOPES
)

def append_row(values):
    """Hàm ghi một dòng vào Google Sheet"""
    service = build("sheets", "v4", credentials=CREDS)
    body = {"values": [values]}
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="TEST!A:G",  # Tên sheet và số cột
        valueInputOption="RAW",
        body=body
    ).execute()

# --------------- Webhook ----------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        text = data["message"].get("text", "")
        chat_id = data["message"]["chat"]["id"]
        name = data["message"]["chat"].get("first_name", "Unknown")
        shift = "Ca 1"           # Bạn có thể lấy từ message nếu muốn
        start = "08:00"
        end = "17:00"

        # Gửi phản hồi tin nhắn Telegram
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": f"Bot nhận được: {text}"}
        )

        # Nếu message chứa #checkin → ghi vào Google Sheet
        if "#checkin" in text.lower():
            append_row([name, "checkin", shift, start, end, text, datetime.now().isoformat()])

    return "ok"

# ------------- Chạy Flask ---------------
if __name__ == "__main__":
    # Host 0.0.0.0 để Render truy cập được
    app.run(host="0.0.0.0", port=5000)
