"""
Парсер для сбора данных о товарах с маркетплейса Ozon
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin
from typing import List, Dict, Optional
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OzonParser:
    """Класс для парсинга товаров с Ozon"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,*/*;q=0.8'),
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.base_url = "https://www.ozon.ru"
        
    def get_category_url(self, category: str) -> str:
        """Формирует URL для категории товаров"""
        # Простой поиск по категории
        search_url = f"{self.base_url}/search/?text={category}"
        return search_url
    
    def parse_product_card(self, card_element) -> Optional[Dict]:
        """Парсит карточку товара"""
        try:
            product_data = {}
            
            # Название товара
            title_element = card_element.find('a', {'data-widget': 'searchResultV2'})
            if title_element:
                product_data['title'] = title_element.get('title', '').strip()
                product_data['url'] = urljoin(self.base_url, title_element.get('href', ''))
            else:
                # Альтернативный поиск названия
                title_element = card_element.find('span', class_='tsBody500Medium')
                if title_element:
                    product_data['title'] = title_element.get_text(strip=True)
                else:
                    return None
            
            # Цена
            price_element = card_element.find('span', class_='tsHeadline500Medium')
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Извлекаем числовое значение цены
                price_match = re.search(r'[\d\s]+', price_text.replace(' ', ''))
                if price_match:
                    product_data['current_price'] = int(price_match.group().replace(' ', ''))
                else:
                    product_data['current_price'] = None
            else:
                product_data['current_price'] = None
            
            # Старая цена (скидка)
            old_price_element = card_element.find('span', class_='tsBodyControl400Small')
            if old_price_element:
                old_price_text = old_price_element.get_text(strip=True)
                old_price_match = re.search(r'[\d\s]+', old_price_text.replace(' ', ''))
                if old_price_match:
                    product_data['old_price'] = int(old_price_match.group().replace(' ', ''))
                else:
                    product_data['old_price'] = None
            else:
                product_data['old_price'] = None
            
            # Рейтинг
            rating_element = card_element.find('span', class_='tsBodyControl400Small')
            if rating_element:
                rating_text = rating_element.get_text(strip=True)
                rating_match = re.search(r'[\d,]+', rating_text)
                if rating_match:
                    product_data['rating'] = float(rating_match.group().replace(',', '.'))
                else:
                    product_data['rating'] = None
            else:
                product_data['rating'] = None
            
            # Проверяем, что у нас есть хотя бы название и цена
            if product_data.get('title') and product_data.get('current_price'):
                return product_data
            else:
                return None
                
        except Exception as e:
            logger.error(f"Ошибка при парсинге карточки товара: {e}")
            return None
    
    def parse_page(self, url: str) -> List[Dict]:
        """Парсит страницу с товарами"""
        try:
            logger.info(f"Парсинг страницы: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Ищем карточки товаров
            product_cards = soup.find_all('div', {'data-widget': 'searchResultsV2'})
            
            if not product_cards:
                # Альтернативный поиск карточек
                product_cards = soup.find_all('div', class_='tile-root')
            
            logger.info(f"Найдено карточек товаров: {len(product_cards)}")
            
            for card in product_cards:
                product_data = self.parse_product_card(card)
                if product_data:
                    products.append(product_data)
            
            return products
            
        except requests.RequestException as e:
            logger.error(f"Ошибка при загрузке страницы {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Ошибка при парсинге страницы {url}: {e}")
            return []
    
    def parse_category(self, category: str, max_pages: int = 5) -> List[Dict]:
        """Парсит категорию товаров с поддержкой пагинации"""
        all_products = []
        base_url = self.get_category_url(category)
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}&page={page}"
            
            logger.info(f"Парсинг страницы {page} из {max_pages}")
            products = self.parse_page(url)
            
            if not products:
                logger.warning(f"На странице {page} не найдено товаров, завершаем парсинг")
                break
            
            all_products.extend(products)
            logger.info(f"Собрано товаров на странице {page}: {len(products)}")
            
            # Пауза между запросами
            time.sleep(1)
        
        logger.info(f"Всего собрано товаров: {len(all_products)}")
        return all_products
    
    def save_to_excel(self, products: List[Dict], filename: str = "ozon_products.xlsx"):
        """Сохраняет данные в Excel файл"""
        if not products:
            logger.warning("Нет данных для сохранения")
            return
        
        df = pd.DataFrame(products)
        
        # Добавляем колонку с датой сбора данных
        df['date_collected'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Переупорядочиваем колонки
        columns_order = ['title', 'current_price', 'old_price', 'rating', 'url', 'date_collected']
        df = df.reindex(columns=columns_order)
        
        # Сохраняем в Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        logger.info(f"Данные сохранены в файл: {filename}")
        
        return df
    
    def save_to_csv(self, products: List[Dict], filename: str = "ozon_products.csv"):
        """Сохраняет данные в CSV файл"""
        if not products:
            logger.warning("Нет данных для сохранения")
            return
        
        df = pd.DataFrame(products)
        df['date_collected'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        
        columns_order = ['title', 'current_price', 'old_price', 'rating', 'url', 'date_collected']
        df = df.reindex(columns=columns_order)
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"Данные сохранены в файл: {filename}")
        
        return df
