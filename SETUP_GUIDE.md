# NewsPulse Setup Guide

## ⚠️ Python 3.11+ REQUIRED

This project requires **Python 3.11 or higher**.

### Check Your Python Version

Open PowerShell and run:
```powershell
python --version
```

Expected: `Python 3.11.x` or higher

### Install Python 3.11 (if needed)

1. Visit https://www.python.org/downloads/
2. Download **Python 3.11** or latest version
3. Run the installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
5. Restart your terminal
6. Verify: `python --version`

---

## Complete Step-by-Step Setup Instructions

### Step 1: Get News API Key

1. Visit https://newsapi.org/
2. Click "Register" and create an account
3. Verify your email
4. Go to "API Keys" section
5. Copy your API key (looks like: `abc123def456ghi789`)

### Step 2: Configure Environment

1. Open `.env` file in the project root
2. Replace placeholder with your actual API key:
   ```
   NEWS_API_KEY=YOUR_ACTUAL_API_KEY_HERE
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=NewsPulse@2024
   ```
3. Save the file

### Step 3: Install Dependencies

Open PowerShell/Terminal in the project directory and run:

```powershell
pip install -r requirements.txt
```

Wait for all packages to install (this may take 2-3 minutes).

### Step 4: Download Required Data

Run the following command to download NLTK data:

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 5: Fetch News Data

Run the news scraper to fetch data from News API:

```powershell
python news_scraper.py
```

**Expected Output:**
```
Starting news scraping...
Fetched 50 articles from category: business
Fetched 50 articles from category: technology
...
News scraping completed successfully
```

This creates a SQLite database at `data/newspulse.db`

### Step 6: Train Sentiment Model

Train the sentiment analysis model:

```powershell
python train_model.py
```

**Expected Output:**
```
Starting sentiment model training...
Generating training data...
Training data shape: (1500, 2)
...
==================================================
TRAINING RESULTS
==================================================
TRAIN RESULTS:
  accuracy: 0.9234
  precision: 0.9187
  recall: 0.9234
  f1_score: 0.9205
```

This saves the model to `models/sentiment_model.pkl` and metrics to `models/model_metrics.json`

### Step 7: Run the Dashboard

Start the Streamlit application:

```powershell
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://YOUR_IP:8501
```

### Step 8: Login to Dashboard

1. Open your browser to http://localhost:8501
2. Use default credentials:
   - **Username**: `admin`
   - **Password**: `NewsPulse@2024`
3. Click "🔓 Login"

## Verification Checklist

- [ ] News API key obtained and added to `.env`
- [ ] Dependencies installed successfully
- [ ] NLTK data downloaded
- [ ] News data scraped (database created)
- [ ] Sentiment model trained (model saved)
- [ ] Dashboard running in browser
- [ ] Login successful
- [ ] All 5 dashboard sections accessible

## Dashboard Features After Login

### ✅ Section 1: Recent & Trending News
- Lists latest news articles
- Shows sentiment for each article
- Filter by category
- Sort by latest/oldest
- Direct links to articles

### ✅ Section 2: Trending Keywords & Topics
- Bar chart of top keywords
- Word cloud visualization
- Keywords table
- Category breakdown
- Download CSV option

### ✅ Section 3: Sentiment Analysis
- Pie chart distribution
- Bar charts with percentages
- Gauge visualizations
- Category breakdown
- Detailed sentiment table

### ✅ Section 4: Model Performance Metrics
- Accuracy, Precision, Recall, F1-Score
- Gauge charts for each metric
- Performance report
- Model information

### ✅ Section 5: Overall Summary
- Dashboard overview statistics
- Sentiment analysis summary
- Top keywords and trends
- Latest news with sentiments
- Advanced analytics

## Python Version Check

Before installing dependencies, verify you have Python 3.11+:

```powershell
python --version
```

Expected output: `Python 3.11.x` or higher

### Installing Python 3.11

If you need to install Python 3.11:

1. Visit https://www.python.org/downloads/
2. Download "Python 3.11" or latest
3. Run installer
4. **IMPORTANT**: Check "Add Python to PATH"
5. Restart terminal after installation

## Common Issues & Solutions

### Issue 1: "API Key Invalid"
**Error**: `API Error: Invalid API key`

**Solution**:
1. Check API key in `.env` file
2. Visit https://newsapi.org/ and verify key
3. Make sure to use quotes if key contains special characters
4. Restart the application

### Issue 2: "Module not found"
**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```powershell
pip install streamlit
# Or reinstall all
pip install -r requirements.txt
```

### Issue 3: "Database error"
**Error**: `Database initialization failed`

**Solution**:
1. Delete `data/newspulse.db` if it exists
2. Run `python news_scraper.py` again
3. The database will be recreated

### Issue 4: "Model not found"
**Error**: `Model not found` in Model Performance page

**Solution**:
1. Run `python train_model.py`
2. Wait for training to complete
3. Restart Streamlit app

### Issue 5: "Port already in use"
**Error**: `Port 8501 is already in use`

**Solution**:
```powershell
streamlit run app.py --server.port=8502
```

## Performance Optimization

### To process more articles:
Edit `news_scraper.py` line:
```python
scraper.fetch_all_categories(page_size=100)  # Increase from 50
```

### To improve sentiment analysis speed:
Edit `sentiment_predictor.py` to use GPU:
```python
device = 0  # Use GPU device 0
```

## Regular Maintenance

### Weekly Tasks
```powershell
python news_scraper.py  # Update news data
```

### Monthly Tasks
```powershell
python train_model.py   # Retrain model with new data
```

## Accessing Dashboard Remotely

If running on a remote machine, use:
```powershell
streamlit run app.py --server.address=0.0.0.0
```

Then access from another computer using the network URL shown.

## Troubleshooting Commands

### Check Python installation
```powershell
python --version
```

### Check installed packages
```powershell
pip list | findstr streamlit
```

### Check if port is open
```powershell
netstat -ano | findstr 8501
```

### Kill process on port 8501
```powershell
taskkill /PID <PID> /F
```

## Data Storage Locations

- **News Database**: `data/newspulse.db`
- **Trained Model**: `models/sentiment_model.pkl`
- **Model Metrics**: `models/model_metrics.json`
- **Configuration**: `.env`

## Customization

### Change Admin Password
Edit `.env`:
```
ADMIN_PASSWORD=YOUR_NEW_PASSWORD
```

### Change Theme Colors
Edit `theme_config.py`:
```python
BACKGROUND_PRIMARY = "#121212"  # Change this
ACCENT_PRIMARY = "#39FF14"      # Or this
```

### Add More News Categories
Edit `news_scraper.py`:
```python
CATEGORIES = {
    'business': 'business',
    'your_category': 'your_category',
    # Add more...
}
```

## Next Steps

1. ✅ Complete setup following this guide
2. ✅ Verify all 5 dashboard sections work
3. ✅ Explore different filters and views
4. ✅ Review sentiment analysis results
5. ✅ Check model performance metrics
6. ✅ Export data as needed

## Need Help?

1. Check the `README.md` file for detailed documentation
2. Review error messages in the terminal
3. Verify `.env` configuration
4. Ensure all dependencies are installed

---

**Happy exploring with NewsPulse!** 🎉
