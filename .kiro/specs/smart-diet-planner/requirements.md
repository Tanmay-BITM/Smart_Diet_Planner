# Requirements Document

## Introduction

The Smart Weekly Diet Planner is a full-stack machine learning web application that generates a personalized 7-day meal plan based on user health data and fitness goals. The system uses K-Means Clustering to group food items by nutritional profile and an ID3 Decision Tree to classify the appropriate diet type for a given user. A Streamlit frontend collects user input and displays results; a Python backend handles all computation and ML logic.

## Glossary

- **System**: The Smart Weekly Diet Planner application as a whole
- **Frontend**: The Streamlit-based user interface
- **Backend**: The Python processing layer including ML models and diet generation logic
- **BMI**: Body Mass Index, calculated as weight (kg) / height (m)²
- **Diet_Type**: A classification of the recommended eating strategy (e.g., weight loss, weight gain, maintenance)
- **Cluster**: A group of food items with similar nutritional profiles produced by K-Means
- **Weekly_Plan**: A structured 7-day meal schedule containing breakfast, lunch, and dinner entries
- **Decision_Tree**: The ID3-based classifier that maps user health attributes to a Diet_Type
- **KMeans_Model**: The unsupervised clustering model that groups food items
- **Preprocessor**: The component responsible for loading and cleaning the food dataset
- **BMI_Calculator**: The component that computes BMI and its category from weight and height
- **Diet_Generator**: The component that selects food items from a cluster and assembles the Weekly_Plan
- **Diet_Service**: The orchestration layer that coordinates BMI_Calculator, Decision_Tree, and Diet_Generator

---

## Requirements

### Requirement 1: User Input Collection

**User Story:** As a user, I want to enter my personal health details so that the system can generate a diet plan tailored to me.

#### Acceptance Criteria

1. THE Frontend SHALL provide input fields for age (integer, 1–120), height (float, cm), weight (float, kg), activity level (sedentary, lightly active, moderately active, very active), and fitness goal (weight loss, weight gain, maintenance).
2. WHEN a user submits the form with all fields filled, THE Frontend SHALL send the collected data to the Backend for processing.
3. IF a required field is missing or contains an out-of-range value, THEN THE Frontend SHALL display a descriptive validation error and prevent form submission.

---

### Requirement 2: BMI Calculation

**User Story:** As a user, I want to see my BMI and its category so that I understand my current health status.

#### Acceptance Criteria

1. WHEN weight and height are provided, THE BMI_Calculator SHALL compute BMI as weight (kg) divided by height (m) squared, rounded to two decimal places.
2. THE BMI_Calculator SHALL classify the computed BMI into one of four categories: Underweight (< 18.5), Normal (18.5–24.9), Overweight (25–29.9), Obese (≥ 30).
3. IF height is zero or negative, THEN THE BMI_Calculator SHALL return an error indicating invalid height.

---

### Requirement 3: Food Dataset Loading and Preprocessing

**User Story:** As a developer, I want the system to load and clean the food dataset so that only valid nutritional data is used for clustering and meal generation.

#### Acceptance Criteria

1. WHEN the application starts, THE Preprocessor SHALL load the food dataset from the configured CSV file path.
2. THE Preprocessor SHALL retain only rows where calories, protein, carbohydrates, and fat values are non-negative numbers.
3. IF the CSV file is missing or unreadable, THEN THE Preprocessor SHALL raise a descriptive error and halt startup.
4. THE Preprocessor SHALL normalize the nutritional feature columns (calories, protein, carbohydrates, fat) to a common scale before passing data to the KMeans_Model.

---

### Requirement 4: K-Means Food Clustering

**User Story:** As a developer, I want food items grouped by nutritional profile so that the diet generator can select appropriate foods for each diet type.

#### Acceptance Criteria

1. WHEN the preprocessed dataset is provided, THE KMeans_Model SHALL cluster food items into at least three distinct groups representing low-calorie, high-protein, and balanced nutritional profiles.
2. THE KMeans_Model SHALL assign a cluster label to every food item in the dataset.
3. THE KMeans_Model SHALL be trained once at application startup and reused for all subsequent requests.
4. WHEN the number of food items in the dataset is fewer than the number of requested clusters, THE KMeans_Model SHALL raise a descriptive error.

---

### Requirement 5: Diet Type Classification (ID3 Decision Tree)

**User Story:** As a user, I want the system to determine the most suitable diet type for me based on my health profile so that the meal plan matches my goals.

#### Acceptance Criteria

1. WHEN BMI, activity level, and fitness goal are provided, THE Decision_Tree SHALL classify the user into exactly one Diet_Type from the set {weight_loss, weight_gain, maintenance}.
2. THE Decision_Tree SHALL use BMI category, activity level, and fitness goal as input features.
3. IF an unrecognized activity level or fitness goal value is provided, THEN THE Decision_Tree SHALL return an error indicating the invalid input.

---

### Requirement 6: Weekly Diet Plan Generation

**User Story:** As a user, I want a structured 7-day meal plan so that I know exactly what to eat each day of the week.

#### Acceptance Criteria

1. WHEN a Diet_Type is determined, THE Diet_Generator SHALL select food items exclusively from the cluster that corresponds to that Diet_Type.
2. THE Diet_Generator SHALL produce a Weekly_Plan containing exactly 7 days, each with breakfast, lunch, and dinner entries.
3. THE Diet_Generator SHALL ensure no single food item appears in the same meal slot (breakfast, lunch, or dinner) on consecutive days.
4. IF the cluster corresponding to the Diet_Type contains fewer food items than required to fill the Weekly_Plan without repetition within a day, THEN THE Diet_Generator SHALL allow cross-day repetition but SHALL NOT repeat the same food item within a single day.

---

### Requirement 7: End-to-End API Endpoint

**User Story:** As a developer, I want a single API endpoint that accepts user health data and returns the full diet plan response so that the frontend can retrieve all results in one call.

#### Acceptance Criteria

1. THE Backend SHALL expose a POST endpoint at `/generate-diet` that accepts age, height, weight, activity level, and fitness goal as parameters.
2. WHEN a valid request is received, THE Backend SHALL return a JSON response containing BMI value, BMI category, Diet_Type, and the Weekly_Plan.
3. IF any input parameter fails validation, THEN THE Backend SHALL return an HTTP 422 response with a descriptive error message.
4. THE Backend SHALL process each request independently without retaining user data between requests.

---

### Requirement 8: Results Display

**User Story:** As a user, I want to see my BMI, recommended diet type, and weekly meal plan displayed clearly so that I can follow the plan easily.

#### Acceptance Criteria

1. WHEN the Backend returns a successful response, THE Frontend SHALL display the BMI value and its category.
2. WHEN the Backend returns a successful response, THE Frontend SHALL display the recommended Diet_Type.
3. WHEN the Backend returns a successful response, THE Frontend SHALL render the Weekly_Plan as a table with days as rows and meal slots (breakfast, lunch, dinner) as columns.
4. IF the Backend returns an error response, THEN THE Frontend SHALL display a user-friendly error message without exposing internal stack traces.

---

### Requirement 9: Data Serialization

**User Story:** As a developer, I want the Weekly_Plan to be consistently serializable to and from JSON so that the API contract is stable and testable.

#### Acceptance Criteria

1. THE Backend SHALL serialize the Weekly_Plan to a JSON-compatible dictionary before returning it in the API response.
2. FOR ALL valid Weekly_Plan objects, serializing then deserializing SHALL produce an equivalent Weekly_Plan (round-trip property).
