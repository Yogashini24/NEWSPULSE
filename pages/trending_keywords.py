import streamlit as st
from news_scraper import NewsScraperDatabase
from utils import MetricsCalculator
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd


def render(render_header):
    """Render Trending Keywords and Topics page"""
    render_header()
    
    st.divider()
    
    st.markdown("""
        <h2 style="color: #39FF14;">🔤 Trending Keywords & Topics</h2>
        <p style="color: #A0AEC0; font-size: 1em;">
            Discover the most discussed topics and keywords in the news.
        </p>
    """, unsafe_allow_html=True)
    
    try:
        db = NewsScraperDatabase()
        all_news = db.get_all_news(limit=5000)
        
        if not all_news:
            st.info("📭 No news data available. Please run `python news_scraper.py` first.")
            return
        
        # Get trending topics
        trending_topics = MetricsCalculator.get_trending_topics(all_news, top_n=20)
        
        # Display top stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total Keywords", len(trending_topics))
        
        with col2:
            if trending_topics:
                top_keyword = max(trending_topics.items(), key=lambda x: x[1])
                st.metric("🔥 Top Keyword", top_keyword[0].upper(), f"{top_keyword[1]} mentions")
        
        with col3:
            total_mentions = sum(trending_topics.values())
            st.metric("💬 Total Mentions", total_mentions)
        
        st.divider()
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Bar Chart", "☁️ Word Cloud", "📋 Table", "🎯 Topic Distribution"])
        
        with tab1:
            st.markdown("### Bar Chart - Top Keywords")
            
            if trending_topics:
                # Prepare data for bar chart
                sorted_topics = sorted(trending_topics.items(), key=lambda x: x[1], reverse=True)[:15]
                keywords = [item[0].upper() for item in sorted_topics]
                frequencies = [item[1] for item in sorted_topics]
                
                fig = go.Figure(data=[
                    go.Bar(
                        y=keywords,
                        x=frequencies,
                        orientation='h',
                        marker=dict(
                            color=frequencies,
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Frequency")
                        ),
                        text=frequencies,
                        textposition='auto',
                    )
                ])
                
                fig.update_layout(
                    title="Top 15 Trending Keywords",
                    xaxis_title="Frequency",
                    yaxis_title="Keyword",
                    height=500,
                    hovermode='closest',
                    paper_bgcolor='#121212',
                    plot_bgcolor='#1A202C',
                    font=dict(color='#E2E8F0', family='Lora, serif'),
                    title_font=dict(color='#39FF14', size=20, family='Playfair Display, serif')
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("### Word Cloud - Keywords Visualization")
            
            if trending_topics:
                # Create word cloud
                fig, ax = plt.subplots(figsize=(12, 6), facecolor='#121212')
                
                try:
                    wordcloud = WordCloud(
                        width=1200,
                        height=600,
                        background_color='#121212',
                        colormap='twilight',
                        relative_scaling=0.5,
                        min_font_size=10
                    ).generate_from_frequencies(trending_topics)
                    
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    
                    st.pyplot(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error generating word cloud: {str(e)}")
        
        with tab3:
            st.markdown("### Top Keywords Table")
            
            if trending_topics:
                # Create dataframe
                sorted_topics = sorted(trending_topics.items(), key=lambda x: x[1], reverse=True)
                df = pd.DataFrame(sorted_topics, columns=['Keyword', 'Frequency'])
                df['Percentage'] = (df['Frequency'] / df['Frequency'].sum() * 100).round(2)
                df['Rank'] = range(1, len(df) + 1)
                df = df[['Rank', 'Keyword', 'Frequency', 'Percentage']]
                
                st.dataframe(
                    df.head(30),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Keywords CSV",
                    data=csv,
                    file_name="trending_keywords.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with tab4:
            st.markdown("### Keywords by Category")
            
            # Get categories
            categories = sorted(set([n.get('category', 'general') for n in all_news]))
            
            # Calculate keywords by category
            category_keywords = {}
            for category in categories:
                category_news = [n for n in all_news if n.get('category') == category]
                keywords = MetricsCalculator.get_trending_topics(category_news, top_n=5)
                category_keywords[category] = keywords
            
            # Create visualization
            category_data = []
            for category, keywords in category_keywords.items():
                for keyword, frequency in keywords.items():
                    category_data.append({
                        'Category': category.upper(),
                        'Keyword': keyword.upper(),
                        'Frequency': frequency
                    })
            
            if category_data:
                df_category = pd.DataFrame(category_data)
                
                fig = px.bar(
                    df_category,
                    x='Keyword',
                    y='Frequency',
                    color='Category',
                    barmode='group',
                    title='Top Keywords by Category',
                    labels={'Frequency': 'Mentions', 'Keyword': 'Keyword'}
                )
                
                fig.update_layout(
                    height=500,
                    paper_bgcolor='#121212',
                    plot_bgcolor='#1A202C',
                    font=dict(color='#E2E8F0', family='Lora, serif'),
                    title_font=dict(color='#39FF14', size=20, family='Playfair Display, serif'),
                    hovermode='closest'
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Insights
        st.markdown("### 💡 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if trending_topics:
                top_5 = sorted(trending_topics.items(), key=lambda x: x[1], reverse=True)[:5]
                st.markdown(f"""
                    **Top 5 Keywords:**
                    1. {top_5[0][0].upper()} ({top_5[0][1]} mentions)
                    2. {top_5[1][0].upper()} ({top_5[1][1]} mentions)
                    3. {top_5[2][0].upper()} ({top_5[2][1]} mentions)
                    4. {top_5[3][0].upper()} ({top_5[3][1]} mentions)
                    5. {top_5[4][0].upper()} ({top_5[4][1]} mentions)
                """)
        
        with col2:
            # Category distribution
            st.markdown("**News by Category:**")
            category_dist = MetricsCalculator.get_category_distribution(all_news)
            for cat, count in sorted(category_dist.items(), key=lambda x: x[1], reverse=True)[:5]:
                st.markdown(f"- {cat.upper()}: {count} articles")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    
    # Back button
    st.divider()
    col1, col2 = st.columns([8, 2])
    
    with col2:
        if st.button("↩️ Back to Home", use_container_width=True, key="back_from_keywords"):
            st.session_state.selected_page = None
            st.rerun()
