
# import streamlit as st
# import json
# from utils.session_manager import navigate_to
# import re

# #


# def recipe_choice_view():
#     """Display the recipe choice view with API recommendations"""
#     st.title("🍽️ Recipe Recommendations")

#     if 'meal_recommendations' not in st.session_state:
#         st.error("No meal recommendations found. Please go back and try again.")
#         if st.button("← Back to Meal Preparation"):
#             navigate_to('meal_preparation')
#             st.rerun()
#         return

#     st.markdown("### What do you want to eat today?")


#     try:
#         recommendations = st.session_state.meal_recommendations
#         start = recommendations.find('{')
#         end = recommendations.rfind('}')
#         json_str = recommendations[start:end+1]
#         recipes = json.loads(json_str)

#         # CSS styling for animated cards
#         st.markdown("""
#         <style>
#             .recipe-card {
#                 background: #fffaf4;
#                 border: 2px solid #ff924c;
#                 border-radius: 15px;
#                 padding: 1.5rem;
#                 margin-bottom: 1.5rem;
#                 box-shadow: 0 4px 12px rgba(255, 145, 77, 0.2);
#                 transition: transform 0.2s ease, box-shadow 0.3s ease;
#             }
#             .recipe-card:hover {
#                 transform: scale(1.02);
#                 box-shadow: 0 6px 18px rgba(255, 145, 77, 0.3);
#             }
#             .recipe-title {
#                 color: #ff914d;
#                 font-size: 1.5rem;
#                 font-weight: bold;
#                 margin-bottom: 0.5rem;
#             }
#             .recipe-meta {
#                 font-size: 0.9rem;
#                 color: #555;
#                 margin-bottom: 1rem;
#             }
#             .recipe-button {
#                 background-color: #ffa366;
#                 color: white;
#                 padding: 0.5rem 1rem;
#                 border: none;
#                 border-radius: 8px;
#                 font-weight: bold;
#                 cursor: pointer;
#             }
#             .recipe-button:hover {
#                 background-color: #ff924c;
#             }
#             ..recipe-card ul, .recipe-card ol {
#     padding-left: 1.5rem;
#     margin-bottom: 1rem;
# }
# .recipe-card ol {
#     list-style-type: decimal;
# }
# .recipe-card ul {
#     list-style-type: none;
# }

#         </style>
#         """, unsafe_allow_html=True)


                 
        
        

#         for i, recipe in enumerate(recipes.values()):
            
#             raw_instruction_text = recipe["instructions"]
#             instruction_steps = re.split(r'\s*\d+\.\s*', raw_instruction_text)
#             instruction_steps = [step.strip() for step in instruction_steps if step.strip()]  # clean and remove empty
        
#             # Preprocess instruction steps
#             steps = '<ol style="margin-left: 1.2rem;">' + ''.join(
#             f"<li style='margin-bottom: 0.5rem;'> {step}</li>"
#             for step in instruction_steps) + '</ol>'



#             # Preprocess ingredients
#             ingredients_html = ''.join(
#                 f"<li><input type='checkbox' checked id='ing_{i}_{j}' style='margin-right:8px;'><label for='ing_{i}_{j}'>{ingredient}</label></li>"
#                 for j,ingredient in enumerate(recipe["ingredients"])
#             )

#             st.markdown(f"""
#                 <div class="recipe-card" id="recipe-card-{i}">
#                     <details>
#                         <summary style="
#                             font-weight: 700;
#                             font-size: 1.2rem;
#                             color: #ff6a00;
#                             cursor: pointer;
#                             outline: none;
#                         ">
#                             {recipe['title']} 
#                             <div style='font-weight: normal; font-size: 0.9rem; color: #444;'> 
#                                 — {recipe['time']} Min | {recipe['calories']} kCal | {recipe['fiber']}g fiber | {recipe['protein']}g protein
#                             </div>
#                         </summary>
#                         <div style="margin-top: 1rem;">
#                             <strong>Ingredients:</strong>
#                                 <ul>
#                                     {ingredients_html}
#                                 </ul>
#                             <strong>Instructions:</strong>
#                             {steps}
#                         </div>
#                     </details>
#                 </div>
#             """, unsafe_allow_html=True)

#             # Functional Streamlit button outside the card
#             if st.button(f"↑ Choose this recipe", key=f"choose_{i}"):
#                 st.session_state.selected_recipe = {
#                     "title": recipe["title"],
#                     "ingredients": recipe["ingredients"],
#                     "instructions": recipe["instructions"]
#                 }
#                 navigate_to('ordering')
#                 st.rerun()


#             # Optional Streamlit-side selection logic if needed
#             if st.session_state.get(f"choose_{i}"):
#                 st.session_state.selected_recipe = {
#                     "title": recipe["title"],
#                     "ingredients": recipe["ingredients"],
#                     "instructions": recipe["instructions"]
#                 }
#                 navigate_to('ordering')
#                 st.rerun()

#     except json.JSONDecodeError:
#         st.warning(f"Could not parse AI response: {recommendations}")

#     # Navigation buttons
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("← Back to Meal Preparation", use_container_width=True):
#             navigate_to('meal_preparation')
#             st.rerun()
#     with col2:
#         if st.button("🏠 Back to Dashboard", use_container_width=True):
#             navigate_to('dashboard')
#             st.rerun()

# --------------------------------------------------------------------------------

import streamlit as st
import json
import re
from utils.session_manager import navigate_to

def recipe_choice_view():
    st.title("🍽️ Recipe Recommendations")

    static_images = {
        "1": "https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg",
        "2": "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg",
        "3": "https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg"
    }

    if 'meal_recommendations' not in st.session_state:
        st.error("No meal recommendations found.")
        if st.button("← Back to Meal Preparation"):
            navigate_to('meal_preparation')
            st.rerun()
        return

    st.markdown("### What do you want to eat today?")

    try:
        recommendations = st.session_state.meal_recommendations
        start = recommendations.find('{')
        end = recommendations.rfind('}')
        json_str = recommendations[start:end+1]
        recipes = json.loads(json_str)

        for i, recipe in enumerate(recipes.values()):
            image_url = static_images.get(str(i + 1), "")

            raw_instruction_text = recipe["instructions"]
            instruction_steps = re.split(r'\s*\d+\.\s*', raw_instruction_text)
            instruction_steps = [step.strip() for step in instruction_steps if step.strip()]
            steps = ''.join(f"<li>{step}</li>" for step in instruction_steps)

            ingredients_html = ''.join(
                f"<li><input type='checkbox' checked id='ing_{i}_{j}' style='margin-right:8px;'>"
                f"<label for='ing_{i}_{j}'>{ingredient}</label></li>"
                for j, ingredient in enumerate(recipe["ingredients"])
            )

            st.markdown(f"""
                <div style="background:#fffaf4; border:2px solid #ff924c; border-radius:15px;
                            padding:1.5rem; margin-bottom:1.5rem; box-shadow:0 4px 12px rgba(255, 145, 77, 0.2);">
                    <details>
                        <summary style="font-weight:700; font-size:1.2rem; color:#ff6a00; cursor:pointer;">
                            {recipe['title']}
                            <div style="font-weight:normal; font-size:0.9rem; color:#444;">
                                — {recipe['time']} Min | {recipe['calories']} kCal | {recipe['fiber']}g fiber | {recipe['protein']}g protein
                            </div>
                        </summary>
                        <div style="margin-top:1rem;">
                            <img src="{image_url}" alt="Recipe image"
                                style="width:100%; max-height:200px; object-fit:cover; border-radius:12px; margin-bottom:1rem;" />
                            <strong>Ingredients:</strong>
                            <ul>{ingredients_html}</ul>
                            <strong>Instructions:</strong>
                            <ol>{steps}</ol>
                        </div>
                    </details>
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"↑ Choose this recipe", key=f"choose_{i}"):
                st.session_state.selected_recipe = {
                    "title": recipe["title"],
                    "ingredients": recipe["ingredients"],
                    "instructions": recipe["instructions"]
                }
                navigate_to("ordering")
                st.rerun()

    except json.JSONDecodeError:
        st.warning("Could not parse AI response")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Meal Preparation", use_container_width=True):
            navigate_to('meal_preparation')
            st.rerun()
    with col2:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            navigate_to('dashboard')
            st.rerun()

