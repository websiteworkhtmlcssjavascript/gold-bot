import os
import asyncio
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("8826488858:AAFLXXaWXnNX00LdJuXT9QweAy1dXTFpt-8")
GOLD_API_KEY = os.getenv("goldapi-315b0b99d2ec5744f99b0c37edaf77cb-io")

CHANNEL_ID = "@AAB12AAB_BOT"

bot = Bot(token=BOT_TOKEN)

message_id = None


async def update_gold():
    global message_id

    while True:
        try:
            headers = {
                "x-access-token": GOLD_API_KEY
            }

            response = requests.get(
                "https://www.goldapi.io/api/XAU/USD",
                headers=headers,
                timeout=10
            )

            data = response.json()
            price = data.get("price", "N/A")

            text = f"🟡 Gold Price\n\nXAU/USD: {price} USD"

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

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(5)


asyncio.run(update_gold())
