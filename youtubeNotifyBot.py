import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from googleapiclient.discovery import build

YOUTUBE_API_KEY = 'AIzaSyB6qkSSMCgHYbcld8Nk0h7DSmP0LjtM1Lg'
CHANNEL_ID = 'UCPdbEHOt8BCs8JbDMTP8bFA'

CHAT_ID = '-1001853205861'

bot = Bot(token="7096954659:AAHnaeiu6rYwUgyeOtBkbE8c7UeBImtCzJ4")
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


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
                await bot.send_message(CHAT_ID, f"🔴 Не пропускай СТРИМ! ЗАЛЕТАЙ!: [{video_title}]({video_url})",
                                       parse_mode=ParseMode.MARKDOWN)
                await asyncio.sleep(3600)

        await asyncio.sleep(10)


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Привет Паша, я жажду служиь!")


async def main():
    asyncio.create_task(check_stream())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
