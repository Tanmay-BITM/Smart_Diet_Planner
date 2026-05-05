import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

from backend.config import N_CLUSTERS
from backend.utils.preprocessing import FEATURE_COLUMNS


def train_kmeans(data: pd.DataFrame):
    """
    Fit a KMeans model on the nutritional feature columns.

    The incoming DataFrame is expected to already be preprocessed
    (no nulls, no negatives).  We re-scale internally so the raw
    (un-normalised) DataFrame can also be passed in.

    Returns
    -------
    model : fitted KMeans instance
    data  : original DataFrame with an added 'cluster' column
    """
    features = data[FEATURE_COLUMNS].copy()

    # Normalise in case raw values were passed
    scaler = MinMaxScaler()
    X = scaler.fit_transform(features)

    model = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    data = data.copy()
    data["cluster"] = model.fit_predict(X)

    return model, data
