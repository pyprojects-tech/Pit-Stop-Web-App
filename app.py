from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd

app = Flask(__name__)

# Define the specific categories
CATEGORIES = ["Bathrooms", "Caffeine", "Nap Zone"]

# Initialize an empty DataFrame with the specific categories
df = pd.DataFrame(columns=['Address', 'Category', 'Rating', 'Comment'])

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/review')
def review():
    return render_template('review.html', categories=CATEGORIES)

@app.route('/submit', methods=['POST'])
def submit():
    global df
    data = request.json
    if not data or 'address' not in data or 'ratings' not in data:
        return jsonify({"message": "Invalid data received"}), 400

    address = data['address']
    ratings = data['ratings']

    new_entries = []
    for category, entry in ratings.items():
        new_entries.append({
            'Address': address,
            'Category': category,
            'Rating': entry['rating'],
            'Comment': entry['comment']
        })
    
    df = pd.concat([df, pd.DataFrame(new_entries)], ignore_index=True)
    return jsonify({"message": "Entries added successfully!"})

@app.route('/display')
def display():
    return df.to_json(orient='records')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/review_content')
def review_content():
    location = request.args.get('location', '')
    return render_template('review_content.html', categories=CATEGORIES, location=location)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    location = request.form.get('location')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    # Process the review data (e.g., save to database)
    
    return jsonify({'message': 'Review submitted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)