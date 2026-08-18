import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -------------------------------
# Generate Dataset
# -------------------------------

np.random.seed(42)

rows = 3000

data = []

activities = [
    "Walking",
    "Running",
    "Standing",
    "Falling",
    "Struggling"
]

for _ in range(rows):

    activity = np.random.choice(activities)

    if activity == "Walking":
        accel = np.random.uniform(1.5,3.5)
        gyro = np.random.uniform(0.5,2.0)

    elif activity == "Running":
        accel = np.random.uniform(4.0,8.0)
        gyro = np.random.uniform(2.5,5.5)

    elif activity == "Standing":
        accel = np.random.uniform(0.0,1.0)
        gyro = np.random.uniform(0.0,0.8)

    elif activity == "Falling":
        accel = np.random.uniform(8.0,12.0)
        gyro = np.random.uniform(4.5,8.0)

    else:  # Struggling
        accel = np.random.uniform(5.0,10.0)
        gyro = np.random.uniform(3.0,7.0)

    data.append([accel, gyro, activity])

df = pd.DataFrame(
    data,
    columns=[
        "accelerometer",
        "gyroscope",
        "activity"
    ]
)

# Save dataset
df.to_csv("activity_dataset.csv", index=False)

print(df.head())

# -------------------------------
# Split Data
# -------------------------------

X = df[["accelerometer", "gyroscope"]]
y = df["activity"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -------------------------------
# Train Model
# -------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------------
# Evaluation
# -------------------------------

pred = model.predict(X_test)

print("\nAccuracy")

print(accuracy_score(y_test, pred))

print("\nClassification Report\n")

print(classification_report(y_test, pred))

# -------------------------------
# Save Model
# -------------------------------

joblib.dump(model, "activity_model.pkl")

print("\nModel Saved Successfully")