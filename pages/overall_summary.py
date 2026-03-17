import streamlit as st
from news_scraper import NewsScraperDatabase
from sentiment_predictor import get_predictor
from utils import MetricsCalculator, DataProcessor, NewsArticleFormatter
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def render(render_header):
    """Render Overall Summary page"""
    render_header()
    
    st.divider()
    
    st.markdown("""
        <h2 style="color: #39FF14;">📋 Overall Summary</h2>
        <p style="color: #A0AEC0; font-size: 1em;">
            Comprehensive overview of all insights and analytics from NewsPulse.
        </p>
    """, unsafe_allow_html=True)
    
    try:
        db = NewsScraperDatabase()
        all_news = db.get_all_news(limit=3000)
        
        if not all_news:
            st.info("📭 No news data available. Please run `python news_scraper.py` first.")
            return
        
        predictor = get_predictor()
        
        # Analyze all sentiments
        st.markdown("### 🔄 Analyzing all news...")
        progress_bar = st.progress(0)
        
        sentiments = []
        for idx, article in enumerate(all_news):
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title}. {description}"
            sentiment = predictor.predict(text)
            sentiments.append(sentiment)
            progress_bar.progress((idx + 1) / len(all_news))
        
        progress_bar.empty()
        
        # Calculate metrics
        sentiment_metrics = MetricsCalculator.calculate_sentiment_distribution(sentiments)
        trending_topics = MetricsCalculator.get_trending_topics(all_news, top_n=15)
        category_dist = MetricsCalculator.get_category_distribution(all_news)
        source_dist = MetricsCalculator.get_source_distribution(all_news)
        
        # SECTION 1: Key Statistics
        st.markdown("### 📊 Key Statistics")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📰 Total Articles", len(all_news))
        
        with col2:
            st.metric("🏢 Sources", len(source_dist))
        
        with col3:
            st.metric("📂 Categories", len(category_dist))
        
        with col4:
            st.metric("🔤 Keywords", len(trending_topics))
        
        with col5:
            st.metric("😊 Analyzed", f"{len(sentiments)}")
        
        st.divider()
        
        # Create main dashboard
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview",
            "😊 Sentiment",
            "🔤 Keywords",
            "📰 Latest News",
            "📈 Analytics"
        ])
        
        # TAB 1: Overview
        with tab1:
            st.markdown("### Dashboard Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📂 News by Category")
                
                if category_dist:
                    sorted_cats = sorted(category_dist.items(), key=lambda x: x[1], reverse=True)
                    cat_labels = [cat[0].upper() for cat in sorted_cats]
                    cat_values = [cat[1] for cat in sorted_cats]
                    
                    fig = go.Figure(data=[go.Bar(
                        x=cat_labels,
                        y=cat_values,
                        marker_color='#39FF14'
                    )])
                    
                    fig.update_layout(
                        title="Articles by Category",
                        xaxis_title="Category",
                        yaxis_title="Count",
                        height=400,
                        paper_bgcolor='#121212',
                        plot_bgcolor='#1A202C',
                        font=dict(color='#E2E8F0', family='Lora, serif'),
                        title_font=dict(color='#39FF14', size=16, family='Playfair Display, serif'),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 🏢 Top News Sources")
                
                if source_dist:
                    sorted_sources = sorted(source_dist.items(), key=lambda x: x[1], reverse=True)[:10]
                    source_names = [src[0] for src in sorted_sources]
                    source_counts = [src[1] for src in sorted_sources]
                    
                    fig = go.Figure(data=[go.Bar(
                        y=source_names,
                        x=source_counts,
                        orientation='h',
                        marker_color='#00FFFF'
                    )])
                    
                    fig.update_layout(
                        title="Top 10 News Sources",
                        xaxis_title="Article Count",
                        yaxis_title="Source",
                        height=400,
                        paper_bgcolor='#121212',
                        plot_bgcolor='#1A202C',
                        font=dict(color='#E2E8F0', family='Lora, serif'),
                        title_font=dict(color='#39FF14', size=16, family='Playfair Display, serif'),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        # TAB 2: Sentiment Analysis
        with tab2:
            st.markdown("### Sentiment Analysis Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Sentiment Distribution")
                
                labels = ['Positive', 'Negative', 'Neutral']
                values = [
                    sentiment_metrics['counts']['positive'],
                    sentiment_metrics['counts']['negative'],
                    sentiment_metrics['counts']['neutral']
                ]
                colors = ['#4ADE80', '#F87171', '#60A5FA']
                
                fig = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    marker=dict(colors=colors),
                    textinfo='label+percent+value'
                )])
                
                fig.update_layout(
                    title="Sentiment Distribution",
                    height=400,
                    paper_bgcolor='#121212',
                    font=dict(color='#E2E8F0', family='Lora, serif'),
                    title_font=dict(color='#39FF14', size=16, family='Playfair Display, serif')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Sentiment Percentages")
                
                st.markdown(f"""
                    **😊 Positive Sentiment**
                    - Count: {sentiment_metrics['counts']['positive']}
                    - Percentage: {sentiment_metrics['percentages']['positive']:.2f}%
                    
                    **😞 Negative Sentiment**
                    - Count: {sentiment_metrics['counts']['negative']}
                    - Percentage: {sentiment_metrics['percentages']['negative']:.2f}%
                    
                    **😐 Neutral Sentiment**
                    - Count: {sentiment_metrics['counts']['neutral']}
                    - Percentage: {sentiment_metrics['percentages']['neutral']:.2f}%
                """)
                
                # Overall sentiment
                dominant_sentiment = max(
                    ('positive', sentiment_metrics['percentages']['positive']),
                    ('negative', sentiment_metrics['percentages']['negative']),
                    ('neutral', sentiment_metrics['percentages']['neutral']),
                    key=lambda x: x[1]
                )
                
                st.markdown(f"""
                    **🎯 Overall Sentiment**: {dominant_sentiment[0].upper()}
                    ({dominant_sentiment[1]:.2f}%)
                """)
            
            # Sentiment by category
            st.markdown("#### Sentiment Trends by Category")
            
            category_sentiment_data = []
            for category in sorted(category_dist.keys()):
                cat_news = [n for n in all_news if n.get('category') == category]
                cat_sentiments = []
                for article in cat_news:
                    title = article.get('title', '')
                    desc = article.get('description', '')
                    text = f"{title}. {desc}"
                    cat_sentiments.append(predictor.predict(text))
                
                cat_metrics = MetricsCalculator.calculate_sentiment_distribution(cat_sentiments)
                category_sentiment_data.append({
                    'Category': category.upper(),
                    'Positive': cat_metrics['percentages']['positive'],
                    'Negative': cat_metrics['percentages']['negative'],
                    'Neutral': cat_metrics['percentages']['neutral']
                })
            
            df_cat_sent = pd.DataFrame(category_sentiment_data)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(x=df_cat_sent['Category'], y=df_cat_sent['Positive'], name='Positive', marker_color='#4ADE80'))
            fig.add_trace(go.Bar(x=df_cat_sent['Category'], y=df_cat_sent['Negative'], name='Negative', marker_color='#F87171'))
            fig.add_trace(go.Bar(x=df_cat_sent['Category'], y=df_cat_sent['Neutral'], name='Neutral', marker_color='#60A5FA'))
            
            fig.update_layout(
                barmode='stack',
                title='Sentiment Distribution by Category (%)',
                xaxis_title='Category',
                yaxis_title='Percentage (%)',
                height=400,
                paper_bgcolor='#121212',
                plot_bgcolor='#1A202C',
                font=dict(color='#E2E8F0', family='Lora, serif'),
                title_font=dict(color='#39FF14', size=16, family='Playfair Display, serif'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # TAB 3: Keywords & Topics
        with tab3:
            st.markdown("### Trending Keywords & Topics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Top Keywords")
                
                if trending_topics:
                    sorted_keywords = sorted(trending_topics.items(), key=lambda x: x[1], reverse=True)[:10]
                    keywords = [kw[0].upper() for kw in sorted_keywords]
                    frequencies = [kw[1] for kw in sorted_keywords]
                    
                    fig = go.Figure(data=[go.Bar(
                        y=keywords,
                        x=frequencies,
                        orientation='h',
                        marker_color='#39FF14'
                    )])
                    
                    fig.update_layout(
                        title="Top 10 Keywords",
                        xaxis_title="Frequency",
                        yaxis_title="Keyword",
                        height=400,
                        paper_bgcolor='#121212',
                        plot_bgcolor='#1A202C',
                        font=dict(color='#E2E8F0', family='Lora, serif'),
                        title_font=dict(color='#39FF14', size=16, family='Playfair Display, serif'),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Word Cloud")
                
                if trending_topics:
                    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#121212')
                    
                    wordcloud = WordCloud(
                        width=1000,
                        height=500,
                        background_color='#121212',
                        colormap='twilight',
                        relative_scaling=0.5
                    ).generate_from_frequencies(trending_topics)
                    
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    
                    st.pyplot(fig, use_container_width=True)
            
            st.markdown("#### Keywords List")
            if trending_topics:
                sorted_kw = sorted(trending_topics.items(), key=lambda x: x[1], reverse=True)
                kw_data = []
                for rank, (keyword, frequency) in enumerate(sorted_kw, 1):
                    kw_data.append({
                        'Rank': rank,
                        'Keyword': keyword.upper(),
                        'Frequency': frequency,
                        'Percentage': f"{frequency / sum(trending_topics.values()) * 100:.2f}%"
                    })
                
                df_kw = pd.DataFrame(kw_data[:20])
                st.dataframe(df_kw, use_container_width=True, hide_index=True)
        
        # TAB 4: Latest News
        with tab4:
            st.markdown("### Latest News with Sentiments")
            
            latest_news = all_news[:20]
            
            for idx, article in enumerate(latest_news):
                title = article.get('title', '')
                desc = article.get('description', '')
                text = f"{title}. {desc}"
                sentiment = predictor.predict(text)
                
                formatted = NewsArticleFormatter.format_article_for_display(article, sentiment=sentiment)
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                        <p style="
                            color: #39FF14;
                            font-size: 1.1em;
                            font-weight: 600;
                            font-family: Playfair Display, serif;
                            margin: 0 0 5px 0;
                        ">
                            {DataProcessor.truncate_text(formatted['title'], 80)}
                        </p>
                    """, unsafe_allow_html=True)
                    
                    st.caption(f"{formatted['source']} • {formatted['time_ago']}")
                
                with col2:
                    sentiment_color = '#4ADE80' if sentiment.get('label') == 'positive' else '#F87171' if sentiment.get('label') == 'negative' else '#60A5FA'
                    st.markdown(f"""
                        <div style="text-align: center; padding: 5px;">
                            <p style="color: {sentiment_color}; margin: 0; font-weight: 600;">
                                {sentiment.get('label', 'neutral').upper()}
                            </p>
                            <p style="color: #A0AEC0; margin: 0; font-size: 0.85em;">
                                {sentiment.get('confidence', 0):.0%}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
        
        # TAB 5: Advanced Analytics
        with tab5:
            st.markdown("### Advanced Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Sentiment Score Distribution")
                
                sentiment_scores = [s.get('confidence', 0) for s in sentiments]
                
                fig = go.Figure(data=[go.Histogram(
                    x=sentiment_scores,
                    nbinsx=30,
                    marker_color='#39FF14'
                )])
                
                fig.update_layout(
                    title="Confidence Score Distribution",
                    xaxis_title="Confidence Score",
                    yaxis_title="Frequency",
                    height=400,
                    paper_bgcolor='#121212',
                    plot_bgcolor='#1A202C',
                    font=dict(color='#E2E8F0', family='Lora, serif'),
                    title_font=dict(color='#39FF14', size=16, family='Playfair Display, serif'),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Summary Statistics")
                
                import numpy as np
                
                stats_data = {
                    'Mean Confidence': f"{np.mean(sentiment_scores):.4f}",
                    'Median Confidence': f"{np.median(sentiment_scores):.4f}",
                    'Std Deviation': f"{np.std(sentiment_scores):.4f}",
                    'Min Score': f"{np.min(sentiment_scores):.4f}",
                    'Max Score': f"{np.max(sentiment_scores):.4f}",
                    'Q1 (25%)': f"{np.percentile(sentiment_scores, 25):.4f}",
                    'Q3 (75%)': f"{np.percentile(sentiment_scores, 75):.4f}"
                }
                
                st.markdown("---")
                for stat_name, stat_value in stats_data.items():
                    st.markdown(f"**{stat_name}**: `{stat_value}`")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Export section
    st.markdown("### 📥 Export Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Summary as CSV", use_container_width=True, key="export_csv"):
            st.info("Export functionality will be added in the next update.")
    
    with col2:
        if st.button("📄 Generate PDF Report", use_container_width=True, key="export_pdf"):
            st.info("PDF export functionality will be added in the next update.")
    
    with col3:
        if st.button("📧 Send Email Report", use_container_width=True, key="export_email"):
            st.info("Email functionality will be added in the next update.")
    
    # Back button
    st.divider()
    col1, col2 = st.columns([8, 2])
    
    with col2:
        if st.button("↩️ Back to Home", use_container_width=True, key="back_from_summary"):
            st.session_state.selected_page = None
            st.rerun()
