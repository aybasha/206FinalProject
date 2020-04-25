# MAKES AVERAGE RATING CALCULATIONS FOR EACH GENRE FOR EACH YEAR,
# THEN OUTPUTS RESULT INTO FILE AS JSON (Amir Basha)

from collections import defaultdict
import os
import sqlite3
import json

# Selects genre(s) and ratings from the database based on passed in year 
# and calculates an average rating for each movie and adds that to a list 
# of average ratings for each genre. Weighted average rating for each genre is then
# calculated and passed into a dictionary of key value year and value of
# a dictionary list of weighted average ratings for each genre for that year
def processYearGenreData(cur, conn, year, yearDict):
	cur.execute('''SELECT genre, IMDB_Rating, RottenTomatoes_Rating, Metacritic_Rating 
				FROM Movies WHERE year=?''', (str(year), ))
	resList = cur.fetchall()
	cur.execute("SELECT max(id) FROM Movies")
	count = cur.fetchone()[0]
	genreDict = defaultdict(list)
	for res in resList:
		avgSing = calculateAverageSingle(res[1], res[2], res[3])
		if (avgSing != False):
			for genre in res[0].split(","):
				genreDict[genre.strip()].append(avgSing)
	genreAverageDict = defaultdict(float)
	for key in genreDict:
		wAvg = calculateWeightedAverage(genreDict[key], count)
		genreAverageDict[key] = wAvg
	yearDict[year] = dict(genreAverageDict)
	return genreAverageDict

# Converts string rating to a decimal percentage based on type
# Valid types are IMDB, RottenTomatoes, Metacritic
def convertRating(ratingString, ratingType):
	if (ratingType == "IMDB"):
		ratingChunk = float(ratingString[:3])/10.0
		return ratingChunk
	elif (ratingType == "RottenTomatoes" or ratingType == "Metacritic"):
		if len(ratingString) == 2:
			ratingChunk = float(ratingString[0])/100.0
		else:
			ratingChunk = float(ratingString[:2])/100.0
		return ratingChunk
	return None

# Calculates average of a given set of ratings in the database, returning the average
# If all ratings are N/A, returns False indicating to disclude this data point
# in the genre ratings
def calculateAverageSingle(imdbRatingString, rotTomRatingString, metaRatingString):
	total, count = 0.0, 0
	if (imdbRatingString != "N/A"):
		total = total + convertRating(imdbRatingString, "IMDB")
		count += 1
	if (rotTomRatingString != "N/A"):
		total = total + convertRating(rotTomRatingString, "RottenTomatoes")
		count += 1
	if (metaRatingString != "N/A"):
		total = total + convertRating(metaRatingString, "Metacritic")
		count += 1
	if (count == 0):
		return False
	return total / count

# Calculates weighted average of a list of rating averages for a given list of 
# rating averages for a specific genre. The weight is defined by the number of 
# movies make up that genre out of the total movies and is multiplied by the average
# of the ratings for a given genre
def calculateWeightedAverage(genreRatingsList, totalMovies):
	total = 0.0
	for x in genreRatingsList:
		total += x
	weight = len(genreRatingsList) / totalMovies
	return (total / len(genreRatingsList)) * weight

# Sets up the curr/conn connections needed for the database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# Outputs resulting average of genre ratings by year dictionary as a json
# dump file and writes that to a text file. Also prints indication that
# the file was successfully created
def outputToFile(calculationsDict):
	dir = os.path.dirname(__file__)
	outFile = open(os.path.join(dir, "movies_calculations.txt"), "w")
	outFile.write(json.dumps(calculationsDict))
	outFile.close()
	print("Calculations file created!")

# Main
def main():
	yearDict = {2015: [], 2016: [], 2017: [], 2018: [], 2019: []}
	cur, conn = setUpDatabase("masterDB.db")
	for year in range(2015, 2020):
		processYearGenreData(cur, conn, year, yearDict)
	outputToFile(yearDict)
	conn.close()

if __name__ == "__main__":
    main()