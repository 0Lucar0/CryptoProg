import asyncio
import sqlite3
from aiogram import Bot, types

API_TOKEN = '6920587354:AAEMcoGh9s0BVFUWQ6gLNpcN3aSTEwUnv68'
CHANNEL_ID = -1001724660274
bot = Bot(token=API_TOKEN)


async def send_message_with_photo(channel_id: int, text: str, photo_link: str):
    await bot.send_photo(channel_id, photo=photo_link, caption=text, parse_mode=types.ParseMode.HTML)


async def check_for_new_news():
    # Создаем подключение к базе данных
    conn = sqlite3.connect('news.db')
    c = conn.cursor()

    sent_news = set()  # Множество для отслеживания уже отправленных новостей

    while True:
        # Получаем данные из базы данных
        c.execute("SELECT * FROM News ORDER BY rowid DESC LIMIT 1")
        new_news = c.fetchone()

        if new_news and new_news[1] not in sent_news:
            news_text = f"💸💰<b>{new_news[0]}.</b>💸💰\n\n{new_news[2]}"
            await send_message_with_photo(CHANNEL_ID, news_text, new_news[3])  # Отправляем сообщение с фотографией
            sent_news.add(new_news[1])  # Добавляем ссылку на новость в множество отправленных новостей

        await asyncio.sleep(2700)  # Ожидание одного часа перед следующей проверкой


if __name__ == '__main__':
    asyncio.run(check_for_new_news())