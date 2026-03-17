import streamlit as st


class AuthenticationManager:
    """Simple session-based authentication manager for Streamlit."""

    DEFAULT_USERNAME = "admin"
    DEFAULT_PASSWORD = "NewsPulse@2024"

    @staticmethod
    def init_session_state():
        """Ensure required auth keys exist in session_state."""
        if "is_authenticated" not in st.session_state:
            st.session_state.is_authenticated = False
        if "username" not in st.session_state:
            st.session_state.username = ""
        if "selected_page" not in st.session_state:
            st.session_state.selected_page = None

    @staticmethod
    def verify_credentials(username: str, password: str) -> bool:
        """Check provided credentials against defaults."""
        return (
            username == AuthenticationManager.DEFAULT_USERNAME
            and password == AuthenticationManager.DEFAULT_PASSWORD
        )

    @staticmethod
    def set_authenticated(username: str) -> None:
        """Mark user as logged in and store username."""
        st.session_state.is_authenticated = True
        st.session_state.username = username

    @staticmethod
    def is_authenticated() -> bool:
        """Return current authentication status."""
        return bool(st.session_state.get("is_authenticated", False))

    @staticmethod
    def get_username() -> str:
        """Return current username, or a default label."""
        return st.session_state.get("username", "Admin")

    @staticmethod
    def logout() -> None:
        """Log out the current user and clear page selection."""
        st.session_state.is_authenticated = False
        st.session_state.username = ""
        st.session_state.selected_page = None

