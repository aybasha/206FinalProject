# PROCESSES DATA INTO MOVIES TABLE IN DATABASE (Amir Basha)

from bs4 import BeautifulSoup
import requests
import re
import os
import sqlite3
import json

# Pulls data of the movie titles from defined website urls, stores data in cache
# If cache file already exists, function returns and doesn't pull data again
# Calls the API directly for each title read in and filters any invalid titles 
# (i.e. foreign movies, since this is for US only) and adds the api response to
# a dictionary to be output as a cache
def getMovieTitles():
	dir = os.path.dirname(__file__)
	if os.path.exists(os.path.join(dir, "movieTitles_cache.txt")):
		return
	outFile = open(os.path.join(dir, "movieTitles_cache.txt"), "w")
	urls = ["https://www.imdb.com/list/ls063484067/", #2015
			"https://www.imdb.com/list/ls063924870/", #2016
			"https://www.imdb.com/list/ls023426386/", #2017
			"https://www.imdb.com/list/ls047677021/", #2018
			"https://www.imdb.com/list/ls041214362/"] #2019
	year = 2015
	resDict = {2015: [], 2016: [], 2017: [], 2018: [], 2019: []}
	for url in urls:
		page = requests.get(url)
		soup = BeautifulSoup(page.text, "lxml")
		for movieTitle in soup.find_all("h3", "lister-item-header"):
			r = requests.get(setUpURL(movieTitle.a.get_text().strip()))
			movieInfo = json.loads(r.text)
			if (movieInfo["Response"] == "False"):
				continue
			resDict[year].append(movieInfo)
		year += 1
	outFile.write(json.dumps(resDict))
	outFile.close()
	print("Cache file created")

# Reads cache json file and returns loaded dictionary
def readCache(FNAME):
	dir = os.path.dirname(__file__)
	inFile = open(os.path.join(dir, FNAME), "r")
	contents = inFile.read()
	cache_dict = json.loads(contents)
	inFile.close()
	return cache_dict

# Sets up the curr/conn connections needed for the database
# Also creates table if not already present for movie input
def setUpDatabaseAndTable(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Movies 
				(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
				year TEXT, genre TEXT, IMDB_Rating TEXT,
				RottenTomatoes_Rating TEXT, Metacritic_rating TEXT)''')
    conn.commit()
    return cur, conn

# Sets up URL for omdbAPI for movie info request
def setUpURL(movieTitle):
	key = "8239fadc"
	url = "http://www.omdbapi.com/?apikey=" + key + "&t=" + movieTitle
	url = url + "&type=movie&plot=short&r=json"
	return url

# Gets count value to indicate number of elements in table for
# the 20 addition limit
def getCount(cur):
	cur.execute("SELECT max(id) FROM Movies")
	count = cur.fetchone()[0]
	if count is None:
		count = 0
	return count

# Converts the movie dictionary to a single list of tuples for easy
# indexing when adding to the database and access to the year
def convertToList(movieDict):
	res = []
	for k in movieDict:
		for movieInfo in movieDict[k]:
			res.append((k, movieInfo))
	return res

# Adds elements to the database 20 elements at a time based on the
# Count value that indicates the number of elements in the database
# Prints results of movie addition and total movies at the end
def addToDatabase(cur, conn, movieDictList, count):
	countAdded = 0
	for x in range(count, count+20):
		if (x >= len(movieDictList)):
			break
		movieTitle = movieDictList[x][1]["Title"]
		year = movieDictList[x][0]
		genres = movieDictList[x][1]["Genre"]
		ratings = {"Internet Movie Database": "N/A", "Rotten Tomatoes": "N/A", "Metacritic": "N/A"}
		for y in (movieDictList[x][1]["Ratings"]):
			ratings[y["Source"]] = y["Value"]
		cur.execute('''INSERT INTO Movies (title, year, genre, IMDB_Rating,
					RottenTomatoes_Rating, Metacritic_rating) VALUES (?, ?, ?, ?, ?, ?)''',
					(movieTitle, year, genres, ratings["Internet Movie Database"], 
					ratings["Rotten Tomatoes"], ratings["Metacritic"]))
		countAdded += 1
		print("Proccessed: " + movieTitle + " - (" + year + ")")
	print("Number of Proccessed Movies this Run: " + str(countAdded))
	print("Total Number of Proccessed Movies: " + str(getCount(cur)))
	conn.commit()

# Main
def main():
	getMovieTitles()
	movieDict = readCache("movieTitles_cache.txt")
	cur, conn = setUpDatabaseAndTable("masterDB.db")
	count = getCount(cur)
	movieDictList = convertToList(movieDict)
	addToDatabase(cur, conn, movieDictList, count)
	conn.close()

if __name__ == "__main__":
    main()