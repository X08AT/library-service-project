import requests
from django.conf import settings


def send_telegram_message(message):

    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not configured")

    if not settings.TELEGRAM_CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID is not configured")

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
        },
    )
    response.raise_for_status()
