import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from googleapiclient.discovery import build

YOUTUBE_API_KEY = 'AIzaSyB6qkSSMCgHYbcld8Nk0h7DSmP0LjtM1Lg'
CHANNEL_ID = 'UCtBnh_qm1Nk4WL-UmYpcldw'
CHAT_ID = '-1001833068691'

bot = Bot(token="7062851238:AAEsolB--k1vLwTzQ1BVU60C9hznGTvmXU0")
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


# Функция для проверки наличия активного стрима
async def check_stream():
    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=CHANNEL_ID,
            eventType="live",
            type="video"
        )
        response = request.execute()

        if response['items']:
            for item in response['items']:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                await bot.send_message(CHAT_ID, f"🔴 Live Stream Started: [{video_title}]({video_url})",
                                       parse_mode=ParseMode.MARKDOWN)
                await asyncio.sleep(3600)

        await asyncio.sleep(10)


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply(
        "Hi! I'm your YouTube Stream Notifier bot. I'll notify you when a live stream starts on your channel.")


async def main():
    asyncio.create_task(check_stream())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
