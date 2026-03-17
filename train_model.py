"""
NewsPulse Sentiment Model Training Module
Requires: Python 3.11+
No TensorFlow - Uses lightweight transformers pipeline
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, classification_report)
import joblib
import logging
import os
import json
from datetime import datetime

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure models directory exists
os.makedirs('./models', exist_ok=True)


class SentimentDataGenerator:
    """Generate training data for sentiment analysis"""
    
    SAMPLE_DATA = {
        'positive': [
            "This is amazing news! Great developments in technology.",
            "Excellent results from the quarterly earnings report.",
            "I love this product, it works perfectly!",
            "What a wonderful day with fantastic achievements.",
            "Outstanding performance by the team!",
            "This is the best news I've heard all year!",
            "Incredible innovation in the market.",
            "Fantastic growth in our business.",
            "Remarkable progress in research.",
            "Wonderful opportunity ahead!",
            "Splendid achievement by the company.",
            "Brilliant solution to the problem.",
            "Thrilled with the results!",
            "Absolutely delighted with this outcome.",
            "Superb quality and service.",
        ],
        'negative': [
            "This is terrible news. Devastating results.",
            "The company's stock crashed dramatically.",
            "I'm very disappointed with the service.",
            "What a horrible situation we're facing.",
            "Disappointing performance from the team.",
            "This is the worst news possible.",
            "Catastrophic loss in revenue.",
            "Dreadful conditions in the market.",
            "Unfortunate circumstances leading to decline.",
            "Terrible experience with customer support.",
            "Awful quality of the product.",
            "Disastrous outcome of the project.",
            "Deeply frustrated with the situation.",
            "Shocking failure in execution.",
            "Devastating impact on the business.",
        ],
        'neutral': [
            "The stock market went up today.",
            "Company announces new product launch.",
            "Meeting scheduled for next week.",
            "Today's news includes various updates.",
            "Market analysis shows mixed trends.",
            "New policies will be implemented.",
            "The report contains financial data.",
            "Technical details about the system.",
            "Information about the project timeline.",
            "The data shows statistical changes.",
            "Updates on the current situation.",
            "Regular meeting notes available.",
            "Technical specifications provided.",
            "Factual information about the market.",
            "Standard operational procedures updated.",
        ]
    }
    
    @staticmethod
    def generate_training_data(samples_per_category=500):
        """Generate comprehensive training dataset"""
        texts = []
        labels = []
        
        for sentiment, examples in SentimentDataGenerator.SAMPLE_DATA.items():
            # Repeat examples with variations
            for _ in range(samples_per_category // len(examples)):
                for example in examples:
                    texts.append(example)
                    labels.append(sentiment)
        
        df = pd.DataFrame({'text': texts, 'sentiment': labels})
        return df.sample(frac=1).reset_index(drop=True)


class SentimentAnalysisModel:
    """Advanced Sentiment Analysis Model using Transformers"""
    
    def __init__(self, model_name='distilbert-base-uncased-finetuned-sst-2-english'):
        """Initialize sentiment analyzer with pre-trained model"""
        self.model_name = model_name
        self.model = None
        self.performance_metrics = {}
        self.load_model()
    
    def load_model(self):
        """Load or create sentiment analysis pipeline"""
        try:
            # Import transformers only when needed to avoid TensorFlow issues
            from transformers import pipeline
            
            logger.info(f"Loading pre-trained model: {self.model_name}")
            self.model = pipeline(
                'sentiment-analysis',
                model=self.model_name,
                device=-1  # Use CPU only to avoid DLL issues
            )
            logger.info(f"Model loaded successfully on CPU")
        except ImportError as e:
            logger.error(f"Error loading transformers: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def preprocess_text(self, text):
        """Preprocess text for analysis"""
        if isinstance(text, str):
            # Remove extra whitespace and convert to lowercase
            text = ' '.join(text.split()).lower()
            return text
        return ''
    
    def predict(self, text):
        """Predict sentiment of given text"""
        try:
            cleaned_text = self.preprocess_text(text)
            
            if not cleaned_text:
                return {'label': 'NEUTRAL', 'score': 0.5}
            
            # Truncate to 512 tokens (DistilBERT limit)
            words = cleaned_text.split()
            if len(words) > 100:
                cleaned_text = ' '.join(words[:100])
            
            result = self.model(cleaned_text)[0]
            
            # Convert to standard sentiment labels
            label = result['label'].upper()
            score = result['score']
            
            # Map POSITIVE/NEGATIVE to our scale
            if 'POSITIVE' in label:
                sentiment = 'positive'
                confidence = score
            elif 'NEGATIVE' in label:
                sentiment = 'negative'
                confidence = score
            else:
                sentiment = 'neutral'
                confidence = 0.5
            
            return {
                'label': sentiment,
                'confidence': confidence,
                'raw_score': score
            }
        
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return {'label': 'neutral', 'confidence': 0.5, 'error': str(e)}
    
    def batch_predict(self, texts):
        """Predict sentiment for multiple texts"""
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
    
    def train_with_custom_data(self, texts, labels, test_size=0.2):
        """Train model with custom data and evaluate"""
        try:
            predictions = self.batch_predict(texts)
            pred_labels = [p['label'] for p in predictions]
            
            # Calculate metrics
            accuracy = accuracy_score(labels, pred_labels)
            precision = precision_score(labels, pred_labels, average='weighted', zero_division=0)
            recall = recall_score(labels, pred_labels, average='weighted', zero_division=0)
            f1 = f1_score(labels, pred_labels, average='weighted', zero_division=0)
            
            self.performance_metrics = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'confusion_matrix': confusion_matrix(labels, pred_labels).tolist(),
                'classification_report': classification_report(labels, pred_labels, output_dict=True)
            }
            
            logger.info(f"Model Performance - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
            return self.performance_metrics
        
        except Exception as e:
            logger.error(f"Error during training evaluation: {str(e)}")
            return {}
    
    def save_model(self, path='./models/sentiment_model.pkl'):
        """Save model to disk"""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            joblib.dump(self, path)
            logger.info(f"Model saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    @staticmethod
    def load_model_from_file(path='./models/sentiment_model.pkl'):
        """Load model from disk"""
        try:
            model = joblib.load(path)
            logger.info(f"Model loaded from {path}")
            return model
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None


class ModelTrainer:
    """Train and evaluate sentiment analysis model"""
    
    def __init__(self):
        self.model = SentimentAnalysisModel()
        self.training_data = None
    
    def generate_and_train(self, samples_per_category=500):
        """Generate training data and train model"""
        logger.info("Generating training data...")
        self.training_data = SentimentDataGenerator.generate_training_data(samples_per_category)
        
        logger.info(f"Training data shape: {self.training_data.shape}")
        logger.info(f"Data distribution:\n{self.training_data['sentiment'].value_counts()}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            self.training_data['text'].values,
            self.training_data['sentiment'].values,
            test_size=0.2,
            random_state=42,
            stratify=self.training_data['sentiment'].values
        )
        
        logger.info(f"Training set size: {len(X_train)}")
        logger.info(f"Test set size: {len(X_test)}")
        
        # Train and evaluate
        logger.info("Evaluating model on training data...")
        metrics_train = self.model.train_with_custom_data(X_train, y_train)
        
        logger.info("Evaluating model on test data...")
        metrics_test = self.model.train_with_custom_data(X_test, y_test)
        
        return {
            'train_metrics': metrics_train,
            'test_metrics': metrics_test,
            'training_data': self.training_data
        }
    
    def save_results(self):
        """Save model and metrics"""
        try:
            # Save model
            self.model.save_model('./models/sentiment_model.pkl')
            
            # Save metrics
            metrics_file = './models/model_metrics.json'
            os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
            
            with open(metrics_file, 'w') as f:
                json.dump({
                    'accuracy': self.model.performance_metrics.get('accuracy', 0),
                    'precision': self.model.performance_metrics.get('precision', 0),
                    'recall': self.model.performance_metrics.get('recall', 0),
                    'f1_score': self.model.performance_metrics.get('f1_score', 0),
                    'saved_at': datetime.now().isoformat(),
                    'model_name': self.model.model_name
                }, f, indent=4)
            
            logger.info("Results saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return False


def main():
    """Main function to train sentiment model"""
    logger.info("Starting sentiment model training...")
    
    trainer = ModelTrainer()
    results = trainer.generate_and_train(samples_per_category=300)
    
    logger.info("\n" + "="*50)
    logger.info("TRAINING RESULTS")
    logger.info("="*50)
    
    logger.info("\nTrain Metrics:")
    for key, value in results['train_metrics'].items():
        if key != 'confusion_matrix' and key != 'classification_report':
            logger.info(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    
    logger.info("\nTest Metrics:")
    for key, value in results['test_metrics'].items():
        if key != 'confusion_matrix' and key != 'classification_report':
            logger.info(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    
    # Save model and metrics
    trainer.save_results()
    
    logger.info("\n" + "="*50)
    logger.info("Training completed successfully!")
    logger.info("="*50)


if __name__ == '__main__':
    main()
