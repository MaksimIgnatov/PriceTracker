"""
Анализатор цен и создатель графиков для данных Ozon
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import List, Dict, Optional
import logging

# Настройка для корректного отображения русского текста
plt.rcParams['font.family'] = [
    'DejaVu Sans', 'Arial Unicode MS', 'sans-serif'
]
plt.rcParams['axes.unicode_minus'] = False

logger = logging.getLogger(__name__)


class PriceAnalyzer:
    """Класс для анализа цен и создания графиков"""
    
    def __init__(self):
        self.data = None
        self.output_dir = "charts"
        
        # Создаем папку для графиков
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_data(self, filename: str) -> pd.DataFrame:
        """Загружает данные из Excel или CSV файла"""
        try:
            if filename.endswith('.xlsx'):
                self.data = pd.read_excel(filename)
            elif filename.endswith('.csv'):
                self.data = pd.read_csv(filename)
            else:
                raise ValueError("Поддерживаются только файлы .xlsx и .csv")
            
            # Преобразуем дату в datetime
            if 'date_collected' in self.data.columns:
                self.data['date_collected'] = pd.to_datetime(self.data['date_collected'])
            
            logger.info(f"Загружено {len(self.data)} записей из файла {filename}")
            return self.data
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            return None
    
    def get_basic_statistics(self) -> Dict:
        """Возвращает базовую статистику по ценам"""
        if self.data is None or self.data.empty:
            return {}
        
        stats = {}
        
        # Статистика по текущим ценам
        if 'current_price' in self.data.columns:
            current_prices = self.data['current_price'].dropna()
            if not current_prices.empty:
                stats['current_price'] = {
                    'count': len(current_prices),
                    'mean': current_prices.mean(),
                    'median': current_prices.median(),
                    'min': current_prices.min(),
                    'max': current_prices.max(),
                    'std': current_prices.std()
                }
        
        # Статистика по старым ценам (скидки)
        if 'old_price' in self.data.columns:
            old_prices = self.data['old_price'].dropna()
            if not old_prices.empty:
                stats['old_price'] = {
                    'count': len(old_prices),
                    'mean': old_prices.mean(),
                    'median': old_prices.median(),
                    'min': old_prices.min(),
                    'max': old_prices.max(),
                    'std': old_prices.std()
                }
        
        # Статистика по рейтингам
        if 'rating' in self.data.columns:
            ratings = self.data['rating'].dropna()
            if not ratings.empty:
                stats['rating'] = {
                    'count': len(ratings),
                    'mean': ratings.mean(),
                    'median': ratings.median(),
                    'min': ratings.min(),
                    'max': ratings.max(),
                    'std': ratings.std()
                }
        
        return stats
    
    def create_price_distribution_chart(self, save_path: Optional[str] = None) -> str:
        """Создает график распределения цен"""
        if self.data is None or 'current_price' not in self.data.columns:
            logger.warning("Нет данных о ценах для создания графика")
            return None
        
        current_prices = self.data['current_price'].dropna()
        if current_prices.empty:
            logger.warning("Нет данных о ценах")
            return None
        
        plt.figure(figsize=(12, 8))
        
        # Гистограмма распределения цен
        plt.subplot(2, 2, 1)
        plt.hist(current_prices, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Распределение цен', fontsize=14, fontweight='bold')
        plt.xlabel('Цена (руб.)')
        plt.ylabel('Количество товаров')
        plt.grid(True, alpha=0.3)
        
        # Box plot цен
        plt.subplot(2, 2, 2)
        plt.boxplot(current_prices, vert=True)
        plt.title('Box Plot цен', fontsize=14, fontweight='bold')
        plt.ylabel('Цена (руб.)')
        plt.grid(True, alpha=0.3)
        
        # Топ-10 самых дорогих товаров
        plt.subplot(2, 2, 3)
        top_expensive = self.data.nlargest(10, 'current_price')[['title', 'current_price']]
        plt.barh(range(len(top_expensive)), top_expensive['current_price'])
        plt.yticks(range(len(top_expensive)), 
                  [title[:30] + '...' if len(title) > 30 else title 
                   for title in top_expensive['title']])
        plt.title('Топ-10 самых дорогих товаров', fontsize=14, fontweight='bold')
        plt.xlabel('Цена (руб.)')
        
        # Топ-10 самых дешевых товаров
        plt.subplot(2, 2, 4)
        top_cheap = self.data.nsmallest(10, 'current_price')[['title', 'current_price']]
        plt.barh(range(len(top_cheap)), top_cheap['current_price'])
        plt.yticks(range(len(top_cheap)), 
                  [title[:30] + '...' if len(title) > 30 else title 
                   for title in top_cheap['title']])
        plt.title('Топ-10 самых дешевых товаров', fontsize=14, fontweight='bold')
        plt.xlabel('Цена (руб.)')
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'price_distribution.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"График распределения цен сохранен: {save_path}")
        return save_path
    
    def create_rating_analysis_chart(self, save_path: Optional[str] = None) -> str:
        """Создает график анализа рейтингов"""
        if self.data is None or 'rating' not in self.data.columns:
            logger.warning("Нет данных о рейтингах для создания графика")
            return None
        
        ratings = self.data['rating'].dropna()
        if ratings.empty:
            logger.warning("Нет данных о рейтингах")
            return None
        
        plt.figure(figsize=(12, 8))
        
        # Распределение рейтингов
        plt.subplot(2, 2, 1)
        plt.hist(ratings, bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
        plt.title('Распределение рейтингов', fontsize=14, fontweight='bold')
        plt.xlabel('Рейтинг')
        plt.ylabel('Количество товаров')
        plt.grid(True, alpha=0.3)
        
        # Box plot рейтингов
        plt.subplot(2, 2, 2)
        plt.boxplot(ratings, vert=True)
        plt.title('Box Plot рейтингов', fontsize=14, fontweight='bold')
        plt.ylabel('Рейтинг')
        plt.grid(True, alpha=0.3)
        
        # Корреляция цена-рейтинг
        plt.subplot(2, 2, 3)
        if 'current_price' in self.data.columns:
            price_rating_data = self.data[['current_price', 'rating']].dropna()
            if not price_rating_data.empty:
                plt.scatter(price_rating_data['current_price'], price_rating_data['rating'], 
                           alpha=0.6, color='purple')
                plt.title('Корреляция цена-рейтинг', fontsize=14, fontweight='bold')
                plt.xlabel('Цена (руб.)')
                plt.ylabel('Рейтинг')
                plt.grid(True, alpha=0.3)
        
        # Топ товаров по рейтингу
        plt.subplot(2, 2, 4)
        top_rated = self.data.nlargest(10, 'rating')[['title', 'rating']]
        plt.barh(range(len(top_rated)), top_rated['rating'], color='gold')
        plt.yticks(range(len(top_rated)), 
                  [title[:30] + '...' if len(title) > 30 else title 
                   for title in top_rated['title']])
        plt.title('Топ-10 товаров по рейтингу', fontsize=14, fontweight='bold')
        plt.xlabel('Рейтинг')
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'rating_analysis.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"График анализа рейтингов сохранен: {save_path}")
        return save_path
    
    def create_discount_analysis_chart(self, save_path: Optional[str] = None) -> str:
        """Создает график анализа скидок"""
        if self.data is None:
            logger.warning("Нет данных для создания графика скидок")
            return None
        
        # Фильтруем товары со скидками
        discount_data = self.data[
            (self.data['old_price'].notna()) & 
            (self.data['current_price'].notna()) &
            (self.data['old_price'] > self.data['current_price'])
        ].copy()
        
        if discount_data.empty:
            logger.warning("Нет товаров со скидками")
            return None
        
        # Вычисляем размер скидки
        discount_data['discount_amount'] = discount_data['old_price'] - discount_data['current_price']
        discount_data['discount_percent'] = (discount_data['discount_amount'] / discount_data['old_price']) * 100
        
        plt.figure(figsize=(12, 8))
        
        # Распределение размеров скидок
        plt.subplot(2, 2, 1)
        plt.hist(discount_data['discount_percent'], bins=20, alpha=0.7, color='orange', edgecolor='black')
        plt.title('Распределение размеров скидок (%)', fontsize=14, fontweight='bold')
        plt.xlabel('Размер скидки (%)')
        plt.ylabel('Количество товаров')
        plt.grid(True, alpha=0.3)
        
        # Топ скидок по сумме
        plt.subplot(2, 2, 2)
        top_discounts = discount_data.nlargest(10, 'discount_amount')[['title', 'discount_amount']]
        plt.barh(range(len(top_discounts)), top_discounts['discount_amount'], color='red')
        plt.yticks(range(len(top_discounts)), 
                  [title[:30] + '...' if len(title) > 30 else title 
                   for title in top_discounts['title']])
        plt.title('Топ-10 скидок по сумме', fontsize=14, fontweight='bold')
        plt.xlabel('Размер скидки (руб.)')
        
        # Топ скидок по проценту
        plt.subplot(2, 2, 3)
        top_discounts_pct = discount_data.nlargest(10, 'discount_percent')[['title', 'discount_percent']]
        plt.barh(range(len(top_discounts_pct)), top_discounts_pct['discount_percent'], color='green')
        plt.yticks(range(len(top_discounts_pct)), 
                  [title[:30] + '...' if len(title) > 30 else title 
                   for title in top_discounts_pct['title']])
        plt.title('Топ-10 скидок по проценту', fontsize=14, fontweight='bold')
        plt.xlabel('Размер скидки (%)')
        
        # Корреляция цена-скидка
        plt.subplot(2, 2, 4)
        plt.scatter(discount_data['current_price'], discount_data['discount_percent'], 
                   alpha=0.6, color='purple')
        plt.title('Корреляция цена-скидка', fontsize=14, fontweight='bold')
        plt.xlabel('Текущая цена (руб.)')
        plt.ylabel('Размер скидки (%)')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'discount_analysis.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"График анализа скидок сохранен: {save_path}")
        return save_path
    
    def create_summary_report(self, save_path: Optional[str] = None) -> str:
        """Создает сводный отчет с основными метриками"""
        if self.data is None or self.data.empty:
            logger.warning("Нет данных для создания отчета")
            return None
        
        stats = self.get_basic_statistics()
        
        plt.figure(figsize=(12, 10))
        
        # Сводная информация
        plt.subplot(2, 2, 1)
        plt.axis('off')
        
        report_text = f"""
        СВОДНЫЙ ОТЧЕТ ПО ДАННЫМ OZON
        
        Общее количество товаров: {len(self.data)}
        
        ЦЕНЫ:
        • Средняя цена: {stats.get('current_price', {}).get('mean', 0):.0f} руб.
        • Медианная цена: {stats.get('current_price', {}).get('median', 0):.0f} руб.
        • Минимальная цена: {stats.get('current_price', {}).get('min', 0):.0f} руб.
        • Максимальная цена: {stats.get('current_price', {}).get('max', 0):.0f} руб.
        
        РЕЙТИНГИ:
        • Средний рейтинг: {stats.get('rating', {}).get('mean', 0):.2f}
        • Медианный рейтинг: {stats.get('rating', {}).get('median', 0):.2f}
        
        СКИДКИ:
        • Товаров со скидкой: {len(self.data[self.data['old_price'].notna()])}
        """
        
        plt.text(0.1, 0.9, report_text, transform=plt.gca().transAxes, 
                fontsize=12, verticalalignment='top', fontfamily='monospace')
        
        # Круговая диаграмма по наличию скидок
        plt.subplot(2, 2, 2)
        discount_count = len(self.data[self.data['old_price'].notna()])
        no_discount_count = len(self.data) - discount_count
        
        plt.pie([discount_count, no_discount_count], 
                labels=['Со скидкой', 'Без скидки'],
                autopct='%1.1f%%',
                colors=['lightcoral', 'lightblue'])
        plt.title('Распределение товаров по наличию скидок')
        
        # Гистограмма цен
        plt.subplot(2, 2, 3)
        if 'current_price' in self.data.columns:
            current_prices = self.data['current_price'].dropna()
            if not current_prices.empty:
                plt.hist(current_prices, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                plt.title('Распределение цен')
                plt.xlabel('Цена (руб.)')
                plt.ylabel('Количество товаров')
                plt.grid(True, alpha=0.3)
        
        # Гистограмма рейтингов
        plt.subplot(2, 2, 4)
        if 'rating' in self.data.columns:
            ratings = self.data['rating'].dropna()
            if not ratings.empty:
                plt.hist(ratings, bins=15, alpha=0.7, color='lightgreen', edgecolor='black')
                plt.title('Распределение рейтингов')
                plt.xlabel('Рейтинг')
                plt.ylabel('Количество товаров')
                plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'summary_report.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Сводный отчет сохранен: {save_path}")
        return save_path
    
    def create_all_charts(self) -> List[str]:
        """Создает все доступные графики"""
        charts = []
        
        # Создаем все графики
        chart_methods = [
            self.create_price_distribution_chart,
            self.create_rating_analysis_chart,
            self.create_discount_analysis_chart,
            self.create_summary_report
        ]
        
        for method in chart_methods:
            try:
                chart_path = method()
                if chart_path:
                    charts.append(chart_path)
            except Exception as e:
                logger.error(f"Ошибка при создании графика {method.__name__}: {e}")
        
        logger.info(f"Создано графиков: {len(charts)}")
        return charts
