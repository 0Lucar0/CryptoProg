import sqlite3
import requests
from bs4 import BeautifulSoup
import time

# Создаем подключение к базе данных
conn = sqlite3.connect('news.db')
c = conn.cursor()

# Создаем таблицу для хранения новостей, если она еще не существует
c.execute('''CREATE TABLE IF NOT EXISTS News
             (title TEXT, link TEXT PRIMARY KEY, text_news TEXT, photo_link TEXT)''')

def save_news_text(news):
    for item in news:
        try:
            q = requests.get(item['link'])
            result = q.content
            soup = BeautifulSoup(result, 'lxml')

            # Парсим текст новости, если он есть
            text_news = soup.find(class_='article_WYSIWYG__O0uhw article_articlePage__UMz3q text-[18px] leading-8').find('p').text.strip()
            item['text_news'] = text_news if text_news else ''  # Проверка на наличие текста новости

            # Парсим ссылку на фотографию
            photo_div = soup.find('div', class_='mb-2 mt-4 sm:mb-6 sm:mt-8 relative h-[294px] w-full overflow-hidden bg-[#181C21] sm:h-[420px] xl:h-[441px]').find('img', class_='h-full w-full object-contain')
            photo_link = photo_div['src'] if photo_div else ''
            item['photo_link'] = photo_link

            # Добавим отладочный вывод для проверки
            print(f"Title: {item['title']}, Link: {item['link']}, Text: {item['text_news']}, Photo Link: {item['photo_link']}")

            # Сохраняем только ссылку на фотографию в базу данных
            c.execute("INSERT OR IGNORE INTO News (title, link, text_news, photo_link) VALUES (?, ?, ?, ?)", (
                item['title'],
                item['link'],
                item['text_news'],
                item['photo_link']))
            conn.commit()
            print(f"Новость \"{item['title']}\" сохранена в базу данных.")
        except Exception as e:
            print(f"Error occurred while parsing news text: {e}")
def main():
    url = "https://ru.investing.com/news/cryptocurrency-news"
    while True:
        news = get_news(url)
        save_news_text(news)
        print("Сканирование завершено. Ждем 60 секунд перед следующим сканированием...")
        time.sleep(2700)  # Пауза в 60 секунд
def get_news(url):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0 (Edition Yx GX)"
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    news_list = []

    list_news = soup.find_all('li', class_='list_list__item__dwS6E !mt-0 border-t border-solid border-[#E6E9EB] py-6')
    for listN in list_news:
        # Находим ссылку на заголовок новости
        linkN = listN.find('a', attrs={'data-test': 'article-title-link'})
        # Если ссылка найдена
        if linkN:
            href = linkN.get('href')  # Получаем атрибут href
            if href:
                href = 'https://ru.investing.com' + href  # Конкатенируем только если href существует
                title = linkN.text.strip()  # Получаем текст заголовка
                news_item = {'title': title, 'link': href}
                news_list.append(news_item)

    return news_list


if __name__ == "__main__":
    main()

# Закрываем подключение к базе данных при завершении работы программы
conn.close()