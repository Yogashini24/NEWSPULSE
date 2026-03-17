import streamlit as st
from news_scraper import NewsScraperDatabase
from sentiment_predictor import get_predictor
from utils import MetricsCalculator, DataProcessor
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt


def render(render_header):
    """Render Sentiment Analysis page"""
    render_header()
    
    st.divider()
    
    st.markdown("""
        <h2 style="color: #39FF14;">😊 Sentiment Analysis</h2>
        <p style="color: #A0AEC0; font-size: 1em;">
            Explore sentiment distribution across news articles and identify positive, negative, and neutral sentiments.
        </p>
    """, unsafe_allow_html=True)
    
    try:
        db = NewsScraperDatabase()
        all_news = db.get_all_news(limit=2000)
        
        if not all_news:
            st.info("📭 No news data available. Please run `python news_scraper.py` first.")
            return
        
        # Sidebar filters
        st.sidebar.markdown("<h3 style='color: #39FF14;'>🔍 Filters</h3>", unsafe_allow_html=True)
        
        categories = sorted(set([n.get('category', 'general') for n in all_news]))
        selected_category = st.sidebar.selectbox(
            "Category",
            ["All"] + categories,
            key="sentiment_category"
        )
        
        # Filter news
        if selected_category == "All":
            filtered_news = all_news
        else:
            filtered_news = [n for n in all_news if n.get('category') == selected_category]
        
        # Get sentiment predictor
        predictor = get_predictor()
        
        # Analyze sentiment
        st.markdown("### 📊 Analyzing Sentiments...")
        progress_bar = st.progress(0)
        
        sentiments = []
        for idx, article in enumerate(filtered_news):
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title}. {description}"
            
            sentiment = predictor.predict(text)
            sentiments.append(sentiment)
            
            progress_bar.progress((idx + 1) / len(filtered_news))
        
        progress_bar.empty()
        
        # Calculate metrics
        metrics = MetricsCalculator.calculate_sentiment_distribution(sentiments)
        
        # Display metrics
        st.divider()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "😊 Positive",
                f"{metrics['counts']['positive']}",
                f"{metrics['percentages']['positive']:.1f}%"
            )
        
        with col2:
            st.metric(
                "😞 Negative",
                f"{metrics['counts']['negative']}",
                f"{metrics['percentages']['negative']:.1f}%"
            )
        
        with col3:
            st.metric(
                "😐 Neutral",
                f"{metrics['counts']['neutral']}",
                f"{metrics['percentages']['neutral']:.1f}%"
            )
        
        with col4:
            st.metric(
                "📰 Total",
                f"{metrics['total']}",
                f"Analyzed"
            )
        
        st.divider()
        
        # Create tabs for visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Pie Chart", "📈 Bar Chart", "🎨 Distribution", "📋 Details"])
        
        with tab1:
            st.markdown("### Sentiment Distribution Pie Chart")
            
            labels = ['Positive', 'Negative', 'Neutral']
            values = [
                metrics['counts']['positive'],
                metrics['counts']['negative'],
                metrics['counts']['neutral']
            ]
            colors = ['#4ADE80', '#F87171', '#60A5FA']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors),
                textinfo='label+percent+value',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title="Sentiment Distribution",
                height=500,
                paper_bgcolor='#121212',
                font=dict(color='#E2E8F0', family='Lora, serif'),
                title_font=dict(color='#39FF14', size=20, family='Playfair Display, serif')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("### Sentiment Distribution Bar Chart")
            
            labels = ['Positive', 'Negative', 'Neutral']
            values = [
                metrics['percentages']['positive'],
                metrics['percentages']['negative'],
                metrics['percentages']['neutral']
            ]
            colors = ['#4ADE80', '#F87171', '#60A5FA']
            
            fig = go.Figure(data=[go.Bar(
                y=labels,
                x=values,
                orientation='h',
                marker=dict(color=colors),
                text=[f"{v:.1f}%" for v in values],
                textposition='auto',
            )])
            
            fig.update_layout(
                title="Sentiment Percentages",
                xaxis_title="Percentage (%)",
                yaxis_title="Sentiment",
                height=400,
                paper_bgcolor='#121212',
                plot_bgcolor='#1A202C',
                font=dict(color='#E2E8F0', family='Lora, serif'),
                title_font=dict(color='#39FF14', size=20, family='Playfair Display, serif')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("### Numerical Distribution")
            
            # Create gauge charts
            col1, col2, col3 = st.columns(3)
            
            sentiments_list = ['positive', 'negative', 'neutral']
            colors_dict = {'positive': '#4ADE80', 'negative': '#F87171', 'neutral': '#60A5FA'}
            cols = [col1, col2, col3]
            
            for sentiment, col, color_name in zip(sentiments_list, cols, ['😊 Positive', '😞 Negative', '😐 Neutral']):
                with col:
                    percentage = metrics['percentages'][sentiment]
                    
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=percentage,
                        title={'text': color_name},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': colors_dict[sentiment]},
                            'steps': [
                                {'range': [0, 100], 'color': 'rgba(200, 200, 200, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        },
                        number={'suffix': "%"}
                    ))
                    
                    fig.update_layout(
                        height=350,
                        paper_bgcolor='#121212',
                        font=dict(color='#E2E8F0', family='Lora, serif'),
                        title_font=dict(color=colors_dict[sentiment])
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.markdown("### Sentiment Breakdown")
            
            # Create detailed table
            detail_data = []
            
            for article, sentiment in zip(filtered_news, sentiments):
                detail_data.append({
                    'Title': DataProcessor.truncate_text(article.get('title', ''), 50),
                    'Category': article.get('category', 'general').upper(),
                    'Sentiment': sentiment.get('label', 'neutral').upper(),
                    'Confidence': f"{sentiment.get('confidence', 0):.0%}",
                    'Source': article.get('source', 'Unknown')[:30]
                })
            
            df = pd.DataFrame(detail_data)
            
            # Filter by sentiment
            sentiment_filter = st.selectbox(
                "Filter by Sentiment",
                ["All", "Positive", "Negative", "Neutral"],
                key="sentiment_filter"
            )
            
            if sentiment_filter != "All":
                df = df[df['Sentiment'] == sentiment_filter]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Sentiment Analysis CSV",
                data=csv,
                file_name="sentiment_analysis.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.divider()
        
        # Sentiment by category
        st.markdown("### 📊 Sentiment by Category")
        
        category_sentiments = {}
        for category in categories:
            cat_news = [n for n in filtered_news if n.get('category') == category]
            cat_sentiments = []
            for article in cat_news:
                title = article.get('title', '')
                description = article.get('description', '')
                text = f"{title}. {description}"
                cat_sentiments.append(predictor.predict(text))
            
            metrics_cat = MetricsCalculator.calculate_sentiment_distribution(cat_sentiments)
            category_sentiments[category] = metrics_cat['percentages']
        
        # Create stacked bar chart
        cat_data = []
        for category, percentages in category_sentiments.items():
            cat_data.append({
                'Category': category.upper(),
                'Positive': percentages['positive'],
                'Negative': percentages['negative'],
                'Neutral': percentages['neutral']
            })
        
        df_cat = pd.DataFrame(cat_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_cat['Category'],
            y=df_cat['Positive'],
            name='Positive',
            marker_color='#4ADE80'
        ))
        
        fig.add_trace(go.Bar(
            x=df_cat['Category'],
            y=df_cat['Negative'],
            name='Negative',
            marker_color='#F87171'
        ))
        
        fig.add_trace(go.Bar(
            x=df_cat['Category'],
            y=df_cat['Neutral'],
            name='Neutral',
            marker_color='#60A5FA'
        ))
        
        fig.update_layout(
            barmode='stack',
            title='Sentiment Distribution by Category',
            xaxis_title='Category',
            yaxis_title='Percentage (%)',
            height=400,
            paper_bgcolor='#121212',
            plot_bgcolor='#1A202C',
            font=dict(color='#E2E8F0', family='Lora, serif'),
            title_font=dict(color='#39FF14', size=20, family='Playfair Display, serif'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    
    # Back button
    st.divider()
    col1, col2 = st.columns([8, 2])
    
    with col2:
        if st.button("↩️ Back to Home", use_container_width=True, key="back_from_sentiment"):
            st.session_state.selected_page = None
            st.rerun()
