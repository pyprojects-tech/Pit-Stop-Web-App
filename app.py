from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Initialize the dataframe with the new columns
df = pd.DataFrame(columns=['Address', 'Rating', 'Comments'])

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
    app.logger.info(f"Received data: {data}")
    
    if not data or 'review' not in data:
        app.logger.error("Invalid data structure received")
        return jsonify({"message": "Invalid data structure received"}), 400

    review = data['review']
    app.logger.info(f"Review data: {review}")

    # Validate the received data
    required_fields = ['address', 'rating', 'comments']
    missing_fields = [field for field in required_fields if field not in review or not review[field]]
    if missing_fields:
        app.logger.error(f"Missing fields: {missing_fields}")
        return jsonify({"message": f"Please fill out all the required fields. Missing: {', '.join(missing_fields)}"}), 400

    # Create a new entry
    new_entry = pd.DataFrame({
        'Address': [review['address']],
        'Rating': [int(review['rating'])],
        'Comments': [review['comments']]
    })

    app.logger.info(f"New entry: {new_entry.to_dict('records')}")

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