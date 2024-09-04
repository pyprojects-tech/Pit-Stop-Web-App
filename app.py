import os
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Define the specific categories
CATEGORIES = ["Bathrooms", "Food", "Safety", "Cleanliness", "Staff"]

# Initialize an empty DataFrame with the specific categories
df = pd.DataFrame(columns=['Category', 'Rating', 'Comment'])

@app.route('/')
def index():
    return render_template('index.html', categories=CATEGORIES)

@app.route('/submit', methods=['POST'])
def submit():
    global df
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400

    new_entries = []
    for category, entry in data.items():
        new_entries.append({
            'Category': category,
            'Rating': entry['rating'],
            'Comment': entry['comment']
        })
    
    df = pd.concat([df, pd.DataFrame(new_entries)], ignore_index=True)
    return jsonify({"message": "Entries added successfully!"})

@app.route('/display')
def display():
    return df.to_json(orient='records')

if __name__ == '__main__':
    # This block will only run when you're running the app locally
    app.run(debug=True)