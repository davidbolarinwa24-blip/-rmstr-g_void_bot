import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def GetAccountInformation(data):
    """Placeholder - replace with your actual function"""
    return data

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "👋 Welcome to Free Fire Like Bot\n"
        "**Usage:** `/like [region] [uid]`\n"
        "Example: `/like ind 5513136227`",
        parse_mode='Markdown'
    )

@dp.message(Command("like"))
async def like_cmd(message: Message):
    args = message.text.split()

    # Check args count
    if len(args) < 3:
        await message.answer(
            "**Usage:** `/like [region] [uid]`\nExample: `/like ind 5513136227`",
            parse_mode='Markdown'
        )
        return

    region = args[1].lower()
    uid_in = args[2]

    # VALIDATION: Prevent crash on non-numeric UID
    try:
        uid = int(uid_in)
    except ValueError:
        await message.answer("❌ UID must be numbers only!\nExample: `/like ind 5513136227`", parse_mode='Markdown')
        return

    sent_msg = await message.answer("⏳ *Processing your request...*", parse_mode='Markdown')

    api_url = f"https://najmi-0b53-like-api-yukb.vercel.app/like?uid={uid}&server_name={region}&key=NJM"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=15) as resp:
                resp.raise_for_status() # Check status first - prevents JSON crash
                data = await resp.json()

                # FIXED: Use info_after, not info
                info_after = await GetAccountInformation(data)
                basic_info = info_after.get("basicInfo", {})
                new_likes = basic_info.get("liked", 0)

                likes_before = data.get('likes before command', '0')
                likes_given = data.get('likes given by API', '0')
                remaining = data.get('remaining', 'N/A')
                nickname = data.get('Player nickname', 'N/A')

                template = (
                    f"💎 **LIKE SUCCESSFULLY ✅**\n\n"
                    f"👑 Name: {nickname}\n"
                    f"🆔 UID: {uid}\n"
                    f"🌍 Region: {region.upper()}\n\n"
                    f"❤️ Likes Before: {likes_before}\n"
                    f"📦 Likes Given: {likes_given}\n"
                    f"💚 Likes After: {new_likes}\n"
                    f"📋 Remaining: {remaining}"
                )

                await sent_msg.edit_text(template, parse_mode='Markdown')

    except aiohttp.ClientResponseError as e:
        await sent_msg.edit_text(f"❌ API error {e.status}: {e.message}")
    except asyncio.TimeoutError:
        await sent_msg.edit_text("❌ API took too long. Try again in 5s")
    except Exception as e:
        await sent_msg.edit_text(f"❌ Error: {str(e)[:100]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
