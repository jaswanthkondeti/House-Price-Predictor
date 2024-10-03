from flask import Flask, request, jsonify, render_template, redirect, url_for
import util
from pymongo import MongoClient

app = Flask(__name__, static_folder='static')

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']  # Replace with your database name
users_collection = db['users']  # Collection for storing user info

@app.route("/")
def login():
    return render_template('login.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/signup.html')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        if not (name and email and phone and password):
            return jsonify({"error": "All fields are required!"}), 400

        # Check if the user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return jsonify({"error": "User already exists!"}), 400

        # Store the user in the database
        users_collection.insert_one({"name": name, "email": email, "phone": phone, "password": password})
        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        print(f"Error during signup: {e}")
        return jsonify({"error": "Internal server error!"}), 500

@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not (email and password):
            return jsonify({"error": "Email and password are required!"}), 400

        # Check for user in the database
        user = users_collection.find_one({"email": email, "password": password})
        if user:
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid email or password!"}), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "Internal server error!"}), 500

@app.route('/get_locations')
def get_locations():
    locations = util.get_locations()
    response = jsonify({'locations': locations})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_homeprice', methods=['POST'])
def predict_homeprice():
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Content-Type must be application/json"}), 415

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        total_sqft = float(data.get('total_sqft', 0))
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))
        location = str(data.get('location', ''))

        if total_sqft <= 0 or bhk <= 0 or bath <= 0 or not location:
            return jsonify({"error": "Invalid data"}), 400

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        return jsonify({"estimated_price": estimated_price})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    util.load_locations()
    app.run(port=3001)
