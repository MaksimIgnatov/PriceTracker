# Инструкция по установке OzonPriceTracker

## Системные требования

- **Операционная система**: Windows 10/11, macOS, Linux
- **Python**: версия 3.12 или выше (для локальной установки)
- **Docker**: версия 20.10+ (для Docker установки)
- **Интернет**: стабильное соединение
- **Память**: минимум 512 МБ свободного места

## Установка

### Вариант 1: Docker (рекомендуется)

#### Шаг 1: Установка Docker

Установите Docker Desktop с [docker.com](https://www.docker.com/products/docker-desktop/)

#### Шаг 2: Клонирование проекта

```bash
git clone https://github.com/MaksimIgnatov/PriceTracker.git
cd PriceTracker
```

#### Шаг 3: Запуск через Docker Compose

```bash
# Сборка и запуск
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build
```

#### Шаг 4: Использование

```bash
# Интерактивный режим
docker-compose run ozon-tracker

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Вариант 2: Локальная установка

## Пошаговая установка

### Шаг 1: Проверка Python

Убедитесь, что Python установлен на вашем компьютере:

```bash
python --version
```

Если Python не установлен, скачайте его с [python.org](https://www.python.org/downloads/)

### Шаг 2: Клонирование проекта

Скачайте или скопируйте файлы проекта в папку на вашем компьютере.

### Шаг 3: Переход в папку проекта

```bash
cd OzonPriceTracker
```

### Шаг 4: Создание виртуального окружения (рекомендуется)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Шаг 5: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 6: Проверка установки

```bash
python main.py --help
```

Если появилась справка, установка прошла успешно!

## Альтернативная установка

### Установка без виртуального окружения:

```bash
pip install requests beautifulsoup4 pandas openpyxl matplotlib lxml
```

### Установка через conda:

```bash
conda create -n ozon-tracker python=3.12
conda activate ozon-tracker
pip install -r requirements.txt
```

## Проверка работоспособности

### Тестовый запуск:

1. Запустите приложение:
   ```bash
   python main.py
   ```

2. Введите тестовую категорию (например, "книги")

3. Укажите 1 страницу для парсинга

4. Проверьте, что создались файлы с данными

## Возможные проблемы при установке

### Ошибка "python не является внутренней или внешней командой"

**Решение**: Python не добавлен в PATH. Переустановите Python с галочкой "Add Python to PATH"

### Ошибка "pip не найден"

**Решение**: Установите pip:
```bash
python -m ensurepip --upgrade
```

### Ошибка при установке зависимостей

**Решение**: Обновите pip:
```bash
python -m pip install --upgrade pip
```

### Ошибка с matplotlib на Windows

**Решение**: Установите Visual C++ Redistributable или используйте:
```bash
pip install --only-binary=all matplotlib
```

### Ошибка с openpyxl

**Решение**: Установите дополнительно:
```bash
pip install openpyxl[styles]
```

## Настройка для разработки

### Установка дополнительных инструментов:

```bash
pip install jupyter notebook
pip install black flake8
```

### Настройка IDE:

Рекомендуемые IDE:
- Visual Studio Code с расширением Python
- PyCharm Community Edition
- Jupyter Notebook

## Обновление

### Обновление зависимостей:

```bash
pip install --upgrade -r requirements.txt
```

### Обновление приложения:

Замените файлы проекта на новые версии и переустановите зависимости.

## Удаление

### Полное удаление:

1. Удалите папку проекта
2. Если использовали виртуальное окружение:
   ```bash
   deactivate
   rmdir /s venv  # Windows
   rm -rf venv    # macOS/Linux
   ```

## Поддержка

При проблемах с установкой:

1. Проверьте версию Python: `python --version`
2. Проверьте версию pip: `pip --version`
3. Очистите кэш pip: `pip cache purge`
4. Попробуйте установку в виртуальном окружении
5. Обратитесь к логам установки

## Дополнительные настройки

### Настройка прокси (если необходимо):

Создайте файл `config.py`:
```python
PROXY = {
    'http': 'http://proxy:port',
    'https': 'https://proxy:port'
}
```

### Настройка User-Agent:

Отредактируйте файл `ozon_parser.py` в методе `__init__` класса `OzonParser`.
