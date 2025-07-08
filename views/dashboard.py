import streamlit as st
import json
from utils.session_manager import logout_user, navigate_to

def dashboard_view():
    """Display the main dashboard with user data"""
    user = st.session_state.user_data

    # Convert gender to full word
    gender_display = "Male" if user["SEX"] == "M" else "Female"

    st.markdown("<h1 style='color:#ff914d;'>👋 Welcome back, <span style='color:#333;'>{}</span>!</h1>".format(user['USER_NAME']), unsafe_allow_html=True)

    st.markdown("""
        <style>
            .metric-card {
                background-color: #fffaf4;
                padding: 1rem;
                border: 2px solid #ffa366;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(255,145,77,0.1);
                text-align: center;
                transition: transform 0.2s ease-in-out;
                margin-top: 1rem;
                margin-bottom: 1rem;
            }
            .metric-card:hover {
                transform: scale(1.02);
            }
            .cta-button {
                background-color: #ffa366;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 0.8rem 1.2rem;
                margin-top: 1rem;
            }
            .section-header {
                color: #ff914d;
                font-size: 1.3rem;
                font-weight: 700;
                margin-top: 2rem;
            }
            .styled-list {
                background-color: #fff4e6;
                padding: 1rem;
                border-radius: 10px;
                line-height: 1.8;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("🍳 Let's cook something delicious!", use_container_width=True):
        navigate_to('meal_preparation')
        st.rerun()

    st.markdown("<div class='section-header'>🧍 Your Profile</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'>👤<br><strong>Gender</strong><br>{gender_display}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'>🎂<br><strong>Age</strong><br>{user['AGE']}</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'>⚖️<br><strong>Weight</strong><br>{user['WEIGHT']} kg</div>", unsafe_allow_html=True)

    col4, col5 = st.columns(2)
    with col4:
        st.markdown(f"<div class='metric-card'>📏<br><strong>Height</strong><br>{user['HEIGHT']} cm</div>", unsafe_allow_html=True)
    with col5:
        bmi = user['WEIGHT'] / ((user['HEIGHT'] / 100) ** 2)
        st.markdown(f"<div class='metric-card'>📊<br><strong>BMI</strong><br>{bmi:.1f}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>🥦 Dietary Information</div>", unsafe_allow_html=True)

    with st.expander("🔎 View Restrictions and Preferences"):
        try:
            restrictions = user['DIETARY_RESTRICTIONS']

            # Attempt to extract 3 parts from the restriction string
            parsed = {
                "Restrictions": "",
                "Allergies": "",
                "Other Preferences": ""
            }

            if "Allergies" in restrictions:
                parts = restrictions.split("Allergies")
                parsed["Restrictions"] = parts[0].replace("Restrictions:", "").strip()
                if "Other preferences" in parts[1]:
                    allergy_part, other_part = parts[1].split("Other preferences")
                    parsed["Allergies"] = allergy_part.strip(": ,")
                    parsed["Other Preferences"] = other_part.strip(": ,")
                else:
                    parsed["Allergies"] = parts[1].strip(": ,")
            else:
                parsed["Restrictions"] = restrictions.strip()

            st.markdown(f"""<div class='styled-list'>
            <strong>🚫 Restrictions:</strong> {parsed["Restrictions"]}<br>
            <strong>⚠️ Allergies:</strong> {parsed["Allergies"]}<br>
            <strong>💡 Other Preferences:</strong> {parsed["Other Preferences"]}
            </div>""", unsafe_allow_html=True)

        except Exception as e:
            st.info(f"❌ No dietary restrictions specified. ({str(e)})")

    with st.expander("📈 View Your Dietary Goals"):
        try:
            goals = json.loads(user['DIETARY_GOALS'])
            st.markdown(f"""
            <div class='styled-list'>
            🔥 <strong>Calories:</strong> {goals['calories']} kCal<br>
            🌾 <strong>Fiber:</strong> {goals['fiber']} g<br>
            🥩 <strong>Protein:</strong> {goals['protein']} g
            </div>
            """, unsafe_allow_html=True)
        except:
            st.error(f"Could not parse: {user['DIETARY_GOALS']}")

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        logout_user()
        st.rerun()

