from telegram import Bot
import asyncio

BOT_TOKEN = "8826488858:AAFLXXaWXnNX00LdJuXT9QweAy1dXTFpt-8"

async def test():
    bot = Bot(BOT_TOKEN)
    await bot.send_message(
        chat_id="@gold_price_live_2026",
        text="✅ Bot Connected"
    )

asyncio.run(test())
