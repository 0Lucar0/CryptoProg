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

    while True:
        # Получаем все новости из базы данных, у которых значение published равно 'no'
        c.execute("SELECT * FROM News WHERE published=?", ('0',))
        new_news_list = c.fetchall()

        for new_news in new_news_list:
            # Опубликовываем новость в канале
            news_text = f"💸💰<b>{new_news[0]}.</b>💸💰\n\n{new_news[2]}"
            await send_message_with_photo(CHANNEL_ID, news_text, new_news[3])  # Отправляем сообщение с фотографией

            # Обновляем статус новости в базе данных на "опубликовано в канале"
            c.execute("UPDATE News SET published=? WHERE link=?", ('1', new_news[1]))
            conn.commit()  # Фиксируем изменения в базе данных

        await asyncio.sleep(420)  # Ожидание одного часа перед следующей проверкой

if __name__ == '__main__':
    asyncio.run(check_for_new_news())