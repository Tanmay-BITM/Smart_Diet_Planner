"""
Streamlit entry point for the Smart Weekly Diet Planner.

Run with:
    streamlit run frontend/app.py
"""
import sys
import os

# Ensure the project root is on the path so backend imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from frontend.pages.home import render_home
from frontend.pages.results import render_results

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Diet Planner",
    page_icon="🥗",
    layout="centered",
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
_css_path = os.path.join(os.path.dirname(__file__), "styles", "style.css")
if os.path.exists(_css_path):
    with open(_css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Backend pipeline (cached so it only runs once) ────────────────────────────
@st.cache_resource
def load_pipeline():
    from backend.config import DATA_PATH
    from backend.utils.preprocessing import load_and_preprocess
    from backend.models.kmeans_model import train_kmeans

    raw = load_and_preprocess(DATA_PATH)
    _, food_data = train_kmeans(raw)
    return food_data


food_data = load_pipeline()

# ── Render pages ──────────────────────────────────────────────────────────────
user_input = render_home()

if user_input:
    from backend.services.diet_services import generate_plan

    with st.spinner("Generating your personalised diet plan…"):
        bmi_value, bmi_category, diet_label, weekly_plan = generate_plan(
            weight=user_input["weight"],
            height=user_input["height"],
            goal=user_input["goal"],
            food_data=food_data,
        )

    render_results(bmi_value, bmi_category, diet_label, weekly_plan)
