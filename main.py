last_text = ""

async def update_gold():
    global message_id, last_text

    while True:
        try:
            ...
            text = f"""🟡 GOLD LIVE

💰 XAU/USD: {price} USD

🔄 Update every 5 seconds
"""

            if text != last_text:

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

                last_text = text

            print("Running...")

        except Exception as e:
            print("ERROR:", e)

        await asyncio.sleep(5)
