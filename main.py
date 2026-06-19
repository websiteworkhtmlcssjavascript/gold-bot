import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOLD_API_KEY = os.getenv("GOLD_API_KEY")

CHANNEL_ID = "@gold_price_live_2026"

bot = Bot(token=BOT_TOKEN)

message_id = None
last_text = ""


async def update_gold():
    global message_id, last_text

    while True:
        try:
            headers = {
                "x-access-token": GOLD_API_KEY,
                "Content-Type": "application/json"
            }

            response = requests.get(
                "https://www.goldapi.io/api/XAU/USD",
                headers=headers,
                timeout=10
            )

            data = response.json()

            print(data)

            price = data.get("price")

            if price is None:
                print("Price not found")
                await asyncio.sleep(10)
                continue

            text = (
                "🟡 GOLD LIVE\n\n"
                f"XAU/USD: {price}$\n\n"
                "🔄 Auto update every 10 sec"
            )

            if message_id is None:
                msg = await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=text
                )
                message_id = msg.message_id
                last_text = text

            else:
                if text != last_text:
                    await bot.edit_message_text(
                        chat_id=CHANNEL_ID,
                        message_id=message_id,
                        text=text
                    )
                    last_text = text

            print("Price:", price)

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(10)


asyncio.run(update_gold())
