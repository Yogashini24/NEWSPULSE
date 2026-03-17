import streamlit as st
from news_scraper import NewsScraperDatabase
from sentiment_predictor import get_predictor
from utils import NewsArticleFormatter, DataProcessor
import pandas as pd


def render(render_header):
    """Render Recent and Trending News page"""
    render_header()
    
    st.divider()
    
    st.markdown("""
        <h2 style="color: #39FF14;">🔥 Recent & Trending News</h2>
        <p style="color: #A0AEC0; font-size: 1em;">
            Explore the latest news articles and trending stories from across the web.
        </p>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.markdown("<h3 style='color: #39FF14;'>🔍 Filters</h3>", unsafe_allow_html=True)
    
    try:
        db = NewsScraperDatabase()
        
        # Get categories
        all_news = db.get_all_news(limit=10000)
        categories = sorted(set([n.get('category', 'general') for n in all_news]))
        
        # Filter options
        selected_category = st.sidebar.selectbox(
            "Category",
            ["All"] + categories,
            key="news_category"
        )
        
        sort_by = st.sidebar.radio(
            "Sort By",
            ["Latest First", "Oldest First"],
            key="news_sort"
        )
        
        limit = st.sidebar.slider(
            "Number of Articles",
            5, 100, 20,
            key="news_limit"
        )
        
        # Filter news
        if selected_category == "All":
            news_items = all_news[:limit]
        else:
            news_items = [n for n in all_news if n.get('category') == selected_category][:limit]
        
        # Sort
        if sort_by == "Oldest First":
            news_items = list(reversed(news_items))
        
        # Get sentiment predictor
        predictor = get_predictor()
        
        # Display stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📰 Total Articles", len(news_items))
        
        with col2:
            st.metric("🏢 Sources", len(set([n.get('source', 'Unknown') for n in news_items])))
        
        with col3:
            st.metric("📂 Categories", len(set([n.get('category', 'general') for n in news_items])))
        
        st.divider()
        
        # Display articles
        if news_items:
            st.markdown("### 📰 Latest Articles")
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📋 List View", "📊 Table View"])
            
            with tab1:
                for idx, article in enumerate(news_items):
                    # Get sentiment
                    title = article.get('title', '')
                    description = article.get('description', '')
                    text_to_analyze = f"{title}. {description}"
                    
                    sentiment = predictor.predict(text_to_analyze)
                    
                    formatted_article = NewsArticleFormatter.format_article_for_display(
                        article,
                        sentiment=sentiment
                    )
                    
                    # Display article card
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # Title
                            st.markdown(f"""
                                <p style="
                                    color: #39FF14;
                                    font-size: 1.15em;
                                    font-weight: 600;
                                    font-family: Playfair Display, serif;
                                    margin: 0 0 10px 0;
                                ">
                                    {formatted_article['title']}
                                </p>
                            """, unsafe_allow_html=True)
                            
                            # Meta information
                            st.markdown(f"""
                                <p style="color: #A0AEC0; font-size: 0.85em; margin: 5px 0;">
                                    📰 <strong>{formatted_article['source']}</strong> | 
                                    ⏱️ {formatted_article['time_ago']} | 
                                    📂 {formatted_article['category'].upper()}
                                </p>
                            """, unsafe_allow_html=True)
                            
                            # Description
                            st.caption(DataProcessor.truncate_text(formatted_article['description'], 300))
                        
                        with col2:
                            # Sentiment badge
                            if sentiment:
                                emoji = DataProcessor.get_sentiment_emoji(sentiment.get('label', 'neutral'))
                                color = '#4ADE80' if sentiment.get('label') == 'positive' else '#F87171' if sentiment.get('label') == 'negative' else '#60A5FA'
                                
                                st.markdown(f"""
                                    <div style="
                                        background: linear-gradient(135deg, rgba(57, 255, 20, 0.1), rgba(0, 255, 255, 0.1));
                                        border: 2px solid {color};
                                        border-radius: 6px;
                                        padding: 10px;
                                        text-align: center;
                                    ">
                                        <p style="color: {color}; margin: 0; font-weight: 600; font-size: 1.5em;">
                                            {emoji}
                                        </p>
                                        <p style="color: {color}; margin: 5px 0 0 0; font-size: 0.85em; font-weight: 600;">
                                            {sentiment.get('label', 'NEUTRAL').upper()}
                                        </p>
                                        <p style="color: #A0AEC0; margin: 2px 0 0 0; font-size: 0.75em;">
                                            {sentiment.get('confidence', 0):.0%}
                                        </p>
                                    </div>
                                """, unsafe_allow_html=True)
                        
                        # Read more link
                        if formatted_article['url']:
                            st.markdown(
                                f"[🔗 Read Full Article →]({formatted_article['url']})",
                                unsafe_allow_html=True
                            )
                        
                        st.divider()
            
            with tab2:
                # Create table
                table_data = []
                for article in news_items:
                    title = article.get('title', '')
                    description = article.get('description', '')
                    text_to_analyze = f"{title}. {description}"
                    sentiment = predictor.predict(text_to_analyze)
                    
                    table_data.append({
                        'Title': DataProcessor.truncate_text(title, 50),
                        'Source': article.get('source', 'Unknown'),
                        'Category': article.get('category', 'general').upper(),
                        'Published': DataProcessor.format_timestamp(article.get('published_at', '')),
                        'Sentiment': sentiment.get('label', 'neutral').upper(),
                        'Confidence': f"{sentiment.get('confidence', 0):.0%}"
                    })
                
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        else:
            st.info("📭 No articles found for the selected filters.")
    
    except Exception as e:
        st.error(f"❌ Error loading news: {str(e)}")
        st.info("💡 Please run `python news_scraper.py` to fetch news data first.")
    
    # Back button
    st.divider()
    col1, col2 = st.columns([8, 2])
    
    with col2:
        if st.button("↩️ Back to Home", use_container_width=True, key="back_from_recent"):
            st.session_state.selected_page = None
            st.rerun()
