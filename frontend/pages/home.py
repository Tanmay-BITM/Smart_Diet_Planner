"""Home page – user input form."""
import streamlit as st


def render_home():
    st.title("🥗 Smart Weekly Diet Planner")
    st.markdown(
        "Enter your health details below and get a personalised 7-day meal plan "
        "powered by K-Means Clustering and an ID3 Decision Tree."
    )
    st.divider()

    with st.form("diet_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=25, step=1)
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
            weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.5)

        with col2:
            activity_level = st.selectbox(
                "Activity Level",
                ["Sedentary", "Lightly Active", "Moderate", "Very Active", "Extra Active"],
                index=2,
            )
            goal = st.selectbox(
                "Fitness Goal",
                ["Weight Loss", "Weight Gain", "Maintenance"],
            )

        submitted = st.form_submit_button("🚀 Generate Diet Plan", use_container_width=True)

    if submitted:
        return {
            "age": age,
            "height": height,
            "weight": weight,
            "activity_level": activity_level,
            "goal": goal,
        }
    return None
