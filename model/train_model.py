import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression

# =========================
# Helper function
# =========================
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# =========================
# Base Data
# =========================
raw_data = [
    # age, weight, height, smoker, label
    [25, 70, 1.75, 0, 1],
    [45, 85, 1.70, 1, 0],
    [30, 65, 1.68, 0, 1],
    [50, 95, 1.72, 1, 0],
    [22, 55, 1.60, 0, 1],
    [60, 100, 1.65, 1, 0],
    [28, 68, 1.80, 0, 1],
    [40, 90, 1.75, 1, 0],
    [32, 68, 1.72, 0, 1],   
    [35, 75, 1.80, 1, 1],   
    [38, 70, 1.75, 0, 1],   
    [42, 78, 1.78, 1, 1],   
    [45, 65, 1.68, 0, 1],   
    [50, 72, 1.73, 0, 1],   
    [55, 80, 1.82, 0, 1],   
    [60, 68, 1.70, 0, 1],   
]

# =========================
# Add more unhealthy cases
# =========================
extra_unhealthy = [
    [35, 110, 1.65, 1, 0],
    [50, 120, 1.70, 1, 0],
    [28, 95, 1.60, 1, 0],
    [45, 105, 1.68, 1, 0],
    [60, 115, 1.72, 1, 0],
    [25, 45, 1.75, 0, 0],   # underweight
    [30, 48, 1.80, 0, 0],
    [22, 40, 1.65, 0, 0],
    [55, 90, 1.60, 0, 0],
    [40, 100, 1.70, 0, 0],
]

# Combine all data
raw_data.extend(extra_unhealthy)

# =========================
# Prepare X and y
# =========================
X_data = []
y = []

for row in raw_data:
    age, weight, height, smoker, label = row
    bmi = calculate_bmi(weight, height)

    X_data.append({
        "age": age,
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "smoker": smoker
    })
    y.append(label)

X = pd.DataFrame(X_data)
y = np.array(y)

# =========================
# Train model
# =========================
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# =========================
# Test prediction
# =========================
test_sample = pd.DataFrame([{
    "age": 35,
    "weight": 95,
    "height": 1.70,
    "bmi": calculate_bmi(95, 1.70),
    "smoker": 1
}])

prediction = model.predict(test_sample)

print("Test Prediction (1=Healthy, 0=Unhealthy):", prediction[0])

# Optional: probability
probability = model.predict_proba(test_sample)
print("Prediction probabilities [unhealthy, healthy]:", probability[0])

# =========================
# Save model
# =========================
with open("model/health_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as health_model.pkl")