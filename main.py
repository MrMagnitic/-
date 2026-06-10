import argparse
import logging
from collector import collect_news
from analyzer import analyze_news
from config import DEFAULT_DAYS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description='Сбор и анализ новостей Lenta.ru')
    parser.add_argument('--collect', action='store_true', help='Собрать свежие новости')
    parser.add_argument('--days', type=int, default=DEFAULT_DAYS, help='Количество дней для сбора')
    parser.add_argument('--analyze', action='store_true', help='Выполнить анализ')
    parser.add_argument('--file', type=str, help='Файл с данными для анализа (по умолчанию lenta_news.csv)')
    args = parser.parse_args()

    if args.collect:
        df = collect_news(days=args.days)
        if not df.empty:
            print(f"Собрано {len(df)} новостей.")
    elif args.analyze:
        analyze_news(file_path=args.file)
    else:
        df = collect_news(days=args.days)
        if not df.empty:
            analyze_news(df)

if __name__ == '__main__':
    main()