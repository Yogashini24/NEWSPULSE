"""
NewsPulse Dashboard Application
Requires: Python 3.11+
"""
import streamlit as st
import os
from theme_config import ThemeConfig
from auth import AuthenticationManager
from utils import DataProcessor

# Page configuration
st.set_page_config(
    page_title="NewsPulse Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme
ThemeConfig.apply_custom_styling()

# Initialize authentication
AuthenticationManager.init_session_state()


def render_login_page():
    """Render the login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>" * 3, unsafe_allow_html=True)
        
        # Logo and title
        st.markdown("""
            <div style="text-align: center; margin-bottom: 3em;">
                <h1 style="font-size: 4em; color: #39FF14; text-shadow: 0 0 20px rgba(57, 255, 20, 0.5);">
                    📰 NewsPulse
                </h1>
                <p style="color: #A0AEC0; font-size: 1.3em; margin-top: -1em;">
                    Advanced News Analytics Dashboard
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Login form
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(57, 255, 20, 0.1), rgba(0, 255, 255, 0.1));
                border: 2px solid #39FF14;
                border-radius: 10px;
                padding: 30px;
                margin-top: 2em;
            ">
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <h3 style="text-align: center; color: #39FF14; margin-bottom: 1.5em;">
                Admin Login
            </h3>
        """, unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        col_login, col_spacer = st.columns([1, 1])
        
        with col_login:
            if st.button("🔓 Login", use_container_width=True, key="login_button"):
                if username and password:
                    if AuthenticationManager.verify_credentials(username, password):
                        AuthenticationManager.set_authenticated(username)
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                else:
                    st.warning("⚠️ Please enter username and password.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Default credentials info
        st.markdown("""
            <div style="
                background: rgba(96, 165, 250, 0.1);
                border-left: 4px solid #60A5FA;
                padding: 15px;
                border-radius: 6px;
                margin-top: 2em;
                text-align: center;
            ">
                <p style="color: #A0AEC0; margin: 0; font-size: 0.9em;">
                    Demo Credentials:<br>
                    <strong style="color: #E2E8F0;">Username:</strong> admin<br>
                    <strong style="color: #E2E8F0;">Password:</strong> NewsPulse@2024
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>" * 5, unsafe_allow_html=True)


def render_header():
    """Render dashboard header"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown("""
            <h1 style="margin: 0; display: inline-flex; align-items: center; gap: 10px;">
                📰 NewsPulse Dashboard
            </h1>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True, key="logout_button"):
            AuthenticationManager.logout()
            st.rerun()


def render_homepage():
    """Render the dashboard homepage"""
    render_header()
    
    st.divider()
    
    # Welcome message
    username = AuthenticationManager.get_username()
    st.markdown(f"""
        <p style="color: #A0AEC0; font-size: 1.1em; margin-bottom: 2em;">
            Welcome back, <strong style="color: #39FF14;">{username}</strong>! 👋
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <h2 style="text-align: center; color: #39FF14; margin: 2em 0;">
            📊 Select Dashboard Section
        </h2>
    """, unsafe_allow_html=True)
    
    # Dashboard sections
    sections = [
        {
            "page": "recent_trending",
            "icon": "🔥",
            "title": "Recent & Trending News",
            "description": "Explore the latest and trending news articles from various sources.",
            "color": "#FF6B6B"
        },
        {
            "page": "trending_keywords",
            "icon": "🔤",
            "title": "Trending Keywords & Topics",
            "description": "Discover the most discussed topics and keywords in news.",
            "color": "#4ECDC4"
        },
        {
            "page": "sentiment_analysis",
            "icon": "😊",
            "title": "Sentiment Analysis",
            "description": "View sentiment distribution of news articles.",
            "color": "#45B7D1"
        },
        {
            "page": "model_performance",
            "icon": "📈",
            "title": "Model Performance Metrics",
            "description": "Check the accuracy and performance metrics of our sentiment model.",
            "color": "#96CEB4"
        },
        {
            "page": "overall_summary",
            "icon": "📋",
            "title": "Overall Summary",
            "description": "Comprehensive overview of all insights and analytics.",
            "color": "#FFEAA7"
        }
    ]
    
    # Create grid of section buttons
    cols = st.columns(2)
    
    for idx, section in enumerate(sections):
        col = cols[idx % 2]
        
        with col:
            if st.button(
                f"{section['icon']} {section['title']}",
                key=f"btn_{section['page']}",
                use_container_width=True,
                help=section['description']
            ):
                st.session_state.selected_page = section['page']
                st.rerun()
            
            st.markdown(f"""
                <p style="color: #A0AEC0; margin: 5px 0 15px 0; font-size: 0.9em;">
                    {section['description']}
                </p>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick stats
    st.markdown("""
        <h3 style="color: #39FF14; margin-top: 2em;">⚡ Quick Stats</h3>
    """, unsafe_allow_html=True)
    
    try:
        from news_scraper import NewsScraperDatabase
        db = NewsScraperDatabase()
        all_news = db.get_all_news(limit=10000)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total News Articles", len(all_news), delta="Updated", delta_color="off")
        
        with col2:
            st.metric("Categories", len(set([n.get('category', 'general') for n in all_news])), delta="Diverse", delta_color="off")
        
        with col3:
            st.metric("News Sources", len(set([n.get('source', 'Unknown') for n in all_news])), delta="Multiple", delta_color="off")
        
        with col4:
            st.metric("Dashboard Status", "🟢 Operational", delta="Active", delta_color="off")
    
    except Exception as e:
        st.info("📊 Dashboard statistics will be available after data is loaded.")


def main():
    """Main application"""
    if AuthenticationManager.is_authenticated():
        # Check if a specific page is selected
        if 'selected_page' in st.session_state and st.session_state.selected_page:
            page = st.session_state.selected_page
            
            if page == "recent_trending":
                from pages import recent_trending
                recent_trending.render(render_header)
            elif page == "trending_keywords":
                from pages import trending_keywords
                trending_keywords.render(render_header)
            elif page == "sentiment_analysis":
                from pages import sentiment_analysis
                sentiment_analysis.render(render_header)
            elif page == "model_performance":
                from pages import model_performance
                model_performance.render(render_header)
            elif page == "overall_summary":
                from pages import overall_summary
                overall_summary.render(render_header)
            else:
                st.session_state.selected_page = None
                render_homepage()
        else:
            render_homepage()
    else:
        render_login_page()


if __name__ == "__main__":
    main()
