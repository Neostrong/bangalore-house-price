import pickle
import json
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CHANGE THIS LINE ↓
with open(
    os.path.join(BASE_DIR, "model", "banglore_home_prices_model.pickle"), "rb"
) as f:
    model = pickle.load(f)

# CHANGE THIS LINE ↓
with open(os.path.join(BASE_DIR, "model", "columns.json"), "r") as f:
    data = json.load(f)
    data_columns = data["data_columns"]
    locations = data_columns[3:]


def get_locations():
    return locations


def predict_price(location: str, sqft: float, bath: int, bhk: int) -> float:
    location = location.lower().strip()
    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if location in data_columns:
        loc_index = data_columns.index(location)
        x[loc_index] = 1
    return round(model.predict([x])[0], 2)
