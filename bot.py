import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
FF_API_KEY = os.getenv("FF_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("🔮 Årmstrøng Void Bot is online 24/7!\nSend: /ff UID\nExample: /ff 811094988")

@dp.message(Command("ff"))
async def ff_cmd(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /ff <player_id>")
        return
    player_id = args[1]
    url = f"https://free-fire-api.p.rapidapi.com/player/{player_id}"
    headers = {"X-RapidAPI-Key": FF_API_KEY, "X-RapidAPI-Host": "free-fire-api.p.rapidapi.com"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                rank = data.get("rank", "Not found")
                name = data.get("nickname", "Unknown")
                await message.answer(f"Player: {name}\nRank: {rank}")
            else:
                # Show actual error so we can debug
                text = await resp.text()
                await message.answer(f"❌ API error {resp.status}\n{ text[:200]}")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
