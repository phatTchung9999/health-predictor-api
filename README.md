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

## Endpoint
- GET /
- GET /health
- POST /predict
  
---
## Example

Example Request
{ "age":25, "weight":70, "height":1.75, "smoker":false }

Example Response
{ "result": "healthy" }

---


