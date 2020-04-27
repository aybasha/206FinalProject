import os
import sys
import requests
import sqlite3


#######YELP#######

#Grab data from database
def get_data(conn, cur):
	city = sys.argv[1]
	r = requests.get('https://api.yelp.com/v3/businesses/search?location=' + city, headers={'Authorization': 'Bearer rOfTzkagaCPTnPiF96gkzi9iy7YzzPHxINhCMT7hFTe4ABO1An9Lo3UhGxPcwFqD74WSKUW_ZjJVu6uiKU3TGIgR7BnA0sDM4RMn_xtDMOAwAdeTPt731WvetwyBXnYx'})
	businesses = r.json()['businesses']

	#Create Tables
	#cur.execute("DROP TABLE IF EXISTS Businesses")
	cur.execute("CREATE TABLE IF NOT EXISTS Businesses (business_id TEXT PRIMARY KEY, name TEXT, rating REAL)")

	#cur.execute("DROP TABLE IF EXISTS Cities")
	cur.execute("CREATE TABLE IF NOT EXISTS Cities (id TEXT PRIMARY KEY, location TEXT, FOREIGN KEY (id) REFERENCES Businesses(business_id))")

	for business in businesses:
		cur.execute("INSERT OR REPLACE INTO Businesses (business_id, name, rating) VALUES (?,?,?)", (business['id'], business['name'], business['rating']))
		cur.execute("INSERT OR REPLACE INTO Cities (id, location) VALUES (?,?)", (business['id'], city))

	conn.commit()


#Connect to database
conn = sqlite3.connect('masterDB.db')
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()
get_data(conn, cur)


