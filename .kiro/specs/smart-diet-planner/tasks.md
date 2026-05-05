# Implementation Plan: Smart Weekly Diet Planner

## Overview

Implement the Smart Weekly Diet Planner incrementally, starting with the data layer and ML models, then the service/API layer, and finally the Streamlit frontend. Each step builds on the previous and is validated by tests before moving on.

## Tasks

- [x] 1. Set up project foundation
  - Create `requirements.txt` with: fastapi, uvicorn, streamlit, pandas, numpy, scikit-learn, hypothesis, pytest, httpx, requests
  - Create `backend/config.py` defining `DATA_PATH` pointing to `backend/data/food_dataset.csv` and `N_CLUSTERS = 3`
  - Create `backend/data/food_dataset.csv` with at least 30 food items and columns: `food_name`, `calories`, `protein`, `carbohydrates`, `fat`
  - Create `backend/tests/__init__.py` and `backend/tests/conftest.py` with shared fixtures (sample DataFrame, sample weekly plan)
  - _Requirements: 3.1, 4.1_

- [x] 2. Implement BMI Calculator
  - [x] 2.1 Implement `calculate_bmi(weight_kg, height_cm)` in `backend/utils/bmi.py`
    - Returns `(bmi_value: float, bmi_category: str)` tuple
    - Raises `ValueError` for height ≤ 0 or weight ≤ 0
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 2.2 Write property tests for BMI Calculator
    - **Property 1: BMI calculation is mathematically correct**
    - **Property 2: BMI category boundaries are correct**
    - **Validates: Requirements 2.1, 2.2**
    - Include edge-case unit tests: height=0, weight=0, BMI boundary values 18.5, 25.0, 30.0

- [-] 3. Implement Preprocessor
  - [x] 3.1 Implement `load_and_preprocess(csv_path)` in `backend/utils/preprocessing.py`
    - Loads CSV, drops rows with null or negative nutritional values
    - Applies MinMaxScaler to `calories`, `protein`, `carbohydrates`, `fat` columns
    - Raises `FileNotFoundError` if path missing, `ValueError` if required columns absent
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [ ] 3.2 Write property tests for Preprocessor
    - **Property 9: Preprocessing removes invalid rows**
    - **Validates: Requirements 3.2**
    - Include edge-case unit tests: missing file, missing columns, all-null dataset

- [ ] 4. Implement KMeans Model
  - [ ] 4.1 Implement `train_kmeans(data, n_clusters)` and `get_cluster_for_diet_type(diet_type, model, data)` in `backend/models/kmeans_model.py`
    - Fits KMeans on normalized features, assigns `cluster` column to DataFrame
    - Maps diet types to clusters by inspecting centroids (lowest calorie → weight_loss, highest protein → weight_gain, else → maintenance)
    - Raises `ValueError` if `len(data) < n_clusters`
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ] 4.2 Write property test for KMeans labeling
    - **Property 3: Every food item receives a cluster label**
    - **Validates: Requirements 4.2**
    - Include edge-case unit test: dataset with fewer rows than n_clusters

- [ ] 5. Implement Decision Tree Classifier
  - [ ] 5.1 Implement `classify_diet_type(bmi_category, activity_level, goal)` in `backend/models/decision_tree.py`
    - Rule-based ID3 tree using nested dict `DIET_RULES`
    - Returns one of: `weight_loss`, `weight_gain`, `maintenance`
    - Raises `ValueError` for any unrecognized input value
    - _Requirements: 5.1, 5.2, 5.3_

  - [ ] 5.2 Write property test for Decision Tree coverage
    - **Property 8: Decision Tree covers all valid input combinations**
    - **Validates: Requirements 5.1**
    - Include edge-case unit tests: invalid activity_level, invalid goal, invalid bmi_category

- [ ] 6. Checkpoint — Ensure all backend utility tests pass
  - Run `pytest backend/tests/ -v` and confirm all tests pass before proceeding.

- [ ] 7. Implement Diet Generator
  - [ ] 7.1 Implement `generate_weekly_plan(cluster_data, seed)` in `backend/utils/diet_generator.py`
    - Produces a dict with 7 day keys, each containing breakfast/lunch/dinner
    - No food item repeats within the same day
    - Raises `ValueError` if cluster_data has fewer than 3 unique food items
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

  - [ ] 7.2 Write property tests for Diet Generator
    - **Property 4: Weekly plan structure invariant**
    - **Property 5: No same-day food repetition**
    - **Property 6: Diet Generator only uses foods from the correct cluster**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**
    - Include edge-case unit test: cluster with exactly 3 food items

- [ ] 8. Implement Diet Service
  - [ ] 8.1 Implement `generate_plan(age, weight_kg, height_cm, activity_level, goal, data)` in `backend/services/diet_services.py`
    - Orchestrates BMI_Calculator → Decision_Tree → cluster selection → Diet_Generator
    - Returns dict with keys: `bmi`, `bmi_category`, `diet_type`, `weekly_plan`
    - _Requirements: 7.2_

  - [ ] 8.2 Write unit tests for Diet Service
    - Test that the returned dict contains all required keys
    - Test that invalid inputs propagate errors correctly
    - _Requirements: 7.2, 7.3_

- [ ] 9. Implement FastAPI Backend
  - [ ] 9.1 Complete `backend/main.py`
    - Load dataset and train KMeans at startup using `lifespan` context
    - Wire `POST /generate-diet` to `Diet_Service.generate_plan`
    - Return HTTP 422 on `ValueError`, HTTP 500 on unexpected errors
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 9.2 Write property test for Weekly Plan serialization round-trip
    - **Property 7: Weekly plan serialization round-trip**
    - **Validates: Requirements 9.2**

  - [ ] 9.3 Write API endpoint unit tests using `httpx.AsyncClient`
    - Test valid request returns 200 with correct response keys
    - Test missing parameter returns 422
    - _Requirements: 7.1, 7.2, 7.3_

- [ ] 10. Checkpoint — Ensure all backend tests pass
  - Run `pytest backend/tests/ -v` and confirm all tests pass before proceeding.

- [ ] 11. Implement Streamlit Frontend
  - [ ] 11.1 Implement `frontend/app.py`
    - Input form: age, height, weight, activity_level (selectbox), goal (selectbox)
    - On submit: POST to `http://localhost:8000/generate-diet`
    - Display BMI metric, diet type label, weekly plan as `st.dataframe`
    - On error response or connection failure: `st.error()` with user-friendly message
    - _Requirements: 1.1, 1.2, 1.3, 8.1, 8.2, 8.3, 8.4_

- [ ] 12. Final Checkpoint — Ensure all tests pass
  - Run `pytest backend/tests/ -v` and confirm all tests pass.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Property tests use Hypothesis with `settings(max_examples=100)`
- Tag format in each test: `# Feature: smart-diet-planner, Property N: <property_text>`
- To run the app: start the backend with `uvicorn backend.main:app --reload` then run `streamlit run frontend/app.py`
