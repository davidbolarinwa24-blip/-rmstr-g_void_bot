import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🔮 Årmstrøng Void Bot is online 24/7!\n\n"
        "Send: /like <region> <uid>\n"
        "Example: /like ind 5513136227"
    )

@dp.message(Command("like"))
async def like_cmd(message: types.Message):
    args = message.text.split()
    if len(args) < 3:
        await message.answer(
            "**Usage:** `/like [region] [uid]`\n"
            "Example: `/like ind 5513136227`",
            parse_mode='Markdown'
        )
        return

    region = args[1]
    uid = args[2]
    sent_msg = await message.answer("⏳ *Processing your request...*", parse_mode='Markdown')

    # API call from your book page 2 line 24-25
    api_url = f"https://najmi-0b53-like-api-yukb.vercel.app/like?uid={uid}&server_name={region}&key=NJM"

    try:
        # Converted requests.get to async aiohttp for Railway
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    # Mapping API response - your book page 2 line 31-35
                    name = data.get('Player nickname', 'N/A')
                    likes_before = data.get('likes before command', '0')
                    likes_given = data.get('likes given by API', '0')
                    likes_after = data.get('likes after command', '0')
                    remaining = data.get('remaining', 'N/A')

                    # Your exact template from book page 3 line 37-49
                    template = (
                        f"——— ◇◆◇ ———\n"
                        f"💎 LIKE SUCCESSFULLY ✅\n"
                        f"——— ◇◆◇ ———\n\n"
                        f"👑 Name: {name}\n"
                        f"🆔 UID: {uid}\n"
                        f"🌍 Region: {region.upper()}\n\n"
                        f"———\n"
                        f"❤️ Likes Before: {likes_before}\n"
                        f"📦 Likes Given: {likes_given}\n"
                        f"💚 Likes After: {likes_after}\n"
                        f"———\n"
                        f"📋 Remaining Requests: {remaining}"
                    )

                    await sent_msg.edit_text(template)

                else:
                    text = await resp.text()
                    await sent_msg.edit_text(
                        f"❌ API error {resp.status}\n"
                        f"Details: {text[:150]}"
                    )
    except Exception as e:
        await sent_msg.edit_text(f"❌ Connection error: {str(e)[:100]}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
