import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import hashlib
import hmac

load_dotenv()


class AuthenticationManager:
    """Manage user authentication for NewsPulse Dashboard"""
    
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'NewsPulse@2024')
    
    @staticmethod
    def hash_password(password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_credentials(username, password):
        """Verify admin credentials"""
        if username == AuthenticationManager.ADMIN_USERNAME:
            stored_hash = AuthenticationManager.hash_password(
                AuthenticationManager.ADMIN_PASSWORD
            )
            provided_hash = AuthenticationManager.hash_password(password)
            return stored_hash == provided_hash
        return False
    
    @staticmethod
    def init_session_state():
        """Initialize session state for authentication"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'login_time' not in st.session_state:
            st.session_state.login_time = None
    
    @staticmethod
    def set_authenticated(username):
        """Set user as authenticated"""
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.login_time = datetime.now()
    
    @staticmethod
    def logout():
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.login_time = None
    
    @staticmethod
    def is_authenticated():
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_username():
        """Get current username"""
        return st.session_state.get('username', None)
    
    @staticmethod
    def get_session_duration():
        """Get session duration"""
        if st.session_state.get('login_time'):
            return datetime.now() - st.session_state.login_time
        return None


class DataProcessor:
    """Process and format data for dashboard display"""
    
    @staticmethod
    def format_timestamp(timestamp):
        """Format timestamp to readable string"""
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                return timestamp
        return str(timestamp)
    
    @staticmethod
    def extract_keywords(text, num_keywords=5):
        """Extract keywords from text"""
        try:
            from nltk import word_tokenize
            from nltk.corpus import stopwords
            import nltk
            
            # Download required NLTK data
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
            
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords', quiet=True)
            
            if not text:
                return []
            
            # Tokenize and filter
            tokens = word_tokenize(text.lower())
            stop_words = set(stopwords.words('english'))
            
            keywords = [
                word for word in tokens
                if len(word) > 3 and word.isalpha() and word not in stop_words
            ]
            
            # Return most common keywords
            from collections import Counter
            most_common = Counter(keywords).most_common(num_keywords)
            return [kw[0] for kw in most_common]
        
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return []
    
    @staticmethod
    def get_time_ago(timestamp):
        """Get time ago string"""
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                return timestamp
        else:
            dt = timestamp
        
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            if diff.days == 1:
                return "1 day ago"
            return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    @staticmethod
    def get_sentiment_emoji(sentiment):
        """Get emoji for sentiment"""
        sentiment = sentiment.lower()
        if sentiment == 'positive':
            return '😊'
        elif sentiment == 'negative':
            return '😞'
        else:
            return '😐'
    
    @staticmethod
    def truncate_text(text, max_length=150):
        """Truncate text to max length"""
        if isinstance(text, str) and len(text) > max_length:
            return text[:max_length] + "..."
        return text


class CacheManager:
    """Manage caching for dashboard data"""
    
    @staticmethod
    @st.cache_resource
    def load_news_data(limit=1000):
        """Cache news data"""
        try:
            from news_scraper import NewsScraperDatabase
            db = NewsScraperDatabase()
            return db.get_all_news(limit=limit)
        except Exception as e:
            print(f"Error loading news data: {str(e)}")
            return []
    
    @staticmethod
    @st.cache_resource
    def load_sentiment_model():
        """Cache sentiment model"""
        try:
            from sentiment_predictor import get_predictor
            return get_predictor()
        except Exception as e:
            print(f"Error loading sentiment model: {str(e)}")
            return None
    
    @staticmethod
    def clear_all_cache():
        """Clear all cached data"""
        st.cache_resource.clear()


class MetricsCalculator:
    """Calculate various metrics for dashboard"""
    
    @staticmethod
    def calculate_sentiment_distribution(sentiment_predictions):
        """Calculate sentiment distribution"""
        if not sentiment_predictions:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        
        distribution = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for pred in sentiment_predictions:
            sentiment = pred.get('label', 'neutral').lower()
            if sentiment in distribution:
                distribution[sentiment] += 1
        
        total = sum(distribution.values())
        percentages = {
            k: (v / total * 100) if total > 0 else 0
            for k, v in distribution.items()
        }
        
        return {
            'counts': distribution,
            'percentages': percentages,
            'total': total
        }
    
    @staticmethod
    def get_trending_topics(news_items, top_n=10):
        """Get trending topics from news items"""
        from collections import Counter
        from nltk.corpus import stopwords
        import nltk
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        all_keywords = []
        stop_words = set(stopwords.words('english'))
        
        for item in news_items:
            title = item.get('title', '')
            if title:
                words = title.lower().split()
                filtered = [
                    w for w in words
                    if len(w) > 3 and w.isalpha() and w not in stop_words
                ]
                all_keywords.extend(filtered)
        
        counter = Counter(all_keywords)
        return dict(counter.most_common(top_n))
    
    @staticmethod
    def get_source_distribution(news_items):
        """Get distribution of news by source"""
        from collections import Counter
        
        sources = [item.get('source', 'Unknown') for item in news_items]
        return dict(Counter(sources).most_common(15))
    
    @staticmethod
    def get_category_distribution(news_items):
        """Get distribution of news by category"""
        from collections import Counter
        
        categories = [item.get('category', 'general') for item in news_items]
        return dict(Counter(categories))


class NewsArticleFormatter:
    """Format news articles for display"""
    
    @staticmethod
    def format_article_for_display(article, sentiment=None):
        """Format article for dashboard display"""
        return {
            'title': article.get('title', 'No Title'),
            'description': article.get('description', 'No description available'),
            'content': article.get('content', ''),
            'source': article.get('source', 'Unknown'),
            'author': article.get('author', 'Unknown'),
            'url': article.get('url', ''),
            'image_url': article.get('image_url', ''),
            'published_at': DataProcessor.format_timestamp(article.get('published_at', '')),
            'time_ago': DataProcessor.get_time_ago(article.get('published_at', '')),
            'category': article.get('category', 'general'),
            'sentiment': sentiment
        }
    
    @staticmethod
    def display_article_card(article, col=None, show_sentiment=True):
        """Display article as a card"""
        container = col if col else st.container()
        
        with container:
            title_html = f"""
            <p style="
                color: #39FF14;
                font-size: 1.15em;
                font-weight: 600;
                font-family: Playfair Display, serif;
                margin: 0;
            ">{article['title']}</p>
            """
            st.markdown(title_html, unsafe_allow_html=True)
            
            meta_html = f"""
            <p style="
                color: #A0AEC0;
                font-size: 0.9em;
                margin: 5px 0;
            ">
                📰 {article['source']} | ⏱️ {article['time_ago']}
            </p>
            """
            st.markdown(meta_html, unsafe_allow_html=True)
            
            st.caption(article['description'][:200] + "..." if len(article.get('description', '')) > 200 else article.get('description', ''))
            
            if show_sentiment and article.get('sentiment'):
                sentiment = article['sentiment']
                emoji = DataProcessor.get_sentiment_emoji(sentiment.get('label', 'neutral'))
                color = '#4ADE80' if sentiment.get('label') == 'positive' else '#F87171' if sentiment.get('label') == 'negative' else '#60A5FA'
                
                sentiment_html = f"""
                <p style="color: {color}; font-weight: 600;">
                    {emoji} {sentiment.get('label', 'neutral').upper()} ({sentiment.get('confidence', 0):.0%})
                </p>
                """
                st.markdown(sentiment_html, unsafe_allow_html=True)
            
            if article['url']:
                st.markdown(f"[Read Full Article →]({article['url']})")
            
            st.divider()
