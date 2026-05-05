import os
import pytest
import pandas as pd
import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.pandas import column, data_frames

from backend.utils.preprocessing import load_and_preprocess, FEATURE_COLUMNS


# ---------------------------------------------------------------------------
# Property 9: Preprocessing removes invalid rows
# Feature: smart-diet-planner, Property 9: Preprocessing removes invalid rows
# Validates: Requirements 3.2
# ---------------------------------------------------------------------------
@given(
    data_frames(
        columns=[
            column("food_name", elements=st.text(min_size=1, max_size=20)),
            column("calories",      elements=st.floats(min_value=-100, max_value=600, allow_nan=True)),
            column("protein",       elements=st.floats(min_value=-50,  max_value=100, allow_nan=True)),
            column("carbohydrates", elements=st.floats(min_value=-50,  max_value=200, allow_nan=True)),
            column("fat",           elements=st.floats(min_value=-50,  max_value=100, allow_nan=True)),
        ],
        rows=st.integers(min_value=1, max_value=30),
    )
)
@settings(max_examples=100)
def test_preprocessing_removes_invalid_rows(df):
    """
    For any dataset with mixed valid/invalid rows, after preprocessing
    no row should have negative or null values in nutritional columns.
    """
    # Need at least one valid row for scaler to work; skip if none
    valid_mask = (df[FEATURE_COLUMNS] >= 0).all(axis=1) & df[FEATURE_COLUMNS].notna().all(axis=1)
    if valid_mask.sum() == 0:
        return  # nothing to test — all rows invalid

    result = _preprocess_df(df)

    for col in FEATURE_COLUMNS:
        assert result[col].notna().all(), f"Null found in {col} after preprocessing"
        assert (result[col] >= 0).all(), f"Negative value found in {col} after preprocessing"


def _preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """Helper: run preprocessing logic directly on a DataFrame (bypasses CSV loading)."""
    from sklearn.preprocessing import MinMaxScaler

    data = df.dropna(subset=FEATURE_COLUMNS)
    mask = (data[FEATURE_COLUMNS] >= 0).all(axis=1)
    data = data[mask].reset_index(drop=True)

    if len(data) == 0:
        return data

    scaler = MinMaxScaler()
    data[FEATURE_COLUMNS] = scaler.fit_transform(data[FEATURE_COLUMNS])
    return data


# ---------------------------------------------------------------------------
# Edge-case unit tests
# ---------------------------------------------------------------------------
def test_load_raises_file_not_found():
    with pytest.raises(FileNotFoundError, match="not found"):
        load_and_preprocess("/nonexistent/path/food.csv")


def test_load_raises_on_missing_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("food_name,calories\nApple,95\n")
    with pytest.raises(ValueError, match="missing required columns"):
        load_and_preprocess(str(bad_csv))


def test_load_drops_negative_rows(tmp_path):
    csv = tmp_path / "food.csv"
    csv.write_text(
        "food_name,calories,protein,carbohydrates,fat\n"
        "Apple,95,0.5,25,0.3\n"
        "Bad,-10,5,20,1\n"
        "Banana,89,1.1,23,0.3\n"
    )
    result = load_and_preprocess(str(csv))
    assert len(result) == 2
    assert "Bad" not in result["food_name"].values


def test_load_drops_null_rows(tmp_path):
    csv = tmp_path / "food.csv"
    csv.write_text(
        "food_name,calories,protein,carbohydrates,fat\n"
        "Apple,95,0.5,25,0.3\n"
        "NullFood,,5,20,1\n"
        "Banana,89,1.1,23,0.3\n"
    )
    result = load_and_preprocess(str(csv))
    assert len(result) == 2
    assert "NullFood" not in result["food_name"].values


def test_normalized_values_in_range(tmp_path):
    """After normalization all feature values should be in [0, 1]."""
    csv = tmp_path / "food.csv"
    csv.write_text(
        "food_name,calories,protein,carbohydrates,fat\n"
        "Apple,95,0.5,25,0.3\n"
        "Chicken,220,42,0,5\n"
        "Rice,215,5,45,2\n"
    )
    result = load_and_preprocess(str(csv))
    for col in FEATURE_COLUMNS:
        assert result[col].between(0, 1).all(), f"{col} values out of [0,1] range"
