import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOLD_API_KEY = os.getenv("GOLD_API_KEY")

CHANNEL_ID = "@gold_price_live_2026"

bot = Bot(token=BOT_TOKEN)

message_id = None


async def update_gold():
    global message_id

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
    await asyncio.sleep(5)
    continue 

            text = f"""🟡 GOLD LIVE

💰 XAU/USD: {price} USD

🔄 Update every 5 seconds
"""

            if message_id is None:
                msg = await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=text
                )
                message_id = msg.message_id

            else:
                await bot.edit_message_text(
                    chat_id=CHANNEL_ID,
                    message_id=message_id,
                    text=text
                )

            print(f"Price: {price}")

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(5)


asyncio.run(update_gold())
