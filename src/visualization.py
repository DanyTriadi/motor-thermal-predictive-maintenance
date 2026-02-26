import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("../data/measures_v2.csv")

y = data["stator_winding"]
X = data.drop(columns=["stator_winding", "profile_id"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

plt.figure()
plt.scatter(y_test[:2000], y_pred[:2000], alpha=0.6)
plt.xlabel("Actual Temperature")
plt.ylabel("Predicted Temperature")
plt.title("Actual vs Predicted Temperature")
plt.show()

errors = y_test - y_pred
plt.figure()
plt.hist(errors, bins=60)
plt.title("Prediction Error Distribution")
plt.xlabel("Error (°C)")
plt.ylabel("Frequency")
plt.show()

coeff = model.coef_
features = X.columns

plt.figure()
plt.barh(features, coeff)
plt.title("Feature Importance (Linear Regression)")
plt.xlabel("Coefficient Value")
plt.show()

plt.figure()
plt.plot(y_test.values[:500], label="Actual")
plt.plot(y_pred[:500], label="Predicted")
plt.title("Thermal Prediction Signal")
plt.xlabel("Sample Index")
plt.ylabel("Temperature")
plt.legend()
plt.show()