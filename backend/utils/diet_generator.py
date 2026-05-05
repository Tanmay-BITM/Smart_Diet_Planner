import random
import pandas as pd

from backend.config import DAYS, MEALS


def generate_weekly_plan(food_df: pd.DataFrame, cluster_id: int) -> dict:
    """
    Build a 7-day meal plan from foods belonging to *cluster_id*.

    If the cluster has fewer than 3 foods, falls back to the full dataset
    so we always have something to show.

    Returns
    -------
    dict  {day: {meal: food_name}}
    """
    cluster_foods = food_df[food_df["cluster"] == cluster_id]["food_name"].tolist()

    # Fallback: use all foods if cluster is too small
    if len(cluster_foods) < 3:
        cluster_foods = food_df["food_name"].tolist()

    plan: dict = {}
    for day in DAYS:
        plan[day] = {}
        # Sample without replacement per day where possible
        sample_size = min(len(cluster_foods), len(MEALS))
        daily_foods = random.sample(cluster_foods, sample_size)
        # If cluster smaller than meals, allow repeats
        while len(daily_foods) < len(MEALS):
            daily_foods.append(random.choice(cluster_foods))
        for meal, food in zip(MEALS, daily_foods):
            plan[day][meal] = food

    return plan
