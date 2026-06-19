import asyncio
import yfinance as yf
from telegram import Bot

BOT_TOKEN = "8826488858:AAFLXXaWXnNX00LdJuXT9QweAy1dXTFpt-8"
CHANNEL_ID = "@gold_price_live_2026"

bot = Bot(BOT_TOKEN)

message_id = None
last_text = ""


async def main():
    global message_id, last_text

    while True:
        try:
            gold = yf.Ticker("GC=F")

            df = gold.history(period="1d", interval="1m")

            if df.empty:
                print("No data")
                await asyncio.sleep(60)
                continue

            price = float(df["Close"].iloc[-1])

            text = f"""🟡 GOLD LIVE

💰 Price: {price:.2f} USD

⏱ Update: 60 sec
"""

            if message_id is None:
                msg = await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=text
                )
                message_id = msg.message_id
                last_text = text

            elif text != last_text:
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


asyncio.run(main())
