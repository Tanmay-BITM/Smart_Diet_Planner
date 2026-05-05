def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    """
    Compute BMI and return (bmi_value, bmi_category).

    BMI = weight_kg / (height_m ** 2), rounded to 2 decimal places.
    Categories:
        Underweight : BMI < 18.5
        Normal      : 18.5 <= BMI < 25
        Overweight  : 25 <= BMI < 30
        Obese       : BMI >= 30

    Raises ValueError if height_cm <= 0 or weight_kg <= 0.
    """
    if height_cm <= 0:
        raise ValueError(f"height_cm must be positive, got {height_cm}")
    if weight_kg <= 0:
        raise ValueError(f"weight_kg must be positive, got {weight_kg}")

    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25.0:
        category = "Normal"
    elif bmi < 30.0:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi, category
