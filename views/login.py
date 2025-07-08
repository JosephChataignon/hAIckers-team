# import streamlit as st
# from utils.database import authenticate_user
# from utils.session_manager import navigate_to, login_user

# def login_view():
#     """Display the login view"""
#     st.title("🔐 Login")
#     """Display the login view"""
    
#     with st.form("login_form"):
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             login_button = st.form_submit_button("Login", use_container_width=True)
#         with col2:
#             back_button = st.form_submit_button("Back to Home", use_container_width=True)
    
#     if login_button:
#         if username and password:
#             user_data = authenticate_user(username, password)
#             if user_data is not None:
#                 login_user(user_data)
#                 st.success("Login successful!")
#                 st.rerun()
#             else:
#                 st.error("Invalid username or password")
#         else:
#             st.error("Please enter both username and password")
    
#     if back_button:
#         navigate_to('onboarding')
#         st.rerun()

import streamlit as st
from utils.database import authenticate_user
from utils.session_manager import navigate_to, login_user

def login_view():
    """Display the login view"""

    # Load styles
    st.markdown("""
    <style>
        .login-title {
            font-size: 2.2rem;
            font-weight: bold;
            color: #e67300;
            margin-bottom: 0.5rem;
        }
   
        .custom-button > button {
            background-color: #ffc107 !important;
            color: black !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.2rem !important;
        }
        .custom-button > button:hover {
            background-color: #ffb300 !important;
        }
        .forgot-link {
            font-size: 0.9rem;
            color: #0072C6;
            text-decoration: underline;
            cursor: pointer;
            margin-bottom: 1rem;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<div class="login-title">🔐 Login to Continue</div>', unsafe_allow_html=True)

    # Container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # State for showing forgot password message
    if "forgot_password" not in st.session_state:
        st.session_state.forgot_password = False

    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.session_state.forgot_password:
            st.info("📧 To reset your password, please check your email inbox. A recovery link has been sent.")

        # This is a real-looking clickable "forgot password" link
        st.markdown('<a class="forgot-link" href="#" onclick="window.location.reload();">🔘 Forgot password?</a>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.markdown('<div class="custom-button">', unsafe_allow_html=True)
                login_button = st.form_submit_button("➡️ Login", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            with st.container():
                st.markdown('<div class="custom-button">', unsafe_allow_html=True)
                back_button = st.form_submit_button("🏠 Back to Home", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Handle login
    if login_button:
        if username and password:
            user_data = authenticate_user(username, password)
            if user_data is not None:
                login_user(user_data)
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
        else:
            st.error("⚠️ Please enter both username and password.")

    # Handle navigation
    if back_button:
        navigate_to('onboarding')
        st.rerun()

