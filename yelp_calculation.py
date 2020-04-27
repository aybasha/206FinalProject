import os
import sys
import sqlite3
import json
import matplotlib.pyplot as plt

#retrieve data from database
def retrieve_data(conn, cur):
	city_ratings = {}
	cur.execute("SELECT rating FROM Businesses JOIN CITIES ON Businesses.business_id=Cities.id WHERE Cities.location='Boston'")
	rows = cur.fetchall()
	for row in rows:
		if 'Boston' not in city_ratings:
			city_ratings['Boston'] = [row[0]]
		else:
			city_ratings['Boston'].append(row[0])


	cur.execute("SELECT rating FROM Businesses JOIN CITIES ON Businesses.business_id=Cities.id WHERE Cities.location='New'")
	rows = cur.fetchall()
	for row in rows:
		if 'New York' not in city_ratings:
			city_ratings['New York'] = [row[0]]
		else:
			city_ratings['New York'].append(row[0])


	cur.execute("SELECT rating FROM Businesses JOIN CITIES ON Businesses.business_id=Cities.id WHERE Cities.location='Miami'")
	rows = cur.fetchall()
	for row in rows:
		if 'Miami' not in city_ratings:
			city_ratings['Miami'] = [row[0]]
		else:
			city_ratings['Miami'].append(row[0])


	cur.execute("SELECT rating FROM Businesses JOIN CITIES ON Businesses.business_id=Cities.id WHERE Cities.location='Detroit'")
	rows = cur.fetchall()
	for row in rows:
		if 'Detroit' not in city_ratings:
			city_ratings['Detroit'] = [row[0]]
		else:
			city_ratings['Detroit'].append(row[0])


	cur.execute("SELECT rating FROM Businesses JOIN CITIES ON Businesses.business_id=Cities.id WHERE Cities.location='Los'")
	rows = cur.fetchall()
	for row in rows:
		if 'Los Angeles' not in city_ratings:
			city_ratings['Los Angeles'] = [row[0]]
		else:
			city_ratings['Los Angeles'].append(row[0])
	return city_ratings


#Calculation
def calculate_data(city_ratings):
	for city, ratings in city_ratings.items():
		total = 0
		count = 0
		for rating in ratings:
			total += rating
			count += 1
		city_ratings[city] = (total / count)
	return city_ratings

#write to json file
def write_to_json(city_ratings):
	with open('ratings.json', 'w') as f:
		json.dump(city_ratings, f, indent=4)


conn = sqlite3.connect('masterDb.db')
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()
city_ratings = calculate_data(retrieve_data(conn, cur))
write_to_json(city_ratings)




