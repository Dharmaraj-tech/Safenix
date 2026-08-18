import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------------
# Create Synthetic Dataset
# -----------------------------------

np.random.seed(42)

rows = 3000

dataset = []

emotions = [
    "Normal",
    "Fear",
    "Panic",
    "Anxiety"
]

for i in range(rows):

    emotion = np.random.choice(emotions)

    if emotion == "Normal":
        mfcc1 = np.random.uniform(0.10,0.35)
        mfcc2 = np.random.uniform(0.20,0.45)
        pitch = np.random.uniform(100,160)

    elif emotion == "Fear":
        mfcc1 = np.random.uniform(0.55,0.75)
        mfcc2 = np.random.uniform(0.50,0.80)
        pitch = np.random.uniform(180,240)

    elif emotion == "Panic":
        mfcc1 = np.random.uniform(0.80,1.00)
        mfcc2 = np.random.uniform(0.80,1.00)
        pitch = np.random.uniform(250,320)

    else:
        mfcc1 = np.random.uniform(0.45,0.70)
        mfcc2 = np.random.uniform(0.45,0.70)
        pitch = np.random.uniform(170,220)

    dataset.append([
        mfcc1,
        mfcc2,
        pitch,
        emotion
    ])

df = pd.DataFrame(
    dataset,
    columns=[
        "mfcc1",
        "mfcc2",
        "pitch",
        "emotion"
    ]
)

df.to_csv("emotion_dataset.csv",index=False)

print(df.head())

# -----------------------------------
# Prepare Dataset
# -----------------------------------

X = df[[
    "mfcc1",
    "mfcc2",
    "pitch"
]]

y = df["emotion"]

X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------------
# Train SVM
# -----------------------------------

model=SVC(
    kernel="rbf",
    probability=True
)

model.fit(
    X_train,
    y_train
)

prediction=model.predict(X_test)

print("\nAccuracy")

print(
    accuracy_score(
        y_test,
        prediction
    )
)

print(
classification_report(
y_test,
prediction
)
)

joblib.dump(
    model,
    "emotion_model.pkl"
)

print("\nEmotion Model Saved")