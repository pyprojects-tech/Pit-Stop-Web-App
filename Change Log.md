Change Log 
10.16.2025
-I was able to modify the code so that the search.html and review.html pages are pulling the same unique ids in the same fashion, however the ids are not matching up with the correct locations on the map - there are duplicate ids for different locations.


10.15.2025
-I've made some progress but I need to still work on things. It looks like the search.html and review.html pages are pulling different unique ids for the same address. I think the issue is do to the search.html being based on the POI and review.html is being based on the address. 


10.14.2024
-I was able to implement a new system to match reviews with their markers. I am using the unique geolocation id rather than address now. I am able to pull the ID and rating from the df_avg dataframe that's created from the ratings database. I am having issues with how the markers are being displayed on the map. It looks like like reviews/ID's are not being matched with the correct markers and rather the markers are pulling every rating for the entire dictionary. 
-I updated the dataframe and SQL database to include a new column for the geolocaiton ID.

10.09.2024
-Need to figure out why reviews are showing up as blue icon rather than poop emoji
-Addresses are being stored differently in the search bar on the review page than then they are being pulled on the map


10.06.2024
Database
-Created an average dataframe, df_avg, which stores the average rating for address. This object is passed through javascript on the search.html file to display the average rating on the map as marker size. 

Search
-I was able to add the numberical rating and emoji to the left of the marker based on the average rating for that address. Only 1 rating is currently being displayed and I will need to troubleshoot the code to figure out why there is only one rating being displayed.

10.02.2024
Database
- Added a new column to the database to store the cuurent date and time of the review as the variable Date_Time. 
- Changed from a CSV data storage infrastructure to a SQL database using SQLite3. 
- Made the Pandas dataframe read from the SQL database "data.db" file instead of writing a new dataframe each time which would erase the previous data. . 

General 
-Created a Trello board to help with the development process with the link https://trello.com/b/hNg61et4/zenstop-webb-app

Troubleshooting
- Added a "data.html" file and path to the "app.py" file so that the website would display the data from the SQL database. This location is not linked but can be accessed by navigating to "http://127.0.0.1:5000/data". 