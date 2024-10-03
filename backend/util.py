import json
import pickle
import numpy as np

locations = None
data = None
model = None

def get_estimated_price(location, total_sqft, bhk, bath):
    # Ensure location is a string
    location = str(location).lower()

    # Ensure total_sqft, bhk, and bath are floats/ints
    try:
        total_sqft = float(total_sqft)
        bhk = int(bhk)
        bath = int(bath)
    except ValueError as e:
        print(f"ValueError in conversion: {e}")
        raise

    # Ensure location is in the list
    try:
        loc_index = data.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(data))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(model.predict([x])[0], 2)

def get_locations():
    return locations

def load_locations():
    print("Loading the locations...")
    global data
    global locations
    global model

    try:
        with open("./ml_files/columns.json", 'r') as f:
            data = json.load(f)['data_columns']
            locations = data[3:]
    except Exception as e:
        print("Error loading JSON file:", e)  

    try:
        with open("./ml_files/banglore_house_prices_model.pickle", 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        print("Error loading model file:", e)  

if __name__ == "__main__":
    load_locations()
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
