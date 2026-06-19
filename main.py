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


async def main():
    global message_id, last_price

    while True:
        try:
            headers = {
                "x-access-token": GOLD_API_KEY
            }

            response = requests.get(
                "https://www.goldapi.io/api/XAU/USD",
                headers=headers,
                timeout=15
            )

            data = response.json()

            if "price" not in data:
                print(data)
                await asyncio.sleep(30)
                continue

            price = float(data["price"])

            upper = price * 1.002
            lower = price * 0.998

            if last_price is None:
                trend = "➖ First Reading"
            elif price > last_price:
                trend = "🟢 Bullish ⬆️"
            elif price < last_price:
                trend = "🔴 Bearish ⬇️"
            else:
                trend = "🟡 Sideways ➡️"

            text = f"""
🟡 GOLD LIVE

💰 Price
{price:.2f} USD

📈 Upper Range (+0.2%)
{upper:.2f}

📉 Lower Range (-0.2%)
{lower:.2f}

📊 Trend
{trend}

⏰ Update: 30 sec
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

            last_price = price

            print("Price:", price)

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(30)


asyncio.run(main())
