from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.config import DATA_PATH
from backend.utils.preprocessing import load_and_preprocess
from backend.models.kmeans_model import train_kmeans
from backend.services.diet_services import generate_plan

app = FastAPI(title="Smart Diet Planner API")

# ── Startup: load data and train model once ──────────────────────────────────
_raw_data = load_and_preprocess(DATA_PATH)
_model, _food_data = train_kmeans(_raw_data)


# ── Request schema ────────────────────────────────────────────────────────────
class DietRequest(BaseModel):
    age: int = Field(..., gt=0, le=120)
    height: float = Field(..., gt=0, description="Height in cm")
    weight: float = Field(..., gt=0, description="Weight in kg")
    activity_level: str = Field(default="Moderate")
    goal: str = Field(..., description="Weight Loss | Weight Gain | Maintenance")


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "Smart Diet Planner API is running"}


@app.post("/generate-diet")
def generate_diet(req: DietRequest):
    try:
        bmi_value, bmi_category, diet_label, weekly_plan = generate_plan(
            weight=req.weight,
            height=req.height,
            goal=req.goal,
            food_data=_food_data,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return {
        "bmi": bmi_value,
        "bmi_category": bmi_category,
        "diet_type": diet_label,
        "weekly_plan": weekly_plan,
    }
