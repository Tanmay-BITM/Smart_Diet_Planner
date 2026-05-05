import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from backend.utils.bmi import calculate_bmi


# ---------------------------------------------------------------------------
# Property 1: BMI calculation is mathematically correct
# Feature: smart-diet-planner, Property 1: BMI calculation is mathematically correct
# Validates: Requirements 2.1
# ---------------------------------------------------------------------------
@given(
    weight=st.floats(min_value=1.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    height=st.floats(min_value=1.0, max_value=300.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=100)
def test_bmi_calculation_is_correct(weight, height):
    """For any valid weight and height, BMI == round(weight / (height/100)**2, 2)."""
    bmi, _ = calculate_bmi(weight, height)
    expected = round(weight / (height / 100.0) ** 2, 2)
    assert bmi == expected


# ---------------------------------------------------------------------------
# Property 2: BMI category boundaries are correct
# Feature: smart-diet-planner, Property 2: BMI category boundaries are correct
# Validates: Requirements 2.2
# ---------------------------------------------------------------------------
@given(
    weight=st.floats(min_value=1.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    height=st.floats(min_value=1.0, max_value=300.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=100)
def test_bmi_category_matches_boundaries(weight, height):
    """For any valid weight/height, the returned category matches the threshold rules."""
    bmi, category = calculate_bmi(weight, height)
    if bmi < 18.5:
        assert category == "Underweight"
    elif bmi < 25.0:
        assert category == "Normal"
    elif bmi < 30.0:
        assert category == "Overweight"
    else:
        assert category == "Obese"


# ---------------------------------------------------------------------------
# Edge-case unit tests
# ---------------------------------------------------------------------------
def test_bmi_raises_on_zero_height():
    with pytest.raises(ValueError, match="height_cm"):
        calculate_bmi(70, 0)


def test_bmi_raises_on_negative_height():
    with pytest.raises(ValueError, match="height_cm"):
        calculate_bmi(70, -5)


def test_bmi_raises_on_zero_weight():
    with pytest.raises(ValueError, match="weight_kg"):
        calculate_bmi(0, 170)


def test_bmi_raises_on_negative_weight():
    with pytest.raises(ValueError, match="weight_kg"):
        calculate_bmi(-10, 170)


@pytest.mark.parametrize("weight,height,expected_bmi,expected_cat", [
    # BMI ~18.5 → Normal (just above underweight boundary)
    (56.0, 174.0, round(56.0 / (1.74 ** 2), 2), "Normal"),
    # BMI ~25.0 → Overweight (just above normal boundary)
    (68.0, 164.9, round(68.0 / (1.649 ** 2), 2), "Overweight"),
    # BMI ~30.0 → Obese (just above overweight boundary)
    (90.0, 173.0, round(90.0 / (1.73 ** 2), 2), "Obese"),
])
def test_bmi_boundary_values(weight, height, expected_bmi, expected_cat):
    bmi, cat = calculate_bmi(weight, height)
    assert bmi == expected_bmi
    assert cat == expected_cat
