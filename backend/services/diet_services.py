import pandas as pd

from backend.utils.bmi import calculate_bmi
from backend.models.decision_tree import decide_diet_type
from backend.utils.diet_generator import generate_weekly_plan


def generate_plan(
    weight: float,
    height: float,
    goal: str,
    food_data: pd.DataFrame,
) -> tuple[float, str, str, dict]:
    """
    Orchestrate the full pipeline.

    Parameters
    ----------
    weight    : kg
    height    : cm
    goal      : "Weight Loss" | "Weight Gain" | "Maintenance"
    food_data : preprocessed + clustered DataFrame

    Returns
    -------
    (bmi_value, bmi_category, diet_label, weekly_plan)
    """
    bmi_value, bmi_category = calculate_bmi(weight, height)
    diet_label, cluster_id = decide_diet_type(bmi_value, goal)
    weekly_plan = generate_weekly_plan(food_data, cluster_id)

    return bmi_value, bmi_category, diet_label, weekly_plan
