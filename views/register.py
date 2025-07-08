# import streamlit as st
# import json
# from utils.database import create_user
# from utils.session_manager import navigate_to
# from utils.groq_client import GroqClient

# def register_view():
#     """Display the registration view"""
#     st.title("📝 Create New Account")

#     st.markdown("""
#     In order to help you plan meals that are adapted for you, we need some information 
#     to make you nutrition profile.
#     """)
    
#     with st.form("register_form"):
        
#         col1, col2 = st.columns(2)
#         with col1:
#             username = st.text_input("Username")
#         with col2:
#             password = st.text_input("Password", type="password")
    
#         # Age and Sex in one row
#         col3, col4 = st.columns(2)
#         with col3:
#             age = st.number_input("Age", min_value=1, max_value=120, value=25)
#         with col4:
#             sex = st.selectbox("Sex", ["M", "F"])
    
#         # Weight and Height in one row
#         col5, col6 = st.columns(2)
#         with col5:
#             weight = st.number_input("Weight (kg)", min_value=1, max_value=500, value=70)
#         with col6:
#             height = st.number_input("Height (cm)", min_value=1, max_value=300, value=170)
#         # username = st.text_input("Username")
#         # password = st.text_input("Password", type="password")
#         # age = st.number_input("Age", min_value=1, max_value=120, value=25)
#         # sex = st.selectbox("Sex", ["M", "F"])
#         # weight = st.number_input("Weight (kg)", min_value=1, max_value=500, value=70)
#         # height = st.number_input("Height (cm)", min_value=1, max_value=300, value=170)
#         #TODO: set common restrictions (vegetarian etc) as one-click inserts
#         restrictions = st.text_area("Dietary Restrictions", placeholder="vegetarian, gluten-free, etc.")
#         allergies = st.text_area("Any allergies we should know about ?")
#         preferences = st.text_area("Any other preferences ?", placeholder="I like Chinese cuisine, I have a sweet tooth...")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             register_button = st.form_submit_button("Create Account", use_container_width=True)
#         with col2:
#             back_button = st.form_submit_button("Back to Home", use_container_width=True)
    
#     if register_button:
#         if username and password:
#             try:
#                 # Show loading message
#                 with st.spinner("Generating personalized dietary goals..."):
#                     try:
#                         # Initialize Groq client
#                         groq_client = GroqClient()
                        
#                         # Generate dietary goals using LLM
#                         dietary_goals_response = groq_client.generate_dietary_goals(
#                             age, sex, weight, height
#                         )
#                     except Exception as e:
#                         st.error(f"API call failed: {e}, proceeding with account creation.")
                    
#                     if dietary_goals_response:
#                         try:
#                             # Parse JSON response
#                             start = dietary_goals_response.find('{')
#                             end = dietary_goals_response.rfind('}')
#                             json_str = dietary_goals_response[start:end+1]
#                             goals_data = json.loads(json_str)
                            
#                             # Format dietary goals for storage
#                             dietary_goals = f"Daily Calories: {goals_data['calories']}, Fiber: {goals_data['fiber']}g, Protein: {goals_data['protein']}g"
                            
#                             # Show generated goals to user
#                             st.success("✅ Dietary goals generated successfully!")
#                             st.info(f"**Generated Goals:** {dietary_goals}")
#                             if 'explanation' in goals_data:
#                                 st.info(f"**Explanation:** {goals_data['explanation']}")
                            
#                         except json.JSONDecodeError:
#                             st.warning(f"Could not parse AI response: {dietary_goals_response}")
#                     else:
#                         st.error("failed to get dietary goals, using default instead")
#                         dietary_goals = "to be completed later"

#                 # merge user info
#                 dietary_restrictions = f"Restrictions: {restrictions} \nAllergies: {allergies}\nOther preferences: {preferences}"
#                 # Create user account with generated goals
#                 if create_user(username, password, age, sex, weight, height, dietary_restrictions, json.dumps(goals_data)):
#                     st.session_state.account_created = True
                                        
#             except Exception as e:
#                 st.error(f"Error during registration: {str(e)}")
#         else:
#             st.error("Please enter both username and password")

#     if st.session_state.get("account_created"):
#         st.success("Account created successfully! Please login.")
#         if st.button("Log In", use_container_width=True):
#             navigate_to('login')
#             st.rerun()
    
#     if back_button:
#         navigate_to('onboarding')
#         st.rerun()


import streamlit as st
import json
from utils.database import create_user
from utils.session_manager import navigate_to
from utils.groq_client import GroqClient

def register_view():
    st.markdown(
        "<h1 style='text-align: center; color: #4B8BBE;'>📝 Create Your Account</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; font-size: 16px;'>Let’s personalize your experience by setting up your nutrition profile.</p>",
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown("---")
        with st.form("register_form"):
            # Username and Password
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("👤 Username")
            with col2:
                password = st.text_input("🔒 Password", type="password")

            # Age and Sex
            col3, col4 = st.columns(2)
            with col3:
                age = st.number_input("🎂 Age", min_value=1, max_value=120, value=25)
            with col4:
                sex = st.selectbox("⚧️ Sex", ["M", "F"])

            # Weight and Height
            col5, col6 = st.columns(2)
            with col5:
                weight = st.number_input("⚖️ Weight (kg)", min_value=1, max_value=500, value=70)
            with col6:
                height = st.number_input("📏 Height (cm)", min_value=1, max_value=300, value=170)

            # Restrictions
            st.markdown("---")
            restrictions = st.text_area("🥗 Dietary Restrictions", placeholder="vegetarian, gluten-free, etc.")
            allergies = st.text_area("🚫 Allergies", placeholder="e.g., peanuts, shellfish")
            preferences = st.text_area("🍱 Preferences", placeholder="I like Chinese cuisine, I have a sweet tooth...")

            st.markdown("---")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                register_button = st.form_submit_button("✅ Create Account", use_container_width=True)
            with col_btn2:
                back_button = st.form_submit_button("↩️ Back to Home", use_container_width=True)

    # Register button logic
    if register_button:
        if username and password:
            try:
                with st.spinner("Generating personalized dietary goals..."):
                    try:
                        groq_client = GroqClient()
                        dietary_goals_response = groq_client.generate_dietary_goals(
                            age, sex, weight, height
                        )
                    except Exception as e:
                        st.error(f"API call failed: {e}, proceeding with account creation.")
                        dietary_goals_response = None

                    if dietary_goals_response:
                        try:
                            start = dietary_goals_response.find('{')
                            end = dietary_goals_response.rfind('}')
                            json_str = dietary_goals_response[start:end + 1]
                            goals_data = json.loads(json_str)

                            dietary_goals = f"Calories: {goals_data['calories']}, Fiber: {goals_data['fiber']}g, Protein: {goals_data['protein']}g"
                            st.success("✅ Dietary goals generated!")
                            st.info(f"**Your Goals:** {dietary_goals}")
                            if 'explanation' in goals_data:
                                st.caption(f"ℹ️ {goals_data['explanation']}")

                        except json.JSONDecodeError:
                            st.warning("⚠️ Could not parse response.")
                            dietary_goals = "to be completed later"
                    else:
                        dietary_goals = "to be completed later"

                dietary_restrictions = f"Restrictions: {restrictions}\nAllergies: {allergies}\nPreferences: {preferences}"
                if create_user(username, password, age, sex, weight, height, dietary_restrictions, json.dumps(goals_data)):
                    st.session_state.account_created = True

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.error("❗ Please fill in both username and password.")

    # After successful account creation
    if st.session_state.get("account_created"):
        st.success("🎉 Account created successfully! You can now log in.")
        if st.button("🔐 Log In", use_container_width=True):
            navigate_to('login')
            st.rerun()

    # Back to home
    if back_button:
        navigate_to('onboarding')
        st.rerun()
