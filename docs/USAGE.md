# Руководство по использованию OzonPriceTracker

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск приложения

```bash
python main.py
```

### 3. Следование инструкциям

Приложение попросит вас ввести:
- Категорию товаров для поиска
- Количество страниц для парсинга

## Примеры использования

### Мониторинг ноутбуков

```bash
python main.py
# Введите: ноутбуки
# Введите: 5
```

**Результат:**
- Файл `ozon_products_YYYYMMDD_HHMMSS.xlsx` с данными
- Файл `ozon_products_YYYYMMDD_HHMMSS.csv` с данными
- Графики в папке `charts/`

### Анализ смартфонов

```bash
python main.py
# Введите: смартфоны
# Введите: 3
```

### Поиск книг

```bash
python main.py
# Введите: книги
# Введите: 2
```

## Программное использование

### Использование парсера отдельно

```python
from ozon_parser import OzonParser

# Создание парсера
parser = OzonParser()

# Парсинг категории
products = parser.parse_category("ноутбуки", max_pages=3)

# Сохранение данных
parser.save_to_excel(products, "my_products.xlsx")
parser.save_to_csv(products, "my_products.csv")
```

### Использование анализатора отдельно

```python
from price_analyzer import PriceAnalyzer

# Создание анализатора
analyzer = PriceAnalyzer()

# Загрузка данных
analyzer.load_data("my_products.xlsx")

# Получение статистики
stats = analyzer.get_basic_statistics()
print(stats)

# Создание графиков
charts = analyzer.create_all_charts()
print(f"Создано графиков: {len(charts)}")
```

## Настройка параметров

### Изменение задержек между запросами

Отредактируйте файл `ozon_parser.py`:

```python
# В методе parse_category, строка с time.sleep(1)
time.sleep(2)  # Увеличить до 2 секунд
```

### Изменение User-Agent

Отредактируйте файл `ozon_parser.py`:

```python
# В методе __init__ класса OzonParser
'User-Agent': 'Ваш User-Agent'
```

### Настройка папки для графиков

Отредактируйте файл `price_analyzer.py`:

```python
# В методе __init__ класса PriceAnalyzer
self.output_dir = "my_charts"  # Изменить папку
```

## Работа с результатами

### Excel файлы

Откройте созданный Excel файл в любой программе:
- Microsoft Excel
- LibreOffice Calc
- Google Sheets

**Столбцы:**
- `title` - название товара
- `current_price` - текущая цена
- `old_price` - старая цена (если есть скидка)
- `rating` - рейтинг товара
- `url` - ссылка на товар
- `date_collected` - дата сбора данных

### CSV файлы

CSV файлы можно открыть в:
- Excel
- Google Sheets
- Текстовом редакторе
- Любой программе для работы с данными

### Графики

Графики сохраняются в папке `charts/` в формате PNG:

- `price_distribution.png` - распределение цен
- `rating_analysis.png` - анализ рейтингов
- `discount_analysis.png` - анализ скидок
- `summary_report.png` - сводный отчет

## Автоматизация

### Создание скрипта для регулярного мониторинга

Создайте файл `monitor.py`:

```python
import schedule
import time
from main import main

# Запуск каждый день в 9:00
schedule.every().day.at("09:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Пакетный мониторинг нескольких категорий

Создайте файл `batch_monitor.py`:

```python
from ozon_parser import OzonParser
from price_analyzer import PriceAnalyzer

categories = ["ноутбуки", "смартфоны", "наушники"]
parser = OzonParser()
analyzer = PriceAnalyzer()

for category in categories:
    print(f"Парсинг категории: {category}")
    products = parser.parse_category(category, max_pages=2)
    
    if products:
        filename = f"{category}_products.xlsx"
        parser.save_to_excel(products, filename)
        print(f"Сохранено {len(products)} товаров в {filename}")
```

## Решение проблем

### Ошибка "Нет данных"

**Причины:**
- Неправильное название категории
- Изменение структуры сайта
- Блокировка IP

**Решения:**
- Проверьте правильность названия категории
- Уменьшите количество страниц
- Увеличьте задержки между запросами

### Ошибка создания графиков

**Причины:**
- Отсутствие данных
- Проблемы с matplotlib

**Решения:**
- Убедитесь, что данные загружены
- Переустановите matplotlib: `pip install --upgrade matplotlib`

### Медленная работа

**Причины:**
- Большое количество страниц
- Медленное интернет-соединение

**Решения:**
- Уменьшите количество страниц
- Увеличьте задержки между запросами
- Используйте более быстрое интернет-соединение

## Логирование

Все действия записываются в файл `ozon_tracker.log`:

```bash
# Просмотр логов
tail -f ozon_tracker.log

# Поиск ошибок
grep "ERROR" ozon_tracker.log
```

## Расширенные возможности

### Добавление новых полей

Отредактируйте метод `parse_product_card` в `ozon_parser.py`:

```python
# Добавьте новое поле
product_data['new_field'] = extract_new_field(card_element)
```

### Создание новых графиков

Добавьте новый метод в класс `PriceAnalyzer`:

```python
def create_custom_chart(self):
    # Ваш код для создания графика
    pass
```

### Интеграция с базой данных

Используйте pandas для работы с базами данных:

```python
import sqlite3

# Сохранение в SQLite
df.to_sql('products', sqlite3.connect('products.db'), if_exists='append')
```

## Поддержка

При возникновении проблем:

1. Проверьте файл логов
2. Убедитесь в корректности установки
3. Попробуйте уменьшить параметры парсинга
4. Обратитесь к документации
