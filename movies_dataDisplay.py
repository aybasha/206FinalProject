# CREATES VISUALIZATION OF THE CALCULATED DATA (Amir Basha)

import json
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

# Reads the json calculations data into a dictionary
# for usage with data display
def readCalculationData(filename):
	dir = os.path.dirname(__file__)
	inFile = open(os.path.join(dir, filename), "r")
	contents = inFile.read()
	dataDict = json.loads(contents)
	inFile.close()
	return dataDict

# Gets the top X genres based on the parameter from a given
# dictionary list of genres
def getTopGenres(numToGet, genreDictList):
	if (numToGet > len(genreDictList)):
		numToGet = len(genreDictList)
	sortedGenres = sorted(genreDictList.items(), key=lambda x: x[1], reverse=True)
	output = []
	for x in range(numToGet):
		output.append(sortedGenres[x])
	return output

# Calls the getTopGenres function on each year and builts a dictionary
# for each year of the top X genres based on the parameter numToGet
def getTopGenresYearByYear(numToGet, calcDict):
	output = {"2015": [], "2016": [], "2017": [], "2018": [], "2019": []}
	for year in calcDict:
		output[year] = getTopGenres(numToGet, calcDict[year])
	return output

# Assigns colors for each of the unique genres for plotting
# and puts into a dictionary for lookup
def assignGenreColors(topGenres):
	colorList = ['blue', 'green', 'red', 'cyan', 'magenta', 'gold', 'black',
				'brown', 'orange', 'darkolivegreen', 'limegreen', 'turquoise',
				'teal', 'indigo', 'skyblue', 'yellow', 'palegreen', 'pink',
				'purple']
	genreList = []
	for year in topGenres:
		for genre in topGenres[year]:
			if genre[0] not in genreList:
				genreList.append(genre[0])
	genreColorDict = {}
	for x in range(len(genreList)):
		genreColorDict[genreList[x]] = colorList[x]
	return genreList, genreColorDict

# Creates patch legend handles to be used for a custom legend
# for the entire subplot of genres
def generateLegendHandles(genreColorDict):
	legendHandler = []
	for genre in genreColorDict:
		color = genreColorDict[genre]
		patchToAdd = Patch(facecolor=color, edgecolor=color)
		legendHandler.append(patchToAdd)
	return legendHandler

# Builds a subplot for each year's top X genres in a 3x3 grid
# Adds axis labels and a legend for the entire figure that indicates
# which colors correspond to which genres plotted. The output figure
# fits the full screen
def visualizeTopData(topGenres):
	width = 0.3
	genreList, genreColorDict = assignGenreColors(topGenres)
	fig, axs = plt.figure(constrained_layout=True), []
	grid = gridspec.GridSpec(2, 12, figure=fig)
	axs.append(fig.add_subplot(grid[0, 0:4]))
	axs.append(fig.add_subplot(grid[0, 4:8]))
	axs.append(fig.add_subplot(grid[0, 8:]))
	axs.append(fig.add_subplot(grid[1, 0:4]))
	axs.append(fig.add_subplot(grid[1, 8:12]))
	counter = 0
	for year in topGenres:
		widthAdjust = 0
		for genre in topGenres[year]:
			axs[counter].bar(width * widthAdjust + widthAdjust/10, genre[1],
						  width, color = genreColorDict[genre[0]])
			widthAdjust += 1
		axs[counter].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
		axs[counter].set_xlabel("Genres")
		axs[counter].set_ylabel("Rating Score")
		axs[counter].title.set_text("Top Movie Genres of " + year)
		counter += 1
	mng = plt.get_current_fig_manager()
	mng.window.showMaximized()
	legendHandles = generateLegendHandles(genreColorDict)
	plt.figlegend(legendHandles, genreList, title="Genres", title_fontsize=24,
				  loc="lower center", fontsize=14, ncol=3)
	plt.show()

# Main
def main():
	calcDict = readCalculationData("movies_calculations.txt")
	topGenres = getTopGenresYearByYear(10, calcDict)
	visualizeTopData(topGenres)

if __name__ == "__main__":
    main()