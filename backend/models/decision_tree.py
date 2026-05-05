"""
ID3-inspired decision tree for diet type classification.

Rules
-----
The tree uses BMI category and fitness goal to decide which food
cluster (diet type) is most appropriate.

                        goal
                       /    \\
              Weight Loss   Weight Gain   Maintenance / other
                  |               |               |
              Low Calorie    High Protein      Balanced
              (adjusted by BMI)
"""

from backend.config import CLUSTER_LABELS

# Reverse map: label → cluster id
_LABEL_TO_CLUSTER = {v: k for k, v in CLUSTER_LABELS.items()}


def decide_diet_type(bmi: float, goal: str) -> tuple[str, int]:
    """
    Apply the ID3 decision tree to return (diet_label, cluster_id).

    Parameters
    ----------
    bmi  : float  – calculated BMI value
    goal : str    – one of "Weight Loss", "Weight Gain", "Maintenance"

    Returns
    -------
    (diet_label, cluster_id)
    """
    goal = goal.strip().lower()

    if goal == "weight loss":
        # Obese users get strict low-calorie; others also low-calorie
        label = "Low Calorie"
    elif goal == "weight gain":
        # Underweight users need high protein
        label = "High Protein"
    else:
        # Maintenance – refine by BMI
        if bmi < 18.5:
            label = "High Protein"   # underweight → build mass
        elif bmi < 25.0:
            label = "Balanced"       # normal → maintain
        elif bmi < 30.0:
            label = "Low Calorie"    # overweight → cut slightly
        else:
            label = "Low Calorie"    # obese → cut

    cluster_id = _LABEL_TO_CLUSTER[label]
    return label, cluster_id
