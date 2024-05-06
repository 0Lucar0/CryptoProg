import asyncio
import json
from aiogram import *

API_TOKEN = '6920587354:AAEMcoGh9s0BVFUWQ6gLNpcN3aSTEwUnv68'
CHANNEL_ID = -1001724660274
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

async def send_message(channel_id: int, text: str):
    await bot.send_messagechannel_id, text)

async def check_for_new_news():
    sent_news = set()

    while True:
        # Открываем файл с новостями и загружаем их из JSON
        with open('news_dict.json', encoding='utf-8') as file:
            news_list = json.load(file)
        await bot.send_photo(CHANNEL_ID, photo='https://d7-invdn-com.investing.com/content/picfab5a6328ca58ecd90a1b26211b984a2.png')
        # Если список новостей не пустой
        if news_list:
            # Берем самую свежую новость из самого верха списка
            new_news_item = news_list[0]

            # Проверяем, была ли эта новость уже отправлена
            if new_news_item['link'] not in sent_news:
                # Проверяем, была ли ссылка уже отправлена ранее
                with open('sent_news.txt', 'r', encoding='utf-8') as f:
                    if new_news_item['link'] not in f.read():
                        # Формируем текст новости для отправки
                        news_text = (f"💸💰<b>{new_news_item['title']}.</b>💸💰\n\n"
                                     f"{new_news_item['text_news']}\n")
                        # Отправляем сообщение с новостью
                        await send_message(CHANNEL_ID, news_text)
                        await bot.send_photo(CHANNEL_ID, photo='https://d7-invdn-com.investing.com/content/picfab5a6328ca58ecd90a1b26211b984a2.png')
                        # Добавляем ссылку на новость в список отправленных новостей
                        sent_news.add(new_news_item['link'])

                        # Записываем ссылку на отправленную новость в отдельный текстовый файл
                        with open('sent_news.txt', 'a', encoding='utf-8') as f:
                            f.write(new_news_item['link'] + '\n')

                # Удаляем отправленную новость из списка новостей
                del news_list[0]

                # Перезаписываем обновленный список новостей в файл
                with open('news_dict.json', 'w', encoding='utf-8') as file:
                    json.dump(news_list, file, ensure_ascii=False, indent=4)

        # Ожидание одного часа перед проверкой новых новостей
        await asyncio.sleep(15)

if __name__ == '__main__':
    asyncio.run(check_for_new_news())