"""Results page – display BMI, diet type, and weekly plan."""
import streamlit as st
from frontend.components.ui_elements import bmi_card, diet_type_badge, weekly_plan_table


def render_results(bmi: float, bmi_category: str, diet_label: str, weekly_plan: dict):
    st.divider()
    st.subheader("📊 Your Results")

    col1, col2 = st.columns([1, 1])
    with col1:
        bmi_card(bmi, bmi_category)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        diet_type_badge(diet_label)

    st.subheader("📅 Your 7-Day Meal Plan")
    weekly_plan_table(weekly_plan)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "💡 This plan is generated based on your BMI and fitness goal using "
        "K-Means food clustering and an ID3 decision tree. "
        "Consult a nutritionist for medical advice."
    )
