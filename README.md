# Telegram welcome bot

Python 3.10 or newer. No third-party dependencies.

## Run

Set the `BOT_TOKEN` environment variable to the existing bot token, then run:

```sh
python bot.py
```

For Render, use a Background Worker with start command `python bot.py` and environment variable `BOT_TOKEN`. Run exactly one instance; stop any previous process using the same token.

## Behavior

In a private chat, `/start` immediately sends one message containing the supplied Khmer text and visible service link, followed by one inline button pointing to the same link. Link previews are disabled. Other messages receive no response.

The program does not change the bot name, username, profile image, About, or Description. It removes any existing webhook to enable long polling.

Keep the token secret; do not commit it. This repository does not include a token, and committing the code does not deploy the bot.
