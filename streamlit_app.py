# ==================== main.py ====================
import streamlit as st
from views.onboarding import onboarding_view
from views.login import login_view
from views.register import register_view
from views.dashboard import dashboard_view
from views.meal_preparation import meal_preparation_view
from views.recipe_choice import recipe_choice_view
from views.ordering import ordering_view
from utils.session_manager import initialize_session_state

# ✅ First Streamlit command — set config early
st.set_page_config(
    page_title="Health App",
    page_icon="🏥",
    layout="wide"
)

# ✅ Custom theme applied globally
def apply_custom_theme():
    st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background-color: #fffdf9;
                color: #2c2c2c;
            }
            [data-testid="stSidebar"] {
                background-color: #fff4e6;
                color: #2c2c2c;
            }
            h1, h2, h3 {
                color: #ff914d;
            }
            .stButton>button, .stForm button {
                background-color: #ffa366 !important;
                color: white !important;
                border-radius: 8px !important;
                padding: 0.6rem 1.2rem !important;
                font-weight: bold !important;
                border: none !important;
            }
            .stButton>button:hover, .stForm button:hover {
                background-color: #ff924c !important;
            }
            input[type="text"], input[type="password"], input[type="number"], textarea {
                background-color: #fffaf4 !important;
                color: #2c2c2c !important;
                border: 1px solid #ddd !important;
                border-radius: 6px !important;
                padding: 8px !important;
            }
            [data-testid="stTextInput"] > div:has(input[type="password"]) {
                background-color: #fffaf4 !important;
                border: 1px solid #ddd !important;
                border-radius: 6px !important;
                padding-right: 0.5rem !important;
            }
            [data-testid="stTextInput"] svg {
                color: #ff914d !important;
                background: none !important;
                padding: 0 !important;
                margin: 0 !important;
                border-radius: 0 !important;
                width: 1.2em !important;
                height: 1.2em !important;
                cursor: pointer;
            }
            input::-webkit-outer-spin-button,
            input::-webkit-inner-spin-button {
                -webkit-appearance: none;
                margin: 0;
            }
            .stSelectbox div[data-baseweb="select"] {
                background-color: #fffaf4 !important;
                color: #2c2c2c !important;
                border: 1px solid #ddd !important;
                border-radius: 6px !important;
                padding: 4px;
            }



            
                   /* Generic container styling */
            [data-testid="stAlert"] {
                color: #000000 !important;
                font-weight: 600 !important;
            }
        
            /* Specific background colors for alert types */
            [data-testid="stAlert"][data-type="success"] {
                background-color: #e8fff0 !important;
            }
        
            [data-testid="stAlert"][data-type="error"] {
                background-color: #ffeaea !important;
            }
        
            [data-testid="stAlert"][data-type="warning"] {
                background-color: #fff8e1 !important;
            }
        
            [data-testid="stAlert"][data-type="info"] {
                background-color: #e7f3ff !important;
            }
        
            /* Padding for alert content */
            [data-testid="stAlert"] > div {
                padding: 1rem !important;
            }
        
            /* Target text elements inside alert box */
            [data-testid="stAlert"] * {
                color: #000000 !important;
            }
        </style>
    """, unsafe_allow_html=True)


# ✅ Apply theme once at app start
apply_custom_theme()

def main():
    """Main application logic"""
    initialize_session_state()

    # Route to appropriate view based on session state
    if st.session_state.current_view == 'onboarding':
        onboarding_view()
    elif st.session_state.current_view == 'login':
        login_view()
    elif st.session_state.current_view == 'register':
        register_view()
    elif st.session_state.current_view == 'dashboard' and st.session_state.authenticated:
        dashboard_view()
    elif st.session_state.current_view == 'meal_preparation' and st.session_state.authenticated:
        meal_preparation_view()
    elif st.session_state.current_view == 'recipe_choice' and st.session_state.authenticated:
        recipe_choice_view()
    elif st.session_state.current_view == 'ordering' and st.session_state.authenticated:
        ordering_view()
    else:
        st.session_state.current_view = 'onboarding'
        st.session_state.authenticated = False
        st.rerun()

if __name__ == "__main__":
    main()
