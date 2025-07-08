import streamlit as st
from utils.session_manager import navigate_to
from utils.groq_client import GroqClient

def meal_preparation_view():
    """Display the meal preparation view"""
    st.title("🥗 Meal Preparation")
    
     
    # Get user data from session
    user_data = st.session_state.user_data
    
    # Main question and input
    st.subheader("Let's Plan Your Meal")
    
    with st.form("meal_preferences_form"):
        # Text field for meal preferences
        meal_preferences = st.text_area(
            "Do you have any preference for today's meal?",
            placeholder="I want something light and healthy, or I need a quick 20-minute meal...",
            height=100
        )
        
        # Buttons
        col1, col2 = st.columns(2)
        with col1:
            proceed_button = st.form_submit_button("Proceed", use_container_width=True)
        with col2:
            back_button = st.form_submit_button("← Back to Dashboard", use_container_width=True)
    
    # Handle form submission
    if proceed_button:
        try:
            # Show loading spinner
            with st.spinner("Generating personalized meal recommendations..."):
                # Initialize Groq client
                groq_client = GroqClient()
                
                # Make API call to generate meal recommendations
                meal_recommendations = groq_client.generate_meal_recommendations(
                    user_data=user_data,
                    meal_preferences=meal_preferences
                )
                
                if meal_recommendations:
                    # Store the API response in session state
                    st.session_state.meal_recommendations = meal_recommendations
                    st.session_state.user_meal_preferences = meal_preferences
                    
                    # Navigate to recipe choice view
                    navigate_to('recipe_choice')
                    st.rerun()
                else:
                    st.error("Sorry, we couldn't generate meal recommendations at this time. Please try again.")
                    
        except Exception as e:
            st.error(f"An error occurred while generating recommendations: {str(e)}")
    
    if back_button:
        navigate_to('dashboard')
        st.rerun()