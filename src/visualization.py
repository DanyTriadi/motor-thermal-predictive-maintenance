import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "measures_v2.csv")


data = pd.read_csv(DATA_PATH)

# REGRESSION DATA PREPARATION
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


# 1) REAL vs PREDICTED
plt.figure(figsize=(7,6))
plt.scatter(y_test[:3000], y_pred[:3000], alpha=0.6, color="red")
plt.xlabel("Real Stator Winding Temperature (°C)")
plt.ylabel("Predicted Temperature (°C)")
plt.title("Real vs Predicted Temperature")
plt.grid(True)
plt.tight_layout()
plt.show()

# 2) RESIDUAL ERROR DISTRIBUTION
errors = y_test - y_pred

plt.figure(figsize=(7,6))
plt.hist(errors, bins=80, color="steelblue", edgecolor="black")
plt.xlabel("Prediction Error (°C)")
plt.ylabel("Frequency")
plt.title("Residual Error Distribution")
plt.grid(True)
plt.tight_layout()
plt.show()


# 3) RISK LEVEL DISTRIBUTION

data["risk_level"] = pd.cut(
    data["stator_winding"],
    bins=[-np.inf, 90, 110, np.inf],
    labels=["NORMAL", "WARNING", "CRITICAL"]
)

risk_counts = data["risk_level"].value_counts().sort_index()

colors = {
    "NORMAL": "green",
    "WARNING": "orange",
    "CRITICAL": "red"
}

bar_colors = [colors[level] for level in risk_counts.index]

plt.figure(figsize=(7,6))
plt.bar(risk_counts.index, risk_counts.values, color=bar_colors)
plt.xlabel("Risk Level")
plt.ylabel("Count")
plt.title("Risk Level Distribution")
plt.tight_layout()
plt.show()