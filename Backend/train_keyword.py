import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# ---------------------------------------------------
# Dataset
# ---------------------------------------------------

texts = [

# Emergency

("help me",1),
("please help",1),
("save me",1),
("stop",1),
("stop please",1),
("call police",1),
("call the police",1),
("he is attacking me",1),
("someone is following me",1),
("kidnap",1),
("don't touch me",1),
("leave me",1),
("i am scared",1),
("i need help",1),
("emergency",1),
("danger",1),
("help",1),
("please save me",1),
("help police",1),
("he is chasing me",1),

# Safe

("hello",0),
("good morning",0),
("good evening",0),
("how are you",0),
("i am fine",0),
("thank you",0),
("nice to meet you",0),
("good job",0),
("welcome",0),
("see you tomorrow",0),
("happy birthday",0),
("have a nice day",0),
("good night",0),
("i reached home",0),
("everything is okay",0),
("lets go shopping",0),
("thank you so much",0),
("what are you doing",0),
("lets eat",0),
("see you later",0)

]

df = pd.DataFrame(
    texts,
    columns=[
        "text",
        "label"
    ]
)

df.to_csv(
    "keyword_dataset.csv",
    index=False
)

# ---------------------------------------------------
# Split
# ---------------------------------------------------

X = df["text"]

y = df["label"]

X_train,X_test,y_train,y_test = train_test_split(

    X,
    y,
    test_size=0.20,
    random_state=42

)

# ---------------------------------------------------
# Pipeline
# ---------------------------------------------------

model = Pipeline([

    (
        "tfidf",
        TfidfVectorizer()
    ),

    (
        "classifier",
        MultinomialNB()
    )

])

model.fit(

    X_train,
    y_train

)

prediction = model.predict(

    X_test

)

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

"keyword_model.pkl"

)

print("\nKeyword Model Saved Successfully")