import streamlit as st


class ThemeConfig:
    """Professional theme configuration for NewsPulse Dashboard"""
    
    # Colors
    BACKGROUND_PRIMARY = "#121212"
    BACKGROUND_SECONDARY = "#1A202C"
    TEXT_PRIMARY = "#E2E8F0"
    TEXT_SECONDARY = "#A0AEC0"
    ACCENT_PRIMARY = "#39FF14"  # Neon Green
    ACCENT_SECONDARY = "#00FFFF"  # Electric Cyan
    
    # Sentiment colors
    SENTIMENT_POSITIVE = "#4ADE80"  # Green
    SENTIMENT_NEGATIVE = "#F87171"  # Red
    SENTIMENT_NEUTRAL = "#60A5FA"  # Blue
    
    # Fonts (via CSS)
    FONT_HEADLINE = "Playfair Display, serif"
    FONT_BODY = "Lora, serif"
    
    @staticmethod
    def apply_custom_styling():
        """Apply custom CSS styling to Streamlit app"""
        st.markdown(f"""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lora:wght@400;500;600;700&display=swap');
                
                * {{
                    font-family: '{ThemeConfig.FONT_BODY}', serif;
                }}
                
                /* Main background */
                .stApp {{
                    background: linear-gradient(135deg, {ThemeConfig.BACKGROUND_PRIMARY} 0%, {ThemeConfig.BACKGROUND_SECONDARY} 100%);
                }}
                
                /* Sidebar */
                .sidebar .sidebar-content {{
                    background: {ThemeConfig.BACKGROUND_SECONDARY};
                }}
                
                /* Headers and titles */
                h1, h2, h3, h4, h5, h6 {{
                    font-family: '{ThemeConfig.FONT_HEADLINE}' !important;
                    color: {ThemeConfig.ACCENT_PRIMARY} !important;
                    text-shadow: 0 0 10px rgba(57, 255, 20, 0.3);
                    letter-spacing: 1px;
                }}
                
                h1 {{
                    font-size: 3em !important;
                    margin-bottom: 0.5em !important;
                }}
                
                h2 {{
                    font-size: 2em !important;
                    border-bottom: 2px solid {ThemeConfig.ACCENT_SECONDARY};
                    padding-bottom: 0.5em !important;
                    margin-top: 1.5em !important;
                }}
                
                h3 {{
                    font-size: 1.5em !important;
                }}
                
                /* Text color */
                body, .stMarkdown, .stText {{
                    color: {ThemeConfig.TEXT_PRIMARY} !important;
                }}
                
                .stMarkdown {{
                    line-height: 1.6;
                }}
                
                /* Primary text elements */
                p {{
                    color: {ThemeConfig.TEXT_PRIMARY} !important;
                    font-size: 1.1em;
                }}
                
                /* Button styling */
                .stButton > button {{
                    background: linear-gradient(135deg, {ThemeConfig.ACCENT_PRIMARY}, {ThemeConfig.ACCENT_SECONDARY});
                    color: {ThemeConfig.BACKGROUND_PRIMARY} !important;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px !important;
                    font-weight: 600 !important;
                    font-family: '{ThemeConfig.FONT_HEADLINE}', serif !important;
                    width: 100%;
                    font-size: 1.1em;
                    transition: all 0.3s ease;
                    box-shadow: 0 0 15px rgba(57, 255, 20, 0.4);
                }}
                
                .stButton > button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 0 25px rgba(0, 255, 255, 0.6);
                }}
                
                /* Input fields */
                .stTextInput > div > div > input,
                .stPasswordInput > div > div > input,
                .stSelectbox > div > div > select {{
                    background-color: {ThemeConfig.BACKGROUND_SECONDARY} !important;
                    color: {ThemeConfig.TEXT_PRIMARY} !important;
                    border: 2px solid {ThemeConfig.ACCENT_PRIMARY} !important;
                    border-radius: 6px;
                    padding: 10px !important;
                    font-family: '{ThemeConfig.FONT_BODY}', serif !important;
                }}
                
                .stTextInput > div > div > input::placeholder {{
                    color: {ThemeConfig.TEXT_SECONDARY} !important;
                }}
                
                /* Cards and containers */
                .stMetric {{
                    background: linear-gradient(135deg, rgba(57, 255, 20, 0.1), rgba(0, 255, 255, 0.1));
                    border-left: 4px solid {ThemeConfig.ACCENT_PRIMARY};
                    padding: 15px !important;
                    border-radius: 8px;
                }}
                
                .stMetricLabel {{
                    color: {ThemeConfig.TEXT_SECONDARY} !important;
                    font-size: 0.9em !important;
                }}
                
                .stMetricValue {{
                    color: {ThemeConfig.ACCENT_PRIMARY} !important;
                    font-size: 2em !important;
                    font-family: '{ThemeConfig.FONT_HEADLINE}', serif !important;
                }}
                
                /* Expander */
                .streamlit-expanderHeader {{
                    background: {ThemeConfig.BACKGROUND_SECONDARY} !important;
                    color: {ThemeConfig.ACCENT_PRIMARY} !important;
                    border: 1px solid {ThemeConfig.ACCENT_SECONDARY} !important;
                }}
                
                .streamlit-expanderHeader:hover {{
                    background: linear-gradient(135deg, rgba(57, 255, 20, 0.2), rgba(0, 255, 255, 0.2)) !important;
                }}
                
                /* Tabs */
                .stTabs [data-baseweb="tab-list"] {{
                    gap: 8px;
                }}
                
                .stTabs [data-baseweb="tab"] {{
                    background: {ThemeConfig.BACKGROUND_SECONDARY};
                    border: 1px solid {ThemeConfig.ACCENT_PRIMARY};
                    color: {ThemeConfig.TEXT_PRIMARY};
                }}
                
                .stTabs [aria-selected="true"] {{
                    background: linear-gradient(135deg, {ThemeConfig.ACCENT_PRIMARY}, {ThemeConfig.ACCENT_SECONDARY}) !important;
                    color: {ThemeConfig.BACKGROUND_PRIMARY} !important;
                }}
                
                /* Table styling */
                table {{
                    color: {ThemeConfig.TEXT_PRIMARY} !important;
                }}
                
                th {{
                    background: linear-gradient(135deg, {ThemeConfig.ACCENT_PRIMARY}, {ThemeConfig.ACCENT_SECONDARY}) !important;
                    color: {ThemeConfig.BACKGROUND_PRIMARY} !important;
                    font-family: '{ThemeConfig.FONT_HEADLINE}', serif !important;
                }}
                
                td {{
                    border-color: {ThemeConfig.ACCENT_SECONDARY} !important;
                    color: {ThemeConfig.TEXT_PRIMARY} !important;
                }}
                
                tr:hover {{
                    background: rgba(57, 255, 20, 0.1) !important;
                }}
                
                /* Sidebar styling */
                .sidebar .sidebar-content {{
                    background: linear-gradient(180deg, {ThemeConfig.BACKGROUND_SECONDARY} 0%, {ThemeConfig.BACKGROUND_PRIMARY} 100%);
                }}
                
                .sidebar .stRadio > label {{
                    color: {ThemeConfig.TEXT_PRIMARY} !important;
                }}
                
                .stRadio > label > div:first-child {{
                    accent-color: {ThemeConfig.ACCENT_PRIMARY} !important;
                }}
                
                /* Success/Error/Info messages */
                .stSuccess {{
                    background: rgba(74, 222, 128, 0.2) !important;
                    border-left: 4px solid {ThemeConfig.SENTIMENT_POSITIVE} !important;
                    color: {ThemeConfig.SENTIMENT_POSITIVE} !important;
                }}
                
                .stError {{
                    background: rgba(248, 113, 113, 0.2) !important;
                    border-left: 4px solid {ThemeConfig.SENTIMENT_NEGATIVE} !important;
                    color: {ThemeConfig.SENTIMENT_NEGATIVE} !important;
                }}
                
                .stInfo {{
                    background: rgba(96, 165, 250, 0.2) !important;
                    border-left: 4px solid {ThemeConfig.ACCENT_SECONDARY} !important;
                    color: {ThemeConfig.ACCENT_SECONDARY} !important;
                }}
                
                /* Scrollbar styling */
                ::-webkit-scrollbar {{
                    width: 10px;
                    height: 10px;
                }}
                
                ::-webkit-scrollbar-track {{
                    background: {ThemeConfig.BACKGROUND_SECONDARY};
                }}
                
                ::-webkit-scrollbar-thumb {{
                    background: {ThemeConfig.ACCENT_PRIMARY};
                    border-radius: 5px;
                }}
                
                ::-webkit-scrollbar-thumb:hover {{
                    background: {ThemeConfig.ACCENT_SECONDARY};
                }}
                
                /* Custom classes for sentiment colors */
                .sentiment-positive {{
                    color: {ThemeConfig.SENTIMENT_POSITIVE} !important;
                    font-weight: 600;
                }}
                
                .sentiment-negative {{
                    color: {ThemeConfig.SENTIMENT_NEGATIVE} !important;
                    font-weight: 600;
                }}
                
                .sentiment-neutral {{
                    color: {ThemeConfig.SENTIMENT_NEUTRAL} !important;
                    font-weight: 600;
                }}
                
                /* Card styling */
                .news-card {{
                    background: linear-gradient(135deg, rgba(57, 255, 20, 0.05), rgba(0, 255, 255, 0.05));
                    border: 1px solid {ThemeConfig.ACCENT_SECONDARY};
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    transition: all 0.3s ease;
                }}
                
                .news-card:hover {{
                    border-color: {ThemeConfig.ACCENT_PRIMARY};
                    box-shadow: 0 0 15px rgba(57, 255, 20, 0.3);
                    transform: translateY(-2px);
                }}
                
                /* Animation */
                @keyframes glow {{
                    0%, 100% {{ text-shadow: 0 0 10px rgba(57, 255, 20, 0.3); }}
                    50% {{ text-shadow: 0 0 20px rgba(0, 255, 255, 0.6); }}
                }}
                
                .glow {{
                    animation: glow 2s ease-in-out infinite;
                }}
            </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def get_color_for_sentiment(sentiment):
        """Get color for sentiment label"""
        sentiment = sentiment.lower()
        if sentiment == 'positive':
            return ThemeConfig.SENTIMENT_POSITIVE
        elif sentiment == 'negative':
            return ThemeConfig.SENTIMENT_NEGATIVE
        else:
            return ThemeConfig.SENTIMENT_NEUTRAL
    
    @staticmethod
    def render_sentiment_badge(sentiment, confidence=None):
        """Render a sentiment badge with color"""
        color = ThemeConfig.get_color_for_sentiment(sentiment)
        if confidence:
            return f'<span style="color: {color}; font-weight: 600;">{sentiment.upper()} ({confidence:.2%})</span>'
        return f'<span style="color: {color}; font-weight: 600;">{sentiment.upper()}</span>'
    
    @staticmethod
    def render_metric_card(title, value, description="", color=None):
        """Render a metric card"""
        if color is None:
            color = ThemeConfig.ACCENT_PRIMARY
        
        return f"""
        <div style="
            background: linear-gradient(135deg, rgba(57, 255, 20, 0.1), rgba(0, 255, 255, 0.1));
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        ">
            <p style="color: {ThemeConfig.TEXT_SECONDARY}; margin: 0; font-size: 0.9em;">{title}</p>
            <h3 style="color: {color}; margin: 5px 0; font-size: 2em;">{value}</h3>
            <p style="color: {ThemeConfig.TEXT_SECONDARY}; margin: 0; font-size: 0.85em;">{description}</p>
        </div>
        """
