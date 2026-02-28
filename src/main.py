import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, classification_report, confusion_matrix

data = pd.read_csv("C:\\Users\\jazzp\\Documents\\ProjectAPK\\motor_failure_prediction\\data\\measures_v2.csv")

y = data["stator_winding"]
X = data.drop(columns=["stator_winding", "profile_id"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

reg_model = LinearRegression()
reg_model.fit(X_train_scaled, y_train)

y_pred = reg_model.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\nTHERMAL MODEL METRICS")
print("MAE :", mae)
print("RMSE:", rmse)
print("R2  :", r2)

coeff_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": reg_model.coef_
}).sort_values(by="Coefficient", ascending=False)

print("\nFEATURE IMPORTANCE")
print(coeff_df)

data["risk_level"] = pd.cut(
    data["stator_winding"],
    bins=[-np.inf, 90, 110, np.inf],
    labels=["NORMAL", "WARNING", "CRITICAL"]
)

y_cls = data["risk_level"]
X_cls = data.drop(columns=["stator_winding", "profile_id", "risk_level"])

Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    X_cls, y_cls, test_size=0.2, random_state=42, stratify=y_cls
)

scaler_cls = StandardScaler()
Xc_train_scaled = scaler_cls.fit_transform(Xc_train)
Xc_test_scaled = scaler_cls.transform(Xc_test)

clf = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    n_jobs=-1
)

clf.fit(Xc_train_scaled, yc_train)

yc_pred = clf.predict(Xc_test_scaled)

print("\nCONFUSION MATRIX")
print(confusion_matrix(yc_test, yc_pred))

print("\nCLASSIFICATION REPORT")
print(classification_report(yc_test, yc_pred))

rng = np.random.default_rng()

random_idx = rng.choice(len(Xc_test), size=5, replace=False)
sample_sensor = Xc_test.iloc[random_idx]

sample_scaled_cls = scaler_cls.transform(sample_sensor)
sample_scaled_reg = scaler.transform(sample_sensor)

risk_pred = clf.predict(sample_scaled_cls)
thermal_pred = reg_model.predict(sample_scaled_reg)

rng = np.random.default_rng()

random_idx = rng.choice(len(Xc_test), size=5, replace=False)
sample_sensor = Xc_test.iloc[random_idx]

sample_scaled_cls = scaler_cls.transform(sample_sensor)
sample_scaled_reg = scaler.transform(sample_sensor)

risk_pred = clf.predict(sample_scaled_cls)
thermal_pred = reg_model.predict(sample_scaled_reg)

print("\nREAL SYSTEM SIMULATION")

for i in range(5):
    action = (
        "CONTINUE OPERATION" if risk_pred[i] == "NORMAL"
        else "SCHEDULE MAINTENANCE" if risk_pred[i] == "WARNING"
        else "EMERGENCY SHUTDOWN"
    )

    print("\n======================================")
    print("INPUT SENSOR DATA →")

    row = sample_sensor.iloc[i]
    for col in sample_sensor.columns:
        print(f"{col:<15}: {row[col]:.3f}")

    print("\nPREDICTION OUTPUT →")
    print(f"Predicted Temp : {thermal_pred[i]:.2f} °C")
    print(f"Predicted Risk : {risk_pred[i]}")
    print(f"Action         : {action}")

print("\nSYSTEM STATUS: PREDICTIVE MAINTENANCE PIPELINE ACTIVE")