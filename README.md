# Health Predictor API

A simple AI-powered API that predicts whether a person is **healthy or unhealthy** based on basic health metrics.

Built with **FastAPI + Scikit-learn**, this project demonstrates how to train a machine learning model and deploy it as an API.

---

## Features

- Predict health status (healthy / unhealthy)
- Uses Logistic Regression model
- RESTful API built with FastAPI
- Input validation using Pydantic
- JSON-based responses
- Versioned model endpoint

---

## Tech Stack

- Python
- FastAPI
- Scikit-learn
- Pandas
- NumPy

---

## Model Details

The model uses the following features:

- Age
- Weight (kg)
- Height (m)
- BMI
- Smoking status (0 = non-smoker, 1 = smoker)

Algorithm:
- Logistic Regression

---

---

## Installation

### 1. Clone repo


git clone https://github.com/phatTchung9999/health-predictor-api.git

cd health-predictor-api


### 2. Create virtual environment

**Windows**

python -m venv .venv
.venv\Scripts\activate


**Mac/Linux**

python3 -m venv .venv
source .venv/bin/activate


### 3. Install dependencies


pip install -r requirements.txt


---

## Run Server


uvicorn app:app --reload


Open:

http://127.0.0.1:8000


---

## API Endpoints

### GET `/`


{
"message": "Health Prediction API"
}


---

### GET `/health`


{
"status": "OK",
"version": "1.0.0",
"model": true
}


---

### POST `/predict`

#### Request


{
"age": 25,
"weight": 70,
"height": 1.75,
"smoker": false
}


#### Response


{
"result": "healthy"
}


---

## Notes

- BMI is automatically calculated inside the backend
- You do NOT need to send BMI manually
- Input is validated using Pydantic

---

## API Docs

Swagger:

http://127.0.0.1:8000/docs


ReDoc:

http://127.0.0.1:8000/redoc

---


