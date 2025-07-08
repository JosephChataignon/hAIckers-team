# import streamlit as st
# from utils.session_manager import navigate_to

# def onboarding_view():
#     """Display the onboarding/welcome view"""
#     st.title("Welcome to Your Healthy Food App")
    
#     st.markdown("""
#     #### Get Started with Your Personalized Journey for Healthy Eating

#     Say goodbye to "recipe block" and cut the boring parts off. We'll 
#     suggest you healthy recipes tailored to your needs and preferences 
#     and order the ingredients for you so you can focus on the fun part: 
#     actually cooking !
    
#     Start by creating an account or logging in.
#     """)
    
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         if st.button("Login to Existing Account", use_container_width=True):
#             navigate_to('login')
#             st.rerun()
    
#     with col2:
#         if st.button("Create New Account", use_container_width=True):
#             navigate_to('register')
#             st.rerun()



import streamlit as st
from utils.session_manager import navigate_to

def onboarding_view():
    """Display the onboarding/welcome view"""
    
    # Custom styling
    st.markdown("""
    <style>
        .main-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #ff7f50;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 1.3rem;
            font-weight: 500;
            color: #444;
        }
        .highlight-box {
            background-color: #fff7f0;
            border-left: 6px solid #ffa366;
            padding: 1.2rem 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 10px rgba(255, 145, 77, 0.1);
        }
        .custom-button > button {
            background-color: #ffa366 !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            border-radius: 10px !important;
            padding: 0.75rem 1.2rem !important;
            margin-top: 1rem;
        }
        .custom-button > button:hover {
            background-color: #ff7f50 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🥗 Welcome to LeCommis</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Personalized Assistant for Healthy & Effortless Cooking</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="highlight-box">
        ✅ Say goodbye to recipe block and boring meals.<br>
        ✅ Get AI-powered healthy recipes tailored to your goals.<br>
        ✅ Automatically shop ingredients – you just cook and enjoy!<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 👇 Get started by logging in or creating a free account:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-button">', unsafe_allow_html=True)
        if st.button("Login to Your Account", use_container_width=True):
            navigate_to('login')
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-button">', unsafe_allow_html=True)
        if st.button("Create New Account", use_container_width=True):
            navigate_to('register')
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
