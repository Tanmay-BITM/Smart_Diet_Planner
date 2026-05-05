import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "food_dataset.csv")
N_CLUSTERS = 3

CLUSTER_LABELS = {
    0: "Low Calorie",
    1: "High Protein",
    2: "Balanced",
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MEALS = ["Breakfast", "Lunch", "Dinner"]
