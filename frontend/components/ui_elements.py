"""Reusable Streamlit UI components."""
import streamlit as st


def bmi_card(bmi: float, category: str):
    """Render a styled BMI result card."""
    color_map = {
        "Underweight": "#3b82f6",
        "Normal":      "#22c55e",
        "Overweight":  "#f59e0b",
        "Obese":       "#ef4444",
    }
    color = color_map.get(category, "#6b7280")
    st.markdown(
        f"""
        <div style="
            background:{color}18;
            border-left:5px solid {color};
            border-radius:8px;
            padding:16px 20px;
            margin-bottom:16px;
        ">
            <h3 style="margin:0;color:{color}">BMI: {bmi}</h3>
            <p style="margin:4px 0 0;font-size:1rem;color:{color}">
                Category: <strong>{category}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def diet_type_badge(diet_label: str):
    """Render a badge showing the recommended diet type."""
    badge_colors = {
        "Low Calorie":  "#f59e0b",
        "High Protein": "#3b82f6",
        "Balanced":     "#22c55e",
    }
    color = badge_colors.get(diet_label, "#6b7280")
    st.markdown(
        f"""
        <div style="
            display:inline-block;
            background:{color};
            color:#fff;
            border-radius:20px;
            padding:6px 18px;
            font-weight:600;
            font-size:0.95rem;
            margin-bottom:16px;
        ">
            Recommended Diet: {diet_label}
        </div>
        """,
        unsafe_allow_html=True,
    )


def weekly_plan_table(plan: dict):
    """Render the 7-day meal plan as a styled HTML table."""
    rows = ""
    for day, meals in plan.items():
        breakfast = meals.get("Breakfast", "—")
        lunch     = meals.get("Lunch", "—")
        dinner    = meals.get("Dinner", "—")
        rows += f"""
        <tr>
            <td><strong>{day}</strong></td>
            <td>{breakfast}</td>
            <td>{lunch}</td>
            <td>{dinner}</td>
        </tr>
        """

    st.markdown(
        f"""
        <style>
            .diet-table {{
                width:100%;
                border-collapse:collapse;
                font-size:0.92rem;
            }}
            .diet-table th {{
                background:#1e293b;
                color:#f8fafc;
                padding:10px 14px;
                text-align:left;
            }}
            .diet-table td {{
                padding:9px 14px;
                border-bottom:1px solid #e2e8f0;
            }}
            .diet-table tr:nth-child(even) td {{
                background:#f8fafc;
            }}
            .diet-table tr:hover td {{
                background:#e0f2fe;
            }}
        </style>
        <table class="diet-table">
            <thead>
                <tr>
                    <th>Day</th>
                    <th>🌅 Breakfast</th>
                    <th>☀️ Lunch</th>
                    <th>🌙 Dinner</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )
