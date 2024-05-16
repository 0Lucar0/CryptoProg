import sqlite3
import requests
from bs4 import BeautifulSoup
import time

# Database connection
conn = sqlite3.connect('news.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS News
             (title TEXT, link TEXT PRIMARY KEY, text_news TEXT, photo_link TEXT, published TEXT DEFAULT 'no')''')


def get_news(url):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0 (Edition Yx GX)"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    news_list = []
    for listN in soup.find_all('li', class_='list_list__item__dwS6E !mt-0 border-t border-solid border-[#E6E9EB]'
                                            ' py-6'):
        linkN = listN.find('a', attrs={'data-test': 'article-title-link'})
        if linkN:
            href = linkN.get('href')
            if href:
                href = 'https://ru.investing.com' + href
                title = linkN.text.strip()
                news_item = {'title': title, 'link': href}
                news_list.append(news_item)
    return news_list


def parse_news_item(item):
    try:
        q = requests.get(item['link'])
        result = q.content
        soup = BeautifulSoup(result, 'lxml')
        text_news = soup.find(class_='article_WYSIWYG__O0uhw article_articlePage__UMz3q text-[18px] leading-8').find(
            'p').text.strip()
        item['text_news'] = text_news if text_news else ''
        photo_div = soup.find('div',
                              class_='mb-5 mt-4 sm:mt-8 md:mb-8 relative h-[294px] w-full overflow-hidden bg-[#181C21]'
                                     ' sm:h-[420px] xl:h-[441px]').find('img', class_='h-full w-full object-contain')
        photo_link = photo_div['src'] if photo_div else ''
        item['photo_link'] = photo_link
        return item
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while parsing news text: {e}")
        return None


def save_news_item(item):
    c.execute("INSERT OR IGNORE INTO News (title, link, text_news, photo_link) VALUES (?, ?, ?, ?)", (
        item['title'],
        item['link'],
        item['text_news'],
        item['photo_link']))
    conn.commit()
    print(f"Новость \"{item['title']}\" сохранена в базе данных.")


def main():
    url = "https://ru.investing.com/news/cryptocurrency-news"
    while True:
        news_list = get_news(url)
        for item in news_list:
            parsed_item = parse_news_item(item)
            if parsed_item:
                save_news_item(parsed_item)
        print("Сканирование завершено. Ждем 60 секунд перед следующим сканированием...")
        time.sleep(420)


if __name__ == "__main__":
    try:
        main()
    finally:
        conn.close()
