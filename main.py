import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOLD_API_KEY = os.getenv("GOLD_API_KEY")

CHANNEL_ID = "@gold_price_live_2026"

bot = Bot(token=BOT_TOKEN)

message_id = None

async def main():
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
                timeout=20
            )

            data = response.json()

            if "price" not in data:
                print(data)
                await asyncio.sleep(30)
                continue

            price = float(data["price"])

            upper = price * 1.005
            lower = price * 0.995

            text = f"""
🟡 GOLD LIVE

💰 Current Price
{price:.2f} USD

📈 Upper Range
{upper:.2f} USD

📉 Lower Range
{lower:.2f} USD

⏰ Update every 30 sec
"""

            if message_id is None:
                msg = await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=text
                )
                message_id = msg.message_id
            else:
                try:
                    await bot.edit_message_text(
                        chat_id=CHANNEL_ID,
                        message_id=message_id,
                        text=text
                    )
                except Exception:
                    pass

            print("Gold:", price)

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(30)

asyncio.run(main())
