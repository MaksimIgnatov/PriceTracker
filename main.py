"""
Главный файл приложения OzonPriceTracker
"""
import sys
import logging
from datetime import datetime
from ozon_parser import OzonParser
from price_analyzer import PriceAnalyzer

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ozon_tracker.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция приложения"""
    print("=" * 60)
    print("           OZON PRICE TRACKER")
    print("=" * 60)
    print()
    
    try:
        # Инициализация парсера и анализатора
        parser = OzonParser()
        analyzer = PriceAnalyzer()
        
        # Получение параметров от пользователя
        category = input("Введите категорию товаров для поиска (например, 'ноутбуки'): ").strip()
        if not category:
            category = "ноутбуки"
            print(f"Используется категория по умолчанию: {category}")
        
        try:
            max_pages = int(input("Введите количество страниц для парсинга (по умолчанию 3): ") or "3")
        except ValueError:
            max_pages = 3
            print(f"Используется количество страниц по умолчанию: {max_pages}")
        
        print(f"\nНачинаем парсинг категории '{category}'...")
        print(f"Количество страниц: {max_pages}")
        print("-" * 40)
        
        # Парсинг данных
        products = parser.parse_category(category, max_pages)
        
        if not products:
            print("❌ Не удалось собрать данные. Возможно, изменилась структура сайта.")
            return
        
        print(f"✅ Успешно собрано {len(products)} товаров")
        
        # Сохранение данных
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"ozon_products_{timestamp}.xlsx"
        csv_filename = f"ozon_products_{timestamp}.csv"
        
        print("\nСохраняем данные...")
        
        # Сохранение в Excel
        parser.save_to_excel(products, excel_filename)
        print(f"✅ Данные сохранены в Excel: {excel_filename}")
        
        # Сохранение в CSV
        parser.save_to_csv(products, csv_filename)
        print(f"✅ Данные сохранены в CSV: {csv_filename}")
        
        # Анализ данных и создание графиков
        print("\nСоздаем графики и анализ...")
        
        # Загружаем данные в анализатор
        analyzer.load_data(excel_filename)
        
        # Создаем все графики
        charts = analyzer.create_all_charts()
        
        if charts:
            print(f"✅ Создано {len(charts)} графиков:")
            for chart in charts:
                print(f"   📊 {chart}")
        else:
            print("❌ Не удалось создать графики")
        
        # Выводим базовую статистику
        stats = analyzer.get_basic_statistics()
        if stats:
            print("\n📈 БАЗОВАЯ СТАТИСТИКА:")
            print("-" * 30)
            
            if 'current_price' in stats:
                price_stats = stats['current_price']
                print("Цены:")
                print(f"  • Средняя: {price_stats['mean']:.0f} руб.")
                print(f"  • Медианная: {price_stats['median']:.0f} руб.")
                print(f"  • Диапазон: {price_stats['min']:.0f} - {price_stats['max']:.0f} руб.")
            
            if 'rating' in stats:
                rating_stats = stats['rating']
                print("Рейтинги:")
                print(f"  • Средний: {rating_stats['mean']:.2f}")
                print(f"  • Медианный: {rating_stats['median']:.2f}")
            
            # Статистика по скидкам
            discount_products = len([p for p in products if p.get('old_price')])
            if discount_products > 0:
                print("Скидки:")
                print(f"  • Товаров со скидкой: {discount_products}")
                print(f"  • Процент товаров со скидкой: {discount_products/len(products)*100:.1f}%")
        
        print("\n🎉 Парсинг завершен успешно!")
        print("📁 Файлы сохранены в текущей директории")
        print("📊 Графики сохранены в папке 'charts'")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Парсинг прерван пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print(f"\n❌ Произошла ошибка: {e}")
        print("Проверьте логи в файле ozon_tracker.log")


def show_help():
    """Показывает справку по использованию"""
    help_text = """
OZON PRICE TRACKER - Справка

ОПИСАНИЕ:
    Приложение для мониторинга цен и характеристик товаров с маркетплейса Ozon.

ИСПОЛЬЗОВАНИЕ:
    python main.py

ФУНКЦИИ:
    • Парсинг товаров по категориям
    • Сбор данных: название, цена, старая цена, рейтинг, ссылка
    • Поддержка пагинации (несколько страниц)
    • Сохранение в Excel и CSV форматах
    • Создание графиков и анализ данных
    • Статистика по ценам и рейтингам

ФАЙЛЫ:
    • ozon_products_YYYYMMDD_HHMMSS.xlsx - данные в Excel
    • ozon_products_YYYYMMDD_HHMMSS.csv - данные в CSV
    • charts/ - папка с графиками
    • ozon_tracker.log - файл логов

ТРЕБОВАНИЯ:
    • Python 3.12+
    • Интернет-соединение
    • Установленные зависимости (см. requirements.txt)

ПРИМЕРЫ КАТЕГОРИЙ:
    • ноутбуки
    • смартфоны
    • наушники
    • одежда
    • книги
    """
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
    else:
        main()
