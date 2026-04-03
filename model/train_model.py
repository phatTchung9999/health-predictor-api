import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression

# Features:
# [age, weight, height, bmi, isSmoker]
X = np.array([
    [25, 70, 1.75, 22.9, 0],
    [45, 85, 1.70, 29.4, 1],
    [30, 65, 1.68, 23.0, 0],
    [50, 95, 1.72, 32.1, 1],
    [22, 55, 1.60, 21.5, 0],
    [60, 100, 1.65, 36.7, 1],
    [28, 68, 1.80, 21.0, 0],
    [40, 90, 1.75, 29.4, 1]
])

# Labels:
# 1 = healthy, 0 = unhealthy
y = np.array([1, 0, 1, 0, 1, 0, 1, 0])

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
with open("health_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as health_model.pkl")