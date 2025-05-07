   
# Ai Employee Success Viability Predictive Assesment Tool 

---

##### _Description: This project is an end-to-end machine learning application built using Python, TensorFlow, SQLAlchemy, Flask-RESTx, and supporting tools. It simulates the prediction of employee success scores based on synthetic data and demonstrates core ML engineering principles such as data generation, model training, evaluation, retraining, and versioning._ 
   
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

<img width="1502" alt="Screenshot 2025-05-07 at 5 31 07 PM" src="https://github.com/user-attachments/assets/a21ccc96-212c-4d8b-8539-0a274bcb2268" />


# 🧪 Getting Started

## Prerequisites

- Python 3.8+ (If you don't have python installed or an older version and if you neveer used anaconda or miniconda I sugguest you use miniconda)
- PostgreSQL (or SQLite for testing)
- MinIO for model versioning (Will add AWS S3 endpoint in next version you can get a free version with a credit card) 
- Docker desktop (Or you can just have docker CLI installed) 

## Enviornemnt setup 
Bash >>
```
pip install -r requirements.txt
```

## Create an `.env` file in the project root
```
DATABASE_URL=postgresql://user:pass@localhost/db
AWS_KEY=your_key
AWS_SECRET=your_secret
AWS_ENDPOINT=http://localhost:9000
```

## Build the docker container and run the app 

#### Build and run the container 
```
docker-compose down -v && docker-compose up --build
```

### _The terminal wlll state the app is running, then you can go to docker desktop and see the 3 containers automatically created for you (below)._
<img width="1500" alt="Screenshot 2025-05-07 at 5 25 18 PM" src="https://github.com/user-attachments/assets/a09f233f-0019-44c7-aa80-62360bdb1377" />

## There will be 3 URLS you can access 
Flask API ``http://localhost:5000`` # Base route takes you to the swagger 
MiniO UI ``http://localhost:9001`` # MiniO alternative S3 free storage (local) 
PostGres ``Ports - 5432:5432`` # This isn't a link instead just a container for Postgres 

## (Optional using DBeaver)
Download DBeaver and select create new database. Just use the default settings and the only thing you will need is the username and password you used to create the .env file. The host option and port stay the same. Once the docker is built this should generate the employee table and other tables in your local database. 
<img width="229" alt="Screenshot 2025-05-07 at 5 29 03 PM" src="https://github.com/user-attachments/assets/a6c2d22e-51d8-4a22-a62e-e9556b8a9ff9" />


## 📊 Clustering (Alternative Scoring)

The app also supports an optional success scoring method using **KMeans clustering**. This unsupervised approach groups employees based on selected features, useful for exploratory analysis or pre-model evaluation.

### Features used for clustering:
- `years_experience`
- `different_industries_worked_in`
- `has_leadership_experience`
- `largest_company_size_worked_at`

---

## 💡 Future Enhancements

- 🔍 Integrate model explainability tools (e.g., SHAP)
- 📈 Add a dashboard UI for visualizing predictions
- 🔁 Implement real-time inference using Kafka or Celery
- ✅ Automate model retraining via CI/CD pipelines

---

## 🛠️ Tech Stack

| Component     | Technology             |
|---------------|------------------------|
| Web API       | Flask + Flask-RESTx    |
| ORM / Database| SQLAlchemy + PostgreSQL|
| ML / Modeling | TensorFlow + Keras     |
| Preprocessing | scikit-learn           |
| Storage       | AWS S3 / MinIO         |
| Dev Tools     | Faker, Pandas, Boto3, docker  |

### More updates and documentation coming soon. 
