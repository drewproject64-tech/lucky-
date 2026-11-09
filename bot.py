"""Single-message Telegram bot. Run with BOT_TOKEN set; Python 3.10+."""
import json
import logging
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SERVICE_URL = "https://t.me/Sdrservice24h"
WELCOME_MESSAGE = "សូមស្វាគមន៍មកវេបសាយធំបំផុត ងាយស្រួលលេង📲 និងគួរឱ្យទុកចិត្តបំផុតនៅកម្ពុជា🔥សេវាកម្ម២៤ម៉ោង: https://t.me/Sdrservice24h"


class TelegramError(Exception):
    pass


def api_call(token, method, payload):
    request = Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=50) as response:
            result = json.load(response)
    except (HTTPError, URLError, TimeoutError) as error:
        # Never log request URLs: they contain the bot token.
        raise TelegramError("Telegram request failed") from None
    if not result.get("ok"):
        raise TelegramError("Telegram rejected the request")
    return result["result"]


def handle_update(update, send):
    message = update.get("message", {})
    if message.get("chat", {}).get("type") != "private":
        return
    parts = message.get("text", "").split(maxsplit=1)
    if not parts or parts[0].split("@", 1)[0] != "/start":
        return
    send("sendMessage", {
        "chat_id": message["chat"]["id"],
        "text": WELCOME_MESSAGE,
        "link_preview_options": {"is_disabled": True},
        "reply_markup": {
            "inline_keyboard": [[{
                "text": "សេវាកម្ម២៤ម៉ោង",
                "url": SERVICE_URL,
            }]]
        },
    })


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("Set the BOT_TOKEN environment variable before starting.")
    send = lambda method, payload: api_call(token, method, payload)
    # Polling requires no webhook and must run as a single process.
    send("deleteWebhook", {"drop_pending_updates": False})
    offset = 0
    logging.info("Bot started.")
    while True:
        try:
            updates = send("getUpdates", {
                "offset": offset,
                "timeout": 40,
                "allowed_updates": ["message"],
            })
            for update in updates:
                handle_update(update, send)
                offset = update["update_id"] + 1
        except TelegramError:
            logging.warning("Telegram unavailable; retrying shortly.")
            time.sleep(3)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
