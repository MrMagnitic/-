import requests
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import logging
from config import BASE_URL, USER_AGENT, REQUEST_DELAY, DEFAULT_DAYS, CSV_FILENAME

logger = logging.getLogger(__name__)

def fetch_page(url, session):
    try:
        response = session.get(url)
        time.sleep(REQUEST_DELAY)
        if response.status_code == 200:
            return response
        return None
    except Exception as e:
        logger.error(f"Ошибка при запросе {url}: {e}")
        return None

def parse_news_page(soup):
    news_items = soup.find_all('a', {"class": "card-full-news _archive"}, href=True)
    page_data = []
    for item in news_items:
        title_elem = item.find('h3', {"class": "card-full-news__title"})
        topic_elem = item.find('span', {"class": "card-full-news__info-item card-full-news__rubric"})
        
        if title_elem and topic_elem:
            title = title_elem.get_text().strip()
            topic = topic_elem.get_text().strip()
            if title and topic:
                page_data.append((title, topic))
    return page_data

def collect_news(days=DEFAULT_DAYS, base_date=None, save_csv=True):
    if base_date is None:
        base_date = datetime.datetime.now()
    
    base_date = base_date.replace(hour=0, minute=0, second=0, microsecond=0)
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})

    records = []

    try:
        for day in range(1, days + 1):
            current_date = base_date - datetime.timedelta(days=day)
            
            if current_date > now:
                continue

            date_str = current_date.strftime('%Y/%m/%d')
            logger.info(f"Обработка {date_str} ({day}/{days})")
            
            page_num = 1
            while True:
                url = f"{BASE_URL}/{date_str}/page/{page_num}/"
                response = fetch_page(url, session)
                if not response:
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                page_news = parse_news_page(soup)
                if not page_news:
                    break

                for title, topic in page_news:
                    records.append({
                        'date': date_str,
                        'topic': topic,
                        'title': title
                    })
                page_num += 1
    except KeyboardInterrupt:
        logger.info(f"\nСбор данных прерван пользователем. Собрано {len(records)} записей.")
    
    if not records:
        logger.warning("Нет собранных данных.")
        return pd.DataFrame()

    df = pd.DataFrame(records)
    if save_csv:
        df.to_csv(CSV_FILENAME, index=False, encoding='utf-8')
        logger.info(f"Сохранено {len(df)} записей в {CSV_FILENAME}")
    return df