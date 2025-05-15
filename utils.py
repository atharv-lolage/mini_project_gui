import json
import os
from datetime import datetime

# Load JSON data from a file; return {} if file is missing or invalid
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Save Python dict to JSON file with indentation
def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Calculate age (in years) from DOB string YYYY-MM-DD
def calculate_age(dob_str):
    dob = datetime.strptime(dob_str, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return max(age, 0)

# Prompt user for a valid date until correct format provided
def get_valid_date(prompt):
    while True:
        date_input = input(f"{prompt} ")
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")
