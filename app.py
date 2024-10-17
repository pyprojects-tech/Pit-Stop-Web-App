from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import sqlite3

app = Flask(__name__)

# Initialize the dataframe with the new columns

conn = sqlite3.connect('templates/data.db',check_same_thread=False)
df = pd.read_sql_query("SELECT * FROM reviews", conn)

#df = pd.DataFrame(columns=['Address', 'Rating', 'Comments','Date_Time','ID'])
#app.logger.info(f"New entry: {df.to_dict('records')}")
#df.to_sql('reviews', conn, if_exists='replace', index=False)

df_avg = df.groupby('ID', as_index=False)['Rating'].mean()
df_avg.columns = ['ID', 'Average_Rating']
df_avg_dict = df_avg.set_index('ID')['Average_Rating'].to_dict()
 # Debugging line to check the structure of review

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
    required_fields = ['address', 'rating']
    missing_fields = [field for field in required_fields if field not in review or not review[field]]
    if missing_fields:
        app.logger.error(f"Missing fields: {missing_fields}")
        return jsonify({"message": f"Please fill out all the required fields. Missing: {', '.join(missing_fields)}"}), 400

    # Create a new entry
    new_entry = pd.DataFrame({
        'Address': [review['address']],
        'Rating': [int(review['rating'])],
        'Comments': [review['comments']],
        'Date_Time': [review['Date_Time']],
        'ID': [review['id']],      
    })

    app.logger.info(f"New entry: {new_entry.to_dict('records')}")

    # Add the new entry to the DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)
    ###REMOVE THIS LATER ONCE SQLITE IS WORKING###
    df.to_csv('zenstopdata.csv', index=False)
    #Script to write to SQLite
    df.to_sql('reviews', conn, if_exists='replace', index=False)

    # Generate the HTML file
    html_content = df.to_html(index=False)

    with open('templates/data.html', 'w') as f:
        f.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Data Display</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
    """)
    return jsonify({"message": "Review submitted successfully!"})

@app.route('/display')
def display():
    return df.to_json(orient='records')

@app.route('/search')
def search():
    return render_template('search.html', df_avg=df_avg_dict)

@app.route('/data')
def data():
    return render_template('data.html')
if __name__ == '__main__':
    app.run(debug=True)