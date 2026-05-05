import pytest
import pandas as pd


@pytest.fixture
def sample_food_df():
    """Minimal food DataFrame with required columns and valid data."""
    return pd.DataFrame({
        "food_name": [
            "Oatmeal", "Cucumber Salad", "Steamed Broccoli",
            "Grilled Chicken", "Boiled Eggs", "Tuna",
            "Brown Rice", "Quinoa Bowl", "Whole Wheat Pasta",
        ],
        "calories":      [150, 45, 55, 220, 155, 130, 215, 222, 220],
        "protein":       [5,   2,  4,  42,  13,  28,  5,   8,   8],
        "carbohydrates": [27,  8,  11, 0,   1,   0,   45,  39,  43],
        "fat":           [3,   0.5, 0.5, 5, 11,  1,   2,   4,   2],
    })


@pytest.fixture
def sample_weekly_plan():
    """A valid 7-day weekly plan dict."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meals = ["breakfast", "lunch", "dinner"]
    foods = [
        ["Oatmeal", "Grilled Chicken", "Brown Rice"],
        ["Boiled Eggs", "Tuna", "Quinoa Bowl"],
        ["Cucumber Salad", "Whole Wheat Pasta", "Steamed Broccoli"],
        ["Oatmeal", "Grilled Chicken", "Brown Rice"],
        ["Boiled Eggs", "Tuna", "Quinoa Bowl"],
        ["Cucumber Salad", "Whole Wheat Pasta", "Steamed Broccoli"],
        ["Oatmeal", "Grilled Chicken", "Brown Rice"],
    ]
    return {
        day: {meal: foods[i][j] for j, meal in enumerate(meals)}
        for i, day in enumerate(days)
    }
