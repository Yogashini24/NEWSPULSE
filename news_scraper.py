"""
NewsPulse News Scraper Module
Requires: Python 3.11+
"""
import requests
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'YOUR_API_KEY_HERE')
BASE_URL = 'https://newsapi.org/v2'
DATABASE_PATH = os.getenv('DATABASE_PATH', './data/newspulse.db')

# Ensure data directory exists
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)


class NewsAPIConfig:
    """Configuration for different news categories"""
    CATEGORIES = {
        'business': 'business',
        'entertainment': 'entertainment',
        'health': 'health',
        'science': 'science',
        'sports': 'sports',
        'technology': 'technology',
        'general': 'general'
    }
    
    SENTIMENT_CATEGORIES = {
        'politics': ['politics', 'election', 'government', 'law'],
        'finance': ['stock', 'market', 'investment', 'crypto'],
        'health': ['health', 'medical', 'disease', 'vaccine'],
        'environment': ['climate', 'pollution', 'renewable', 'environmental'],
        'technology': ['ai', 'tech', 'innovation', 'software'],
        'culture': ['entertainment', 'culture', 'art', 'sports']
    }


class NewsScraperDatabase:
    """Handle database operations for news storage"""
    
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create news table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                content TEXT,
                url TEXT UNIQUE,
                image_url TEXT,
                source TEXT,
                author TEXT,
                published_at TIMESTAMP,
                category TEXT,
                sentiment_score REAL,
                sentiment_label TEXT,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create sentiment cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentiment_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_hash TEXT UNIQUE,
                sentiment_score REAL,
                sentiment_label TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create keywords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE,
                frequency INTEGER DEFAULT 1,
                category TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def insert_news(self, news_data):
        """Insert news articles into database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO news 
                (title, description, content, url, image_url, source, author, published_at, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                news_data.get('title'),
                news_data.get('description'),
                news_data.get('content'),
                news_data.get('url'),
                news_data.get('urlToImage'),
                news_data.get('source', {}).get('name'),
                news_data.get('author'),
                news_data.get('publishedAt'),
                news_data.get('category', 'general')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error inserting news: {str(e)}")
            return False
    
    def get_all_news(self, limit=100, category=None):
        """Retrieve news from database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT * FROM news WHERE category = ? 
                ORDER BY published_at DESC LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT * FROM news 
                ORDER BY published_at DESC LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_trending_keywords(self, limit=20):
        """Get trending keywords"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT keyword, frequency, category FROM keywords 
            ORDER BY frequency DESC LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        return [{'keyword': row[0], 'frequency': row[1], 'category': row[2]} for row in rows]


class NewsScraper:
    """Scrape news from News API"""
    
    def __init__(self, api_key=NEWS_API_KEY):
        self.api_key = api_key
        self.db = NewsScraperDatabase()
        self.session = requests.Session()
    
    def fetch_news(self, category='general', page_size=100):
        """Fetch news from News API"""
        try:
            params = {
                'apiKey': self.api_key,
                'category': category,
                'pageSize': min(page_size, 100),
                'sortBy': 'publishedAt'
            }
            
            response = self.session.get(f'{BASE_URL}/top-headlines', params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                articles = []
                for article in data.get('articles', []):
                    article['category'] = category
                    self.db.insert_news(article)
                    articles.append(article)
                
                logger.info(f"Fetched {len(articles)} articles from category: {category}")
                return articles
            else:
                logger.error(f"API Error: {data.get('message')}")
                return []
        
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            return []
    
    def fetch_all_categories(self, page_size=50):
        """Fetch news from all categories"""
        all_articles = []
        for category in NewsAPIConfig.CATEGORIES.keys():
            articles = self.fetch_news(category, page_size)
            all_articles.extend(articles)
        
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles
    
    def search_news(self, query, sort_by='publishedAt', page_size=100):
        """Search news by query"""
        try:
            params = {
                'q': query,
                'apiKey': self.api_key,
                'pageSize': min(page_size, 100),
                'sortBy': sort_by
            }
            
            response = self.session.get(f'{BASE_URL}/everything', params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                for article in data.get('articles', []):
                    article['category'] = 'search'
                    self.db.insert_news(article)
                
                logger.info(f"Found {len(data['articles'])} articles for query: {query}")
                return data.get('articles', [])
            else:
                logger.error(f"API Error: {data.get('message')}")
                return []
        
        except Exception as e:
            logger.error(f"Error searching news: {str(e)}")
            return []


def main():
    """Main function to scrape news"""
    logger.info("Starting news scraping...")
    
    scraper = NewsScraper()
    
    # Fetch news from all categories
    scraper.fetch_all_categories(page_size=50)
    
    logger.info("News scraping completed successfully")
    
    # Display sample news
    news = scraper.db.get_all_news(limit=10)
    if news:
        df = pd.DataFrame(news)
        print("\nSample News Data:")
        print(df[['title', 'source', 'category', 'published_at']].head(10))


if __name__ == '__main__':
    main()
