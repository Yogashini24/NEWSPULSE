"""
NewsPulse Sentiment Prediction Module
Lightweight sentiment predictor for dashboard usage
Python 3.11+ recommended
"""
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentPredictor:
    """Lightweight sentiment predictor for dashboard usage"""
    
    def __init__(self, model_path='./models/sentiment_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.sentiment_pipeline = None
        self.initialize()
    
    def initialize(self):
        """Initialize the sentiment predictor"""
        try:
            # Try to load saved model
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info("Loaded saved sentiment model")
            else:
                # Use pre-trained transformer model (CPU mode to avoid DLL issues)
                from transformers import pipeline
                
                self.sentiment_pipeline = pipeline(
                    'sentiment-analysis',
                    model='distilbert-base-uncased-finetuned-sst-2-english',
                    device=-1  # Use CPU only
                )
                logger.info("Initialized sentiment pipeline from transformers (CPU mode)")
        except ImportError as e:
            logger.error(f"ImportError during initialization: {str(e)}")
            try:
                from transformers import pipeline
                self.sentiment_pipeline = pipeline(
                    'sentiment-analysis',
                    model='distilbert-base-uncased-finetuned-sst-2-english',
                    device=-1
                )
            except Exception as e2:
                logger.error(f"Fallback initialization failed: {str(e2)}")
        except Exception as e:
            logger.error(f"Error initializing sentiment predictor: {str(e)}")
            try:
                from transformers import pipeline
                self.sentiment_pipeline = pipeline(
                    'sentiment-analysis',
                    model='distilbert-base-uncased-finetuned-sst-2-english',
                    device=-1
                )
            except:
                logger.error("Failed to initialize with transformers")
    
    def preprocess_text(self, text):
        """Preprocess text for sentiment analysis"""
        if not isinstance(text, str):
            return ''
        
        # Clean text
        text = ' '.join(text.split()).lower().strip()
        
        # Truncate to first 100 words to comply with model limits
        words = text.split()
        if len(words) > 100:
            text = ' '.join(words[:100])
        
        return text
    
    def predict(self, text):
        """Predict sentiment of given text"""
        try:
            cleaned_text = self.preprocess_text(text)
            
            if not cleaned_text or len(cleaned_text) < 3:
                return {
                    'label': 'neutral',
                    'sentiment': 'neutral',
                    'confidence': 0.33,
                    'score': 0.0,
                    'raw_score': 0.0
                }
            
            # Use model if available, otherwise use pipeline
            if self.model and hasattr(self.model, 'predict'):
                result = self.model.predict(cleaned_text)
                return {
                    'label': result.get('label', 'neutral'),
                    'sentiment': result.get('label', 'neutral'),
                    'confidence': result.get('confidence', 0.5),
                    'score': result.get('raw_score', 0.0),
                    'raw_score': result.get('raw_score', 0.0)
                }
            else:
                # Use transformer pipeline
                result = self.sentiment_pipeline(cleaned_text)[0]
                
                label = result['label'].upper()
                score = result['score']
                
                # Map to sentiment labels
                if 'POSITIVE' in label:
                    sentiment = 'positive'
                    confidence = score
                elif 'NEGATIVE' in label:
                    sentiment = 'negative'
                    confidence = score
                else:
                    sentiment = 'neutral'
                    confidence = score
                
                return {
                    'label': sentiment,
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'score': score,
                    'raw_score': score
                }
        
        except Exception as e:
            logger.error(f"Error in sentiment prediction: {str(e)}")
            return {
                'label': 'neutral',
                'sentiment': 'neutral',
                'confidence': 0.33,
                'score': 0.0,
                'raw_score': 0.0,
                'error': str(e)
            }
    
    def batch_predict(self, texts):
        """Predict sentiment for multiple texts"""
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
    
    def get_sentiment_distribution(self, texts):
        """Get distribution of sentiments in batch"""
        predictions = self.batch_predict(texts)
        
        distribution = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        total_confidence = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        for pred in predictions:
            sentiment = pred.get('sentiment', 'neutral')
            confidence = pred.get('confidence', 0)
            distribution[sentiment] += 1
            total_confidence[sentiment] += confidence
        
        # Calculate percentages
        total = len(texts)
        percentages = {
            'positive': (distribution['positive'] / total * 100) if total > 0 else 0,
            'negative': (distribution['negative'] / total * 100) if total > 0 else 0,
            'neutral': (distribution['neutral'] / total * 100) if total > 0 else 0
        }
        
        # Average confidence
        avg_confidence = {}
        for sentiment in distribution:
            count = distribution[sentiment]
            avg_confidence[sentiment] = (
                total_confidence[sentiment] / count if count > 0 else 0
            )
        
        return {
            'distribution': distribution,
            'percentages': percentages,
            'average_confidence': avg_confidence
        }


# Global predictor instance
_predictor = None


def get_predictor():
    """Get or create global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = SentimentPredictor()
    return _predictor


def predict_sentiment(text):
    """Predict sentiment of text"""
    predictor = get_predictor()
    return predictor.predict(text)


def batch_predict_sentiment(texts):
    """Batch predict sentiment"""
    predictor = get_predictor()
    return predictor.batch_predict(texts)


def get_sentiment_distribution(texts):
    """Get sentiment distribution"""
    predictor = get_predictor()
    return predictor.get_sentiment_distribution(texts)
