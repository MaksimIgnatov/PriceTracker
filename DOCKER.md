# Docker инструкции для OzonPriceTracker

## 🐳 Быстрый старт с Docker

### Предварительные требования

- Docker Desktop установлен и запущен
- Git для клонирования репозитория

### Установка и запуск

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/MaksimIgnatov/PriceTracker.git
cd PriceTracker

# 2. Запустите приложение
docker-compose up --build
```

### Использование

После запуска приложение будет работать в интерактивном режиме. Следуйте инструкциям на экране:

1. Введите категорию товаров (например, "ноутбуки")
2. Укажите количество страниц для парсинга
3. Дождитесь завершения сбора данных

### Результаты

Все файлы сохраняются в локальные папки:
- `data/` - Excel и CSV файлы с данными
- `charts/` - графики и диаграммы
- `logs/` - файлы логов

## 🔧 Дополнительные команды

### Запуск в фоновом режиме

```bash
docker-compose up -d --build
```

### Просмотр логов

```bash
docker-compose logs -f
```

### Остановка

```bash
docker-compose down
```

### Пересборка контейнера

```bash
docker-compose build --no-cache
```

### Интерактивный режим

```bash
docker-compose run ozon-tracker
```

## 🛠 Разработка

### Редактирование кода

1. Отредактируйте файлы в локальной папке
2. Пересоберите контейнер:
   ```bash
   docker-compose build
   ```
3. Запустите обновленную версию:
   ```bash
   docker-compose up
   ```

### Отладка

```bash
# Запуск с bash для отладки
docker-compose run --rm ozon-tracker bash

# Просмотр содержимого контейнера
docker-compose exec ozon-tracker ls -la
```

## 📁 Структура Docker

```
PriceTracker/
├── Dockerfile              # Конфигурация Docker образа
├── docker-compose.yml      # Конфигурация сервисов
├── .dockerignore           # Исключения для Docker
├── data/                   # Монтируемая папка для данных
├── charts/                 # Монтируемая папка для графиков
└── logs/                   # Монтируемая папка для логов
```

## ⚠️ Важные замечания

1. **Первый запуск** может занять несколько минут из-за загрузки зависимостей
2. **Данные сохраняются** в локальные папки, поэтому не теряются при перезапуске
3. **Логи** доступны в папке `logs/` для отладки
4. **Память** - контейнер использует минимум ресурсов

## 🐛 Решение проблем

### Ошибка "Port already in use"

```bash
# Остановите все контейнеры
docker-compose down

# Запустите заново
docker-compose up --build
```

### Ошибка "Permission denied"

```bash
# На Linux/macOS исправьте права доступа
sudo chown -R $USER:$USER data charts logs
```

### Очистка Docker

```bash
# Удалите неиспользуемые образы
docker system prune -a

# Удалите все контейнеры проекта
docker-compose down --volumes --remove-orphans
```

## 📊 Мониторинг

### Использование ресурсов

```bash
# Просмотр статистики контейнера
docker stats

# Просмотр логов в реальном времени
docker-compose logs -f --tail=100
```

### Проверка состояния

```bash
# Статус сервисов
docker-compose ps

# Информация о контейнере
docker-compose exec ozon-tracker ps aux
```

## 🚀 Продвинутое использование

### Настройка переменных окружения

Создайте файл `.env`:

```env
# Настройки парсинга
MAX_PAGES=5
DELAY_BETWEEN_REQUESTS=1

# Настройки вывода
OUTPUT_FORMAT=xlsx,csv
CREATE_CHARTS=true
```

### Масштабирование

```bash
# Запуск нескольких экземпляров
docker-compose up --scale ozon-tracker=3
```

### Интеграция с CI/CD

```yaml
# .github/workflows/docker.yml
name: Docker Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker-compose build
      - name: Test Docker image
        run: docker-compose up --abort-on-container-exit
```
