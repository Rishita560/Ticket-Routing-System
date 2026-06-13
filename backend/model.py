import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_MODEL = os.path.join(
    BASE_DIR,
    "..",
    "ml",
    "models",
    "classifier.pkl"
)

PRIORITY_MODEL = os.path.join(
    BASE_DIR,
    "..",
    "ml",
    "models",
    "priority_model.pkl"
)

category_model = joblib.load(CATEGORY_MODEL)
priority_model = joblib.load(PRIORITY_MODEL)
#category_model = joblib.load("../ml/models/classifier.pkl")
#priority_model = joblib.load("../ml/models/priority_model.pkl")

def predict_ticket(text):

    category = category_model.predict([text])[0]
    confidence = max(category_model.predict_proba([text])[0])

    priority = priority_model.predict([text])[0]

    # PRIORITY model confidence
    priority_probs = priority_model.predict_proba([text])[0]
    priority_conf = max(priority_probs)

    if priority_conf < 0.45:
        priority = "medium"

    return category, priority, round(confidence, 2)