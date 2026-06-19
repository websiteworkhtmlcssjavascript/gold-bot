import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOLD_API_KEY = os.getenv("GOLD_API_KEY")

CHANNEL_ID = "@gold_price_live_2026"

bot = Bot(token=BOT_TOKEN)

message_id = None
last_price = None


async def get_gold_price():
    headers = {
        "x-access-token": GOLD_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(
        "https://www.goldapi.io/api/XAU/USD",
        headers=headers,
        timeout=15
    )

    data = response.json()

    if "error" in data:
        raise Exception(data["error"])

    return float(data["price"])


async def main():
    global message_id, last_price

    while True:
        try:
            price = await get_gold_price()

            text = f"""
🟡 GOLD LIVE

💰 XAU/USD : {price}

🔄 Update every 10 sec
"""

            if message_id is None:
                msg = await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=text
                )
                message_id = msg.message_id
                last_price = price

            else:
                if price != last_price:
                    await bot.edit_message_text(
                        chat_id=CHANNEL_ID,
                        message_id=message_id,
                        text=text
                    )
                    last_price = price

            print("Gold:", price)

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(10)


asyncio.run(main())
