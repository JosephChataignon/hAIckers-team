import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'onboarding'

def logout_user():
    """Clear user session and return to onboarding"""
    st.session_state.authenticated = False
    st.session_state.user_data = None
    st.session_state.current_view = 'onboarding'

def login_user(user_data):
    """Set user as authenticated and store user data"""
    st.session_state.authenticated = True
    st.session_state.user_data = user_data
    st.session_state.current_view = 'dashboard'

def navigate_to(view_name):
    """Navigate to a specific view"""
    st.session_state.current_view = view_name