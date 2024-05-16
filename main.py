import asyncio
import sqlite3
import random
from aiogram import Bot, types

API_TOKEN = '6920587354:AAEMcoGh9s0BVFUWQ6gLNpcN3aSTEwUnv68'
CHANNEL_ID = -1001724660274
bot = Bot(token=API_TOKEN)

EMOJIS = ['💸', '💰', '👀', '🔥']  # Add more emojis as needed

async def random_emoji():
    return random.choice(EMOJIS)

async def send_news_message(channel_id: int, text: str, photo_link: str):
    try:
        await bot.send_photo(channel_id, photo=photo_link, caption=text, parse_mode=types.ParseMode.HTML)
    except Exception as e:
        print(f"Error sending message: {e}")

async def monitor_news():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()

    while True:
        try:
            c.execute("SELECT * FROM News WHERE published=?", ('0',))
            new_news_list = c.fetchall()

            for new_news in new_news_list:
                emoji = await random_emoji()
                news_text = f"{emoji}<b>{new_news[0]}.</b>{emoji}\n\n{new_news[2]}"
                await send_news_message(CHANNEL_ID, news_text, new_news[3])

                c.execute("UPDATE News SET published=? WHERE link=?", ('1', new_news[1]))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error accessing database: {e}")
        except Exception as e:
            print(f"Error monitoring news: {e}")

        await asyncio.sleep(420)  # Wait for 1 hour before checking again

if __name__ == '__main__':
    asyncio.run(monitor_news())