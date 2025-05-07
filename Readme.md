 
# Ai Employee Success Viability Predictive Assesment Tool 

#
---

##### _Description: This project is an end-to-end machine learning application built using Python, TensorFlow, SQLAlchemy, Flask-RESTx, and supporting tools. It simulates the prediction of employee success scores based on synthetic data and demonstrates core ML engineering principles such as data generation, model training, evaluation, retraining, and versioning._ 

#
#
   
---
   
##### My Socials (Patrick Florian):
[![LinkedIn](https://img.icons8.com/color/48/linkedin.png
)](https://www.linkedin.com) [![GitHub](https://img.icons8.com/color/48/github--v1.png
)](https://github.com) [![Website](https://img.icons8.com/color/48/geography.png
)](https://yourwebsite.com)

---

## 📌 Features

- ✅ Generates 5,000 fake employee records using `Faker`
- ✅ Trains a Keras neural network to predict a 1–10 success score
- ✅ Stores model runs, predictions, and hyperparameters in a SQL database
- ✅ Provides REST API for training, evaluating, and versioning models
- ✅ Uploads/downloads models to/from S3 or MinIO
- ✅ Demonstrates clustering with KMeans
- ✅ Includes model retraining and fine-tuning
- ✅ Swagger documentation with Flask-RESTx

---

## 🏗️ Project Architecture
AiEmployeeViabilityAssessmentTool/
```
├── app/
|   |-- validation         # implementing soon
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy ORM models
│   ├── data_generator.py  # Faker-based synthetic data
│   ├── ml_model.py        # TensorFlow model logic
│   ├── routes.py          # Flask API endpoints
├── docker-compose.yml     
├── Dockerfile
├── requirements.txt
├── config.py              # DB/config settings
```

---

## 🧠 Data Schema

### `Employee`

| Field                          | Type     | Description                                |
|-------------------------------|----------|--------------------------------------------|
| `id`                           | Integer  | Primary Key                                |
| `first_name`, `last_name`      | String   | Employee name                              |
| `dob`                          | DateTime | Date of birth                              |
| `role`                         | String   | Job title                                  |
| `years_experience`            | Integer  | Total career years                         |
| `years_with_current_company`  | Integer  | Tenure at current job                      |
| `has_leadership_experience`   | Boolean  | Has held leadership roles                  |
| `volunteer_experience`        | Boolean  | Volunteer background                       |
| `military_experience`         | Boolean  | Military background                        |
| `success_score` (derived)     | Integer  | Composite score (1-10)                     |

### `ModelRun`

| Field           | Type     | Description                              |
|----------------|----------|------------------------------------------|
| `id`           | Integer  | Run identifier                           |
| `run_date`     | DateTime | Timestamp of training                    |
| `model_type`   | String   | Architecture used (e.g., SequentialNN)   |
| `hyperparameters` | JSON  | Training parameters                      |
| `metrics`      | JSON     | Model performance (e.g., MAE, accuracy)  |
| `is_overfitted`| Boolean  | Overfitting flag                         |

### `ModelEvaluation`

| Field         | Type     | Description                              |
|--------------|----------|------------------------------------------|
| `employee_id`| Integer  | Employee foreign key                     |
| `model_run_id`| Integer | Model run foreign key                    |
| `success_score`| Integer| Predicted score                          |
| `confidence` | Float    | Confidence level                         |

---

## 🤖 Machine Learning Model

- **Model Type**: Keras Sequential Neural Network
- **Input**: Numeric and one-hot encoded categorical data
- **Layers**: Configurable (default: `[64, 32]`)
- **Output**: Single value (score 1–10)
- **Loss Function**: Mean Squared Error (MSE)
- **Metric**: Mean Absolute Error (MAE)
- **Scaler**: `StandardScaler` from `sklearn`

---

## 🔁 Model Versioning & Retraining

Models are saved as `.h5` files and uploaded to an S3 bucket. The system supports:

- ✅ Uploading new models
- ✅ Retraining with new parameters or fine-tuning
- ✅ Switching active models by version

---

## 🔌 API Endpoints

#### POST `/api/train`

| Field | Type | Description |
| ------ | ------ |  ------ |
| epochs | `integer` | Refers to one complete pass of the entire training dataset through the learning algorithm 

#### POST `/api/evaluate`

| Field | Type | Description |
| ------ | ------ |  ------ |
| employee_id | `integer` | Employee to evaluate
| features | `json` | Feature values

#### POST `/api/models/<version>`

| Field | Type | Description |
| ------ | ------ |  ------ |
| version | `string` | Model version (e.g., 20240501)

#### POST `/api/models/retrain`

| Field | Type | Description |
| ------ | ------ |  ------ |
| epochs | `integer` | Number of training epochs
| fine_tune | `boolean` | Use previous weights

