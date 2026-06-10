import pandas as pd
import matplotlib
matplotlib.use('TkAgg')          
import matplotlib.pyplot as plt
from collections import Counter
import re
import logging
from config import CSV_FILENAME, EXCEL_FILENAME, REPORT_FILENAME

logger = logging.getLogger(__name__)

def load_data(file_path=None):
    if file_path is None:
        file_path = CSV_FILENAME
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        logger.info(f"Загружено {len(df)} записей из {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")
        return pd.DataFrame()

def prepare_dataframe(df):
    if df.empty:
        return df
    
    df = df.dropna(subset=['date', 'topic', 'title']).copy()
    df['date_dt'] = pd.to_datetime(df['date'], format='%Y/%m/%d', errors='coerce')
    df = df.dropna(subset=['date_dt'])
    df['month'] = df['date_dt'].dt.to_period('M')
    df['weekday'] = df['date_dt'].dt.day_name()
    df['title_length'] = df['title'].str.len()
    
    return df

def get_word_freq(titles, min_length=4, top_n=20):
    all_titles = ' '.join(titles).lower()
    words = re.findall(r'\b[а-яё]{%d,}\b' % min_length, all_titles)
    return Counter(words).most_common(top_n)

def plot_analysis(df):
    if df.empty:
        logger.warning("Нет данных для построения графиков.")
        return

    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    monthly_counts = df.groupby(df['date_dt'].dt.to_period('M')).size()
    monthly_counts.plot(kind='bar')
    plt.title('Количество новостей по месяцам')
    plt.xlabel('Месяц')
    plt.ylabel('Количество')
    plt.xticks(rotation=45)

    plt.subplot(2, 2, 2)
    topic_counts = df['topic'].value_counts().head(10)
    topic_counts.plot(kind='barh')
    plt.title('Топ-10 тем')
    plt.xlabel('Количество')

    plt.subplot(2, 2, 3)
    df['title_length'].hist(bins=30)
    plt.title('Распределение длины заголовков')
    plt.xlabel('Длина (символы)')
    plt.ylabel('Частота')

    plt.subplot(2, 2, 4)
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_counts = df['weekday'].value_counts().reindex(weekday_order)
    weekday_counts.plot(kind='bar')
    plt.title('Новости по дням недели')
    plt.xlabel('День недели')
    plt.ylabel('Количество')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

def generate_report(df):
    if df.empty:
        return

    topic_counts = df['topic'].value_counts()
    monthly_stats = df.groupby('month').agg(
        news_count=('title', 'count'),
        most_common_topic=('topic', lambda x: x.mode()[0] if len(x.mode()) > 0 else 'None')
    )
    weekday_counts = df['weekday'].value_counts()

    report = f"""
ОТЧЕТ ПО АНАЛИЗУ НОВОСТЕЙ LENTA.RU
=================================
Всего новостей: {len(df)}
Период: с {df['date_dt'].min().strftime('%Y-%m-%d')} по {df['date_dt'].max().strftime('%Y-%m-%d')}
Уникальных тем: {df['topic'].nunique()}

САМЫЕ ПОПУЛЯРНЫЕ ТЕМЫ:
{topic_counts.head(5).to_string()}

МЕСЯЧНАЯ СТАТИСТИКА (последние 3 месяца):
{monthly_stats.tail(3).to_string()}

СРЕДНЯЯ ДЛИНА ЗАГОЛОВКА: {df['title_length'].mean():.1f} символов

САМЫЕ АКТИВНЫЕ ДНИ НЕДЕЛИ:
{weekday_counts.head(3).to_string()}
"""

    with open(REPORT_FILENAME, 'w', encoding='utf-8') as f:
        f.write(report)
    logger.info(f"Отчёт сохранён в {REPORT_FILENAME}")

def analyze_news(df=None, file_path=None):
    if df is None:
        df = load_data(file_path)
    
    if df.empty:
        logger.error("Нет данных для анализа.")
        return None

    df = prepare_dataframe(df)
    
    if df.empty:
        logger.error("После подготовки данных не осталось записей.")
        return None


    print("\nТоп-10 тем:")
    print("=======================")
    topic_counts = df['topic'].value_counts().head(10)
    for topic, count in topic_counts.items():
        print(f"{topic}: {count}")


    print("\nНовостей по месяцам:")
    print("==============================")
    monthly_counts = df.groupby('month').size()
    for month, count in monthly_counts.items():
        print(f"{month}: {count}")

    print("\nТоп-20 слов в заголовках:")
    print("==============================")
    for word, freq in get_word_freq(df['title']):
        print(f"{word}: {freq}")

    print("\nПостроение графиков...")
    plot_analysis(df)

    generate_report(df)
    
    output_csv = 'sorted_' + CSV_FILENAME
    df.to_csv(output_csv, index=False, encoding='utf-8')
    logger.info(f"Отсортированные данные сохранены в {output_csv}")
    
    try:
        df.to_excel(EXCEL_FILENAME, index=False)
        logger.info(f"Данные сохранены в Excel: {EXCEL_FILENAME}")
    except ModuleNotFoundError:
        logger.warning("Модуль openpyxl не установлен. Excel файл не создан.")
    except Exception as e:
        logger.error(f"Ошибка при сохранении в Excel: {e}")

    return df