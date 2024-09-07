from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Initialize the dataframe with the new columns
df = pd.DataFrame(columns=['Address', 'Cleanliness', 'Safety', 'Stalls', 'KeyRequired', 'Comments'])

@app.route('/')
def home():
    # Redirect to the main page or render a home template
    return redirect(url_for('main'))  # Assuming you have a 'main' route

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/review')
def review():
    mapbox_access_token = 'pk.eyJ1IjoicHlwcm9qZWN0c3RlY2giLCJhIjoiY20wb2kxMG1wMDkyazJscHkzamZ0ZWNhbSJ9.IKqL2NV6IzGWoMPhc4DfVg'
    return render_template('review.html', mapbox_access_token=mapbox_access_token)

@app.route('/submit', methods=['POST'])
def submit():
    global df
    data = request.json
    app.logger.info(f"Received data: {data}")  # Add this line
    
    if not data or 'ratings' not in data:
        app.logger.error("Invalid data received")  # Add this line
        return jsonify({"message": "Invalid data received"}), 400

    ratings = data['ratings']
    app.logger.info(f"Ratings: {ratings}")  # Add this line

    # Validate the received data
    required_fields = ['address', 'cleanliness', 'safety', 'stalls', 'keyRequired']
    missing_fields = [field for field in required_fields if field not in ratings or not ratings[field]]
    if missing_fields:
        app.logger.error(f"Missing fields: {missing_fields}")  # Add this line
        return jsonify({"message": f"Please fill out all the required fields. Missing: {', '.join(missing_fields)}"}), 400

    # Convert ratings to integers if they're not empty, otherwise use None
    def safe_int(value):
        return int(value) if value and value.strip() else None

    # Create a new entry
    new_entry = pd.DataFrame({
        'Address': [ratings['address']],
        'Cleanliness': [safe_int(ratings['cleanliness'])],
        'Safety': [safe_int(ratings['safety'])],
        'Stalls': [safe_int(ratings['stalls'])],
        'KeyRequired': [ratings['keyRequired']],
        'Comments': [ratings['comments']]
    })

    app.logger.info(f"New entry: {new_entry.to_dict('records')}")  # Add this line

    # Add the new entry to the DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)

    return jsonify({"message": "Review submitted successfully!"})

@app.route('/display')
def display():
    return df.to_json(orient='records')

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)