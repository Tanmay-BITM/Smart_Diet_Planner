import pandas as pd
from sklearn.preprocessing import MinMaxScaler

REQUIRED_COLUMNS = {"food_name", "calories", "protein", "carbohydrates", "fat"}
FEATURE_COLUMNS = ["calories", "protein", "carbohydrates", "fat"]


def load_and_preprocess(csv_path: str) -> pd.DataFrame:
    """
    Load the food dataset CSV, clean it, and normalize nutritional features.

    Steps:
      1. Load CSV from csv_path.
      2. Validate required columns exist.
      3. Drop rows where any nutritional value is null or negative.
      4. Normalize FEATURE_COLUMNS to [0, 1] using MinMaxScaler.

    Returns a cleaned DataFrame with original columns plus
    scaled versions stored in 'scaled_features' (numpy array per row).

    Raises:
        FileNotFoundError: if csv_path does not exist.
        ValueError: if any required column is missing.
    """
    try:
        data = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Food dataset not found at: {csv_path}")

    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    # Drop rows with null values in nutritional columns
    data = data.dropna(subset=FEATURE_COLUMNS)

    # Drop rows with any negative nutritional value
    mask = (data[FEATURE_COLUMNS] >= 0).all(axis=1)
    data = data[mask].reset_index(drop=True)

    # Normalize features
    scaler = MinMaxScaler()
    data[FEATURE_COLUMNS] = scaler.fit_transform(data[FEATURE_COLUMNS])

    return data
