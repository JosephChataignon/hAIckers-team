# import streamlit as st
# import json
# from utils.session_manager import navigate_to

# def ordering_view():
#     st.title("Ordering ingredients list")
    
#     if 'selected_recipe' not in st.session_state:
#         st.error("No recipe selected. Please go back and choose a recipe.")
#         if st.button("← Back to Recipe Choice"):
#             navigate_to('recipe_choice')
#             st.rerun()
#         return

#     recipe = st.session_state.selected_recipe

#     st.subheader(f"Ingredients for: {recipe['title']}")

#     for ingredient in recipe['ingredients']:
#         st.write(f"• {ingredient}")

#     st.markdown("---")
#     if st.button("← Back to Recipe Choice"):
#         navigate_to('recipe_choice')
#         st.rerun()

import streamlit as st
from utils.session_manager import navigate_to
import json
import time

def ordering_view():
    st.markdown("""
        <style>
            .main-card {
                background-color: #f5fff4;
                border-radius: 16px;
                padding: .5 rem;
                box-shadow: 0 4px 16px rgba(0, 128, 0, 0.1);
                margin-top: 2rem;
                margin-bottom: 2rem;
            }

            .page-title {
                font-size: 2.5rem;
                font-weight: 800;
                color: #ff6a00;
                text-align: center;
                margin-top: .5rem;
            }

            .subheader {
                font-size: 1.5rem;
                font-weight: 600;
                color: #2d572c;
                margin-bottom: 1rem;
            }

            .ingredient-item {
                font-size: 1.1rem;
                margin: 0.5rem 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            div.stButton > button {
                background: #ffa366;
                color: white;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                padding: 0.6rem 1.2rem;
                margin-top: 1.5rem;
                transition: background-color 0.3s ease;
            }

            div.stButton > button:hover {
                background: #ff914d;
            }

            .separator {
                margin: 1rem 0;
                border: none;
                height: 1px;
                background-color: #ddd;
            }

           

            .processing-text {
                font-size: 1.2rem;
                color: #6c757d;
                font-weight: 600;
                margin-bottom: 1rem;
            }

            .success-card {
                background-color: #d4edda;
                border: 2px solid #28a745;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                text-align: center;
            }

            .success-text {
                font-size: 1.2rem;
                color: #28a745;
                font-weight: 600;
                margin-bottom: 1rem;
            }

            .store-info {
                background-color: #fffbea;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            }

            .store-name {
                font-size: 1.1rem;
                font-weight: 600;
                color: #856404;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-title">🛒 Ingredient Checklist</div>', unsafe_allow_html=True)

    if 'selected_recipe' not in st.session_state:
        st.error("No recipe selected. Please go back and choose a recipe.")
        if st.button("← Back to Recipe Choice"):
            navigate_to('recipe_choice')
            st.rerun()
        return

    recipe = st.session_state.selected_recipe

    if 'order_state' not in st.session_state:
        st.session_state.order_state = 'ready'
    if 'order_step' not in st.session_state:
        st.session_state.order_step = 0
    if 'order_start_time' not in st.session_state:
        st.session_state.order_start_time = 0

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="subheader">Ingredients for: <span style="color:#ff6a00;">{recipe["title"]}</span></div>', unsafe_allow_html=True)

    for i, ingredient in enumerate(recipe['ingredients']):
        st.markdown(f"""
            <div class="ingredient-item">
                <input type="checkbox" checked />
                {ingredient}
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr class="separator">', unsafe_allow_html=True)

    if st.session_state.order_state == 'ready':
        col1, col2 = st.columns(2)

        with col1:
            if st.button("← Back to Recipe Choice",key="back_recipe_top"):
                navigate_to('recipe_choice')
                st.rerun()

        with col2:
            if st.button("🛒 Order Ingredients", key="order_button"):
                st.session_state.order_state = 'processing'
                st.session_state.order_step = 0
                st.session_state.order_start_time = time.time()
                st.rerun()

    elif st.session_state.order_state == 'processing':
        steps = [
            ("🔍 Searching nearby stores...", 2),
            ("🏪 Store selected: Franprix rue Saint-Honoré", 2),
            ("🔎 Searching ingredients...", 3),
            ("🛍️ Selecting best items for basket...", 2),
            ("✅ Finalizing basket...", 2)
        ]

        current_time = time.time()
        elapsed_time = current_time - st.session_state.order_start_time

        cumulative_time = 0
        current_step = 0

        for i, (step_text, duration) in enumerate(steps):
            if elapsed_time >= cumulative_time and elapsed_time < cumulative_time + duration:
                current_step = i
                break
            cumulative_time += duration
        else:
            st.session_state.order_state = 'completed'
            st.rerun()
            return

        st.markdown('<div class="processing-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="processing-text">{steps[current_step][0]}</div>', unsafe_allow_html=True)

        with st.spinner('Processing your order...'):
            time.sleep(0.5)

        st.markdown('</div>', unsafe_allow_html=True)

        if current_step > 0:
            st.markdown("**Completed steps:**")
            for i in range(current_step):
                st.markdown(f"✅ {steps[i][0]}")

        st.rerun()
    elif st.session_state.order_state == 'completed':
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
        st.markdown("""
            <div class="success-card">
                <div class="success-text">🎉 Order Ready!</div>
                <p>Your ingredients have been prepared and are ready for pickup.</p>
            </div>
        """, unsafe_allow_html=True)

    
        st.markdown("""
    <div class="store-info">
        <div class="store-name">📍 Franprix rue Saint-Honoré</div>
        <p>1 Rue Saint-Honoré, 75001 Paris<br>Open until 22:00 today</p>
    </div>
""", unsafe_allow_html=True)

    
        st.markdown('</div>', unsafe_allow_html=True)  # Close .main-card


 
        if st.button("🏪 Go to Store for Purchase"):
            st.success("Redirecting to store pickup page...")
            time.sleep(1)
            st.info("💡 In a real implementation, this would open the store's website or show directions to the pickup location.")

    if st.session_state.order_state == 'completed':
        if st.button("← Back to Recipe Choice", key="back_recipe_bottom"):
            navigate_to('recipe_choice')
            st.rerun()

    