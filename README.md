
# NewsPulse - Advanced News Analytics Dashboard

## 📰 Overview

NewsPulse is a professional, web-based news analytics dashboard built with Streamlit. It provides comprehensive insights into news trends, sentiment analysis, and trending topics with a modern, professional UI using a custom theme with Playfair Display and Lora fonts.

### Key Features

- **👤 Secure Admin Login** - Protected dashboard with authentication
- **🔥 Recent & Trending News** - Latest news with sentiment analysis
- **🔤 Trending Keywords & Topics** - Discover most discussed subjects
- **😊 Sentiment Analysis** - Comprehensive sentiment distribution
- **📈 Model Performance Metrics** - Sentiment model accuracy metrics
- **📋 Overall Summary** - Complete overview with advanced analytics
- **☁️ Interactive Visualizations** - Word clouds, charts, and graphs
- **🎨 Professional Theme** - Modern dark theme with neon accents

## 🚀 Quick Start

### Prerequisites
- **Python 3.11** or higher (required)
- pip (Python package manager)

### Installation

1. **Clone/Download the project:**
```bash
cd "c:\Users\ANANTAN\Desktop\milestone 3"
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

4. **Create `.env` file with API key:**
```
NEWS_API_KEY=your_news_api_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=NewsPulse@2024
```

Get your free News API key from: https://newsapi.org/

### Running the Application

1. **Fetch news data:**
```bash
python news_scraper.py
```

2. **Train sentiment model:**
```bash
python train_model.py
```

3. **Run the dashboard:**
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Dashboard Sections

### 1. Recent & Trending News
- View latest news articles with sentiment analysis
- Filter by category and sort options
- Display articles in list or table view
- Direct links to full articles

### 2. Trending Keywords & Topics
- Top trending keywords visualization
- Word cloud representation
- Keywords by category breakdown
- Download keyword data as CSV

### 3. Sentiment Analysis
- Overall sentiment distribution (Positive/Negative/Neutral)
- Sentiment metrics by category
- Detailed sentiment breakdown table
- Gauge charts for visualization

### 4. Model Performance Metrics
- Accuracy, Precision, Recall, F1-Score
- Detailed performance gauges
- Classification report by class
- Model information and benchmarks

### 5. Overall Summary
- Comprehensive overview of all metrics
- News distribution by category and source
- Latest news with sentiments
- Advanced analytics and statistics
- Export options (CSV, PDF, Email - future)

## 🎨 Theme & Design

### Colors
- **Background**: Charcoal (#121212) / Deep Navy (#1A202C)
- **Text**: Light Gray (#E2E8F0) / White (#FFFFFF)
- **Primary Accent**: Neon Green (#39FF14)
- **Secondary Accent**: Electric Cyan (#00FFFF)
- **Sentiments**: Green (#4ADE80), Red (#F87171), Blue (#60A5FA)

### Fonts
- **Headlines**: Playfair Display (Serif) - 3em, 2em, 1.5em
- **Body**: Lora (Serif) - 1.1em

### Components
- Glass-morphism cards with gradient borders
- Glowing titles and accents
- Smooth transitions and hover effects
- Professional metric cards
- Interactive charts and gauges

## 🔐 Authentication

**Default Credentials:**
- Username: `admin`
- Password: `NewsPulse@2024`

**Change credentials in `.env` file:**
```
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
```

## 📦 Project Structure

```
milestone 3/
├── app.py                           # Main Streamlit application
├── auth.py                          # Authentication management
├── news_scraper.py                  # News API data scraping
├── train_model.py                   # Sentiment model training
├── sentiment_predictor.py           # Sentiment prediction utility
├── theme_config.py                  # Professional theme configuration
├── utils.py                         # Utility functions
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
├── data/
│   └── newspulse.db                # SQLite database
├── models/
│   ├── sentiment_model.pkl         # Trained model
│   └── model_metrics.json          # Model performance metrics
└── pages/
    ├── __init__.py
    ├── recent_trending.py          # Latest news page
    ├── trending_keywords.py        # Trending keywords page
    ├── sentiment_analysis.py       # Sentiment analysis page
    ├── model_performance.py        # Model metrics page
    └── overall_summary.py          # Summary page
```

## 🤖 Sentiment Analysis Model

**Architecture**: DistilBERT (Transformer-based)
**Classes**: 3 (Positive, Negative, Neutral)
**Performance**: 
- High accuracy sentiment classification
- Fast inference
- Pre-trained on reviews and news data

**Model Metrics Interpretation:**
- **Accuracy**: Overall correctness
- **Precision**: Accuracy of positive predictions
- **Recall**: Coverage of positive cases
- **F1-Score**: Balanced performance metric

### Training the Model

```bash
python train_model.py
```

- Generates comprehensive training dataset
- Fine-tunes the model on custom data
- Evaluates on test set
- Saves model and metrics

## 📊 Data & Database

### SQLite Database Schema

**news table**: Stores all news articles with metadata
**sentiment_cache table**: Caches sentiment predictions
**keywords table**: Stores extracted keywords and frequencies

### Scraping Process

- Fetches from News API
- Supports 7 news categories
- Stores 100+ articles per scraping session
- Extracts keywords automatically

## 💡 Usage Tips

1. **First Run**: Run `python news_scraper.py` to fetch initial data
2. **Train Model**: Run `python train_model.py` to train sentiment model
3. **Dashboard**: Run `streamlit run app.py` to start the dashboard
4. **Regular Updates**: Schedule news_scraper.py to run periodically for fresh data

## 🔧 Configuration

### News Categories Supported
- Business
- Entertainment
- Health
- Science
- Sports
- Technology
- General

### Sentiment Categories
- Politics
- Finance
- Health
- Environment
- Technology
- Culture

## 📈 Advanced Features

### Word Cloud
Interactive visualization of trending keywords

### Interactive Charts
- Plotly-based visualizations
- Hover tooltips
- Downloadable as images

### Export Options
- CSV export for data
- PDF reports (future)
- Email distribution (future)

## 🐛 Troubleshooting

### Issue: "No news data available"
**Solution**: Run `python news_scraper.py` first

### Issue: "Model not found"
**Solution**: Run `python train_model.py` to train the model

### Issue: "API Key Error"
**Solution**: Make sure your News API key is set in `.env` file

### Issue: Streamlit not found
**Solution**: Run `pip install streamlit`

## 📝 News API Setup

1. Visit: https://newsapi.org/
2. Sign up for a free account
3. Get your API key
4. Add to `.env` file: `NEWS_API_KEY=your_key_here`

### Free Tier Limits
- 100 requests per day
- 30 days of historical data
- Basic news sources

## 🔄 Data Flow

```
News API
    ↓
news_scraper.py (Fetches & Stores)
    ↓
SQLite Database
    ↓
Streamlit Dashboard
    ├─ sentiment_predictor.py (Analyzes)
    ├─ train_model.py (Trains)
    └─ Pages (Display)
```

## 🌟 Future Enhancements

- [ ] Real-time news updates
- [ ] Advanced NLP features
- [ ] PDF report generation
- [ ] Email notifications
- [ ] User customization
- [ ] More sentiment categories
- [ ] Social media integration
- [ ] Trend prediction

## 📜 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Verify dependencies installation
3. Review error messages in terminal
4. Check `.env` configuration

## 📚 References

- **Streamlit**: https://streamlit.io/
- **News API**: https://newsapi.org/
- **Transformers**: https://huggingface.co/transformers/
- **NLTK**: https://www.nltk.org/

---

**Created by**: NewsPulse Team
**Version**: 1.0.0
**Last Updated**: March 2026
=======
# NewsPulse – Global News Trend Analyzer using AI

## Overview
NewsPulse is an AI-powered system that automatically collects global news articles and analyzes them to detect trending topics and sentiment patterns using Natural Language Processing.

## Features
- Automated news data collection using APIs
- Text preprocessing and cleaning
- Tokenization and stopword removal
- Feature extraction using TF-IDF
- Topic modeling using LDA
- Sentiment analysis using TextBlob
- Trend detection using keyword frequency
- Interactive Streamlit dashboard

## Tech Stack
Python
NLP
TF-IDF
LDA
TextBlob
Streamlit

## Project Pipeline
News API → Data Cleaning → NLP Processing → Trend Detection → Sentiment Analysis → Dashboard

## Installation

Clone repository
git clone https://github.com/Yogashini24/NEWSPULSE.git


Install dependencies
pip install -r requirements.txt

Run dashboard
streamlit run app.py


## Results
The system identifies trending keywords and analyzes sentiment distribution from global news articles.

## Future Improvements
- Real-time news streaming
- Transformer-based sentiment analysis
- Topic visualization

The trained model file is not included in the repository due to GitHub size limits.
You can generate the model by running:

python train_model.py
167439b0e6538c3b4cd58d96972cd74299c124a1
