Change Log 

10.02.2024
Database
- Added a new column to the database to store the cuurent date and time of the review as the variable Date_Time. 
- Changed from a CSV data storage infrastructure to a SQL database using SQLite3. 
- Made the Pandas dataframe read from the SQL database "data.db" file instead of writing a new dataframe each time which would erase the previous data. . 

Troubleshooting
- Added a "data.html" file and path to the "app.py" file so that the website would display the data from the SQL database. This location is not linked but can be accessed by navigating to "http://127.0.0.1:5000/data". 