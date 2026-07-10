import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
import yt_dlp
import requests

BOT_TOKEN = "8832973538:AAF4lQsMKV7V4LrmLLw2PVXJIKEGMtNVPes"
GENIUS_TOKEN = "PTLOpXFB92N7vC0VdpvJtqomKsVip"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🎵 MuzicPro ga xush kelibsiz!\n\n"
        "Qo'shiq nomini yozing — men topaman!\n\n"
        "📝 /lyrics — qo'shiq matni\n"
        "🎧 /music — musiqa yuklab olish"
    )

@dp.message(Command("music"))
async def music_cmd(message: Message):
    await message.answer("🎵 Qo'shiq nomini yozing:")

@dp.message(Command("lyrics"))
async def lyrics_cmd(message: Message):
    await message.answer("📝 Qo'shiq nomini yozing (lyrics uchun):")

@dp.message(F.text)
async def handle_text(message: Message):
    query = message.text
    await message.answer(f"🔍 Qidirilmoqda: {query}...")
    
    try:
        # Lyrics qidirish
        headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
        r = requests.get(
            "https://api.genius.com/search",
            params={"q": query},
            headers=headers
        )
        data = r.json()
        hits = data.get("response", {}).get("hits", [])
        
        if hits:
            song = hits[0]["result"]
            title = song["title"]
            artist = song["primary_artist"]["name"]
            url = song["url"]
            await message.answer(
                f"🎵 Topildi!\n\n"
                f"📀 Nomi: {title}\n"
                f"🎤 Artist: {artist}\n"
                f"📝 Lyrics: {url}"
            )
        else:
            await message.answer("❌ Qo'shiq topilmadi!")
            
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
